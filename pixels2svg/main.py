from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, TypeVar, Union

import cc3d
import numpy as np
from svgwrite.container import Group

from pixels2svg.utils import geometry, pixel, svg
from pixels2svg.utils.geometry import Contours

T = TypeVar('T')


def find_contours(
        rgba_array: np.ndarray,
        group_by_color: bool = False
) -> Union[Dict[pixel.PixelRGBA, Tuple[Contours, ...]],
           Tuple[Tuple[Contours, pixel.PixelRGBA], ...]]:
    id_array = pixel.rgba_array_to_id_array(rgba_array)
    labels = cc3d.connected_components(id_array,
                                       out_dtype=np.uint64,
                                       connectivity=4)
    if group_by_color:
        all_contours: dict = {}
        result = OrderedDict()
    else:
        all_contours: list = []
        result = tuple()

    def sort_contours_by_area(
            contours_list: List[Tuple[T, int]]) -> Tuple[T, ...]:
        sorted_contours = sorted(contours_list,
                                 key=lambda c: c[1],
                                 reverse=True)
        return tuple(c[0] for c in sorted_contours)

    for blob_id, blob_shape in cc3d.each(labels, binary=True, in_place=True):

        pixel_coord = geometry.find_first_non_zero_coords(blob_shape)
        color = tuple(rgba_array[pixel_coord])
        # ignore transparent pixels
        if color[3] == 0:
            continue

        contours: Contours = geometry.calculate_blob_contours(blob_shape)
        shape_area = blob_shape.sum()

        if group_by_color:
            all_contours: dict
            if color in all_contours:
                all_contours[color].append((contours, shape_area))
            else:
                all_contours[color] = [(contours, shape_area)]
        else:
            all_contours: list
            all_contours.append(((contours, color), shape_area))

        if group_by_color:
            sorted_colors = sort_contours_by_area(
                [(color, sum(c[1] for c in contours_list))
                 for color, contours_list in all_contours.items()]
            )
            result = OrderedDict()
            for color in sorted_colors:
                result[color] = sort_contours_by_area(all_contours[color])
        else:
            result = sort_contours_by_area(all_contours)

    return result


def trace_pixel_polygons_as_svg(rgba_array: np.ndarray,
                                group_by_color: bool = False) -> svg.Drawing:
    traced_contours = find_contours(rgba_array, group_by_color)

    svg_img = svg.Drawing(rgba_array.shape[0], rgba_array.shape[1])

    has_opacity = np.any(rgba_array[:, :, 3] < 255)

    def color_to_id(color: pixel.PixelRGBA) -> str:
        hex_color = pixel.rgb_color_to_hex_code(color[:3])[1:]
        opacity = color[3] / 255
        color_id = f'x{hex_color}_r{color[0]}_g{color[1]}_b{color[2]}'
        if has_opacity:
            color_id = f'{color_id}_a{opacity}'
        return color_id

    if group_by_color:
        traced_contours: Dict[pixel.PixelRGBA, Tuple[Contours, ...]]
        for color, contours_tuple in traced_contours.items():
            color_id = color_to_id(color)
            group = Group(id=color_id)
            for i, contour in enumerate(contours_tuple, start=1):
                polygon_id = f'{color_id}_shape{i}'
                svg.draw_polygon(group,
                                 contour.outside,
                                 holes=contour.inner_holes,
                                 color=color,
                                 id=polygon_id)
            svg_img.add(group)

    else:
        traced_contours: Tuple[Tuple[Contours, pixel.PixelRGBA], ...]
        for i, (contour, color) in enumerate(traced_contours, start=1):
            color_id = color_to_id(color)
            polygon_id = f'shape{i}_{color_id}'
            svg.draw_polygon(svg_img,
                             contour.outside,
                             holes=contour.inner_holes,
                             color=color,
                             id=polygon_id)

    return svg_img


def pixels2svg(input_path: str,
               output_path: Optional[str] = None,
               group_by_color: bool = True,
               as_string: bool = False,
               pretty: bool = True) -> Optional[Union[svg.Drawing, str]]:
    """
    Parameters
    ----------
    input_path : str
        Path of the input bitmap image
    output_path : Optional[str]
        Path of the output SVG image (optional).
        If passed, the function will return None.
        If not passed, the function will return the SVG data as a `str` or a
        `Drawing` depending on the `as_string` parameter.
    group_by_color : bool
        If True (default), group same-color shapes under <g> SVG elements.
    as_string: bool
        If True and no `output_path` is passed, return a `str` representing
        the SVG data.
    pretty: bool
        If True (default), output SVG code is pretty-printed.

    Returns
    -------
    Optional[Union[svg.Drawing, str]]
        Depends on the `output_path` and `as_string` parameters
    """

    img_rgba_array = pixel.read_image(input_path)

    svg_drawing = trace_pixel_polygons_as_svg(img_rgba_array, group_by_color)

    if output_path:
        svg_drawing.save_to_path(output_path, pretty)
    else:
        if as_string:
            return svg_drawing.to_string(pretty)
        else:
            return svg_drawing
