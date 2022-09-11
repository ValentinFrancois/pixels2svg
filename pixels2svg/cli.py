import argparse

from pixels2svg.main import pixels2svg


def run_command():
    parser = argparse.ArgumentParser(description='pixels2svg CLI')
    parser.add_argument('input',
                        metavar='path',
                        type=str,
                        nargs=1,
                        help='input path of the bitmap image. If not '
                             'passed, will print the output in the terminal.')
    parser.add_argument('--output', '-o',
                        metavar='path',
                        type=str,
                        nargs=1,
                        help='output path of the bitmap image',
                        required=False)
    parser.add_argument('--no_group_by_color',
                        action='store_true',
                        help='do not group shapes of same color together '
                             'inside <g> tags ')
    parser.add_argument('--no_pretty',
                        action='store_true',
                        help='do not pretty-write the SVG code')

    args = parser.parse_args()

    output_str = pixels2svg(
        args.input[0],
        output_path=args.output[0] if args.output else None,
        group_by_color=not args.no_group_by_color,
        as_string=not args.output,
        pretty=not args.no_pretty
    )
    if output_str:
        print(output_str)
