# zheight
A utility for displaying a 2D contour map of the z-height of a tissue cut

## Installation

Install Python 3

Install zheight in its virtual environment (only needs to be done once)
("/path/to" below can be any directory)
```
python -m venv /path/to/zheight 
pip3 install https://github.com/chunglabmit/zheight/archive/master.zip#egg=zheight
```

Activate the environment
```
source /path/to/zheight/bin/activate
```

## Usage

Example:
```
zheight --stack /path/to/stack/*.tif --output /path/to/output.png
```

```
zheight --stack <stack> \
        --output <image-file> \
        [--sigma <sigma>] \
        [--multiplier <multiplier>] \
        [--min-threshold <min-threshold>]
```
where

* **\<stack\>** is the glob expression for the stack of tif files to be analyzed.
            These should be in alphabetical order by z-height, e.g.
            "img0001.tif" instead of "img0.tif".
* **\<output\>** the name of the output image. Supported types are probably .png, .jpg and maybe .pdf
* **\<sigma\>** the smoothing sigma for blurring the image. The default is 20,
            numbers between 10 and 40 should be pretty good choices.
* **\<multiplier\>** after computing the otsu automatic global threshold, zheight
            multiplies the automatic threshold by this factor to get the
            threshold used by the algorithm. The default is .8 which was
            arrived at empirically.
 * **\<min-threshold\>** is a minimum threshold that is used if the method above
            calculates a threshold that is too low.
