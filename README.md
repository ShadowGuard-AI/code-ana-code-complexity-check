![The balloon post at dawn with no lettering: a windsock streaming on the tower edge in the foreground, the nearest balloon just clear of the rooftops with its mail bag beneath it, chimney smoke bending the same way, rooftops running to the city wall, and two more balloons small over the open country](intro-banner.png)


# code-ana-code-complexity-check

![Dawn over the rooftops of a walled city: three balloons climbing away with mail bags under their baskets, a windsock streaming on the tower, and code-ana-code-complexity-check stencilled in cloud cream on the side of the nearest mail bag](banner.png)

![One cream mail envelope with a closed flap, a blank slate postage square and a brass seal, carried under the cropped curve of a monsoon jade balloon on two brass rigging lines, the heading plate](logo.png)

![Balloon post departure in three depths: two distant balloons cross the sky at the pace of the wind, the near balloon climbs in a shallow rise with its basket swaying, and the tower windsock streams and eases while chimney smoke bends in the same rhythm](scene.svg)

Analyzes Python code files and reports the cyclomatic complexity of each function, one line per function with its file and line number. Accepts a single file or a directory, which is searched recursively for .py files. With --max-complexity N the run exits with status 1 when any function exceeds N, so it can gate a script or CI step. A file that does not parse is reported as an error and also fails the run. Complexity counts 1 for entering a function, plus 1 for each if, loop, except handler, conditional expression, comprehension filter, and each extra operand in an and/or chain; nested functions are scored separately, not as part of the function that contains them.

> **Post office notice: this file could not be read.** A file that does not parse is reported as an error and also fails the run.

> **Post office notice: read the text, not only the code.** Scores print to the standard output and failures to the error output, so an exit status of 1 alone does not say whether a function ran over the limit or a file could not be parsed.

![Major separator: the full dotted ground track of a balloon across the page with one gentle drift upward in the middle, slate on cloud cream](sep-heavy.svg)

## Install
`git clone https://github.com/ShadowGuard-AI/code-ana-code-complexity-check`

![Minor separator: a centred run of ground track dots with plain rule on either side](sep-light.svg)

## Usage
`python3 main.py <file-or-directory> [--max-complexity N]`

![Major separator: the full dotted ground track of a balloon across the page with one gentle drift upward in the middle, slate on cloud cream](sep-heavy.svg)

## Verified behavior
- A function with one `if` branch scores complexity 2.
- With `--max-complexity 1`, that same run exits 1.

![Major separator: the full dotted ground track of a balloon across the page with one gentle drift upward in the middle, slate on cloud cream](sep-heavy.svg)

## License
See LICENSE.
