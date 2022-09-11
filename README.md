# pixels2svg <sub><sup>v0.0.2</sup></sub>

### Convert pixels to SVG square-based shapes.


There are a few open source tools around that do bitmap -> vector _tracing_,
for instance [potrace](http://potrace.sourceforge.net) which is the engine 
used by [Inkscape](https://inkscape.org) and also has available python 
bindings ([pypotrace](https://pypi.org/project/pypotrace/)).

But sometimes, what you want is the exact bitmap data, but as a set of 
SVG shapes, that you could for instance:
- enlarge for big prints
- use as input paths for a wood laser cutter
- customize in a vector graphics software (edit opacity, contours, overlay 
  on some background image etc.)

Medical image segmentation is another typical use case where one has 
pretty low-res images and sometimes needs to display them best for data 
visualization/presentation purposes. In this case, an SVG overlay with 
editable contours and opacity can be convenient.

This package enables you to easily convert your bitmap image to its 
equivalent SVG representation, each path of the SVG being a polygon made of 
adjacent pixels of same color merged together.

It is inspired of [Florian Berger](https://github.com/florian-berger)'s 
[pixel2svg](https://florian-berger.de/en/software/pixel2svg) package 
(GitHub fork available [here](https://github.com/cyChop/pixel2svg-fork)), 
which is pretty old (python2) and doesn't merge adjacent pixels of same color, 
making the SVG pretty tedious to edit in vector graphics softwares.


### Example 1 - pixel art
| File                                                                                                                                                                           | Preview                                                                                                                              |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| Original PNG image <br/>(32×32)                                                                                                                                                | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/sword.png"  width="32" height="32"/>             | 
| Original PNG image <br/>(browser enlarged)                                                                                                                                     | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/sword.png"  width="256" height="256"/>           |
| Output SVG image                                                                                                                                                               | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/sword_converted.svg"  width="256" height="256"/> | 
| Output SVG image with <br/>customized contour style <br/>(see [examples/sword_outline.py](https://github.com/ValentinFrancois/pixels2svg/blob/main/examples/sword_outline.py)) | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/sword_outline.svg" width="256" height="256"/>    |

### Example 2 - brain scan + segmentation overlay
| File                                                                                                                                                                                                   | Preview                                                                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Scan image (PNG)                                                                                                                                                                                       | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/brain.png" width="256" height="256"/>             |
| Segmentation overlay (PNG)                                                                                                                                                                             | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/overlay.png" width="256" height="256"/>           |
| Converted SVG segmentation overlay                                                                                                                                                                     | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/overlay_converted.svg" width="256" height="256"/> |
| Converted SVG overlayed on PNG scan <br/>with customized opacity & contour style <br/>(see [examples/sword_outline.py](https://github.com/ValentinFrancois/pixels2svg/blob/main/examples/brain_overlay.py)) | <img src="https://raw.githubusercontent.com/ValentinFrancois/pixels2svg/main/images/brain_overlay.svg" width="256" height="256"/>     | 


## Requirements
- Python >= __3.0__

---

## Dependencies
- [svgwrite](https://github.com/mozman/svgwrite)
- [PIL](https://github.com/python-pillow/Pillow)
- [cc3d](https://github.com/seung-lab/connected-components-3d)

---

## Install
```
pip install pixels2svg
```
or directly from Github:
```pixels2svg
pip install git+git://github.com/ValentinFrancois/pixels2svg#egg=pixels2svg
```

---

## Usage examples
### CLI
```
usage: python3 -m pixels2svg [-h] [--output path] [--no_group_by_color] [--no_pretty] path

pixels2svg CLI

positional arguments:
  path                  input path of the bitmap image. If not passed, will print the output in the terminal.

optional arguments:
  -h, --help            show this help message and exit
  --output path, -o path
                        output path of the bitmap image
  --no_group_by_color   do not group shapes of same color together inside <g> tags
  --no_pretty           do not pretty-write the SVG code
```

### In Python

#### Simple usage
```python
from pixels2svg import pixels2svg

pixels2svg('input.png', 'output.svg')
```

`pixels2svg()` accepts a few optional arguments that should help you 
integrate it best within your codebase:

<div style="background-color: rgba(255, 255, 255, 0.05); padding: 0px 10px 2px 10px;">

### Parameters

- **`input_path`** : `str`
  <br/>Path of the input bitmap image


- **`output_path`** : `Optional[str]`
  <br/>Path of the output SVG image (optional). If passed, the function will 
return None. If not passed, the function will return the SVG data as a `str` or a `Drawing` depending on the `as_string` parameter.


- **`group_by_color`** : `bool`
  <br/>If True (default), group same-color shapes under SVG elements.


- **`as_string`** : `bool`
  <br/>If True and no `output_path` is passed, return a `str` representing the SVG data.


- **`pretty`** : `bool`
  <br/>If True (default), output SVG code is pretty-printed.

### Returns

- `Optional[Union[svg.Drawing, str]]`
  <br/>Depends on the `output_path` and `as_string` parameters

</div>

#### Advanced usage

By setting `output_path=None` and `as_string=False`, you can get an object 
inheriting [svgwrite.Drawing](https://svgwrite.readthedocs.io/en/latest/classes/drawing.html), 
with the additional useful methods: 

- `def save_to_path(self, path: str, pretty: bool = False)`
- `def to_string(self, pretty: bool = False) ‑> str`

This gives you access to the `svgwrite` API to modify the output programmatically.

See advanced examples in [examples](https://github.com/ValentinFrancois/pixels2svg/tree/main/examples).

---

## Contributing

PRs are appreciated, just make sure your PR title starts with one of the
following keywords so that the CI works:
- `[MAJOR]`: breaking changes
- `[MINOR]`: feature changes
- `[PATCH]`: fixes
- `[CONFIG]`: changes only related to GitHub (CI, .gitignore, etc.) -> won't trigger a package release

--- 

## Links

A cool SVG path inspector & editor: https://yqnn.github.io/svg-path-editor/ 

Sources of examples images:

- brain tumor scan & overlay: https://www.nature.com/articles/srep16822
- pixel art sword: https://raventale.itch.io/daily-doodles-pixelart-asset-pack
