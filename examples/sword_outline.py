import os.path

from examples.base import SWORD_PNG_PATH

from pixel2svg import Drawing, pixel2svg


if __name__ == '__main__':
    overlay_img = pixel2svg(SWORD_PNG_PATH)
    final_img = Drawing(overlay_img.width, overlay_img.height)

    # add some custom style to the output SVG shapes
    customized_shapes = []
    for element in overlay_img.elements:
        # by default, pixel2svg groups shapes of same color inside <g> elements
        if element.elementname == 'g':
            for shape in element.elements:
                shape['fill-opacity'] = 0
                shape['fill'] = 'none'
                shape['stroke'] = '#666666'
                shape['stroke-width'] = 0.02
                final_img.add(shape)

    final_img.save_to_path(os.path.join(os.path.dirname(SWORD_PNG_PATH),
                                        'sword_outline.svg'))
