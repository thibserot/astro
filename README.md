# Astro scripts


## Installation

* Create a virtualenv: 

```
mkvirtualenv --python=/usr/bin/python3 astro
```

* Install requirements:

```
pip install -r requirements.txt
```

## Trails.py 

Generate star trails image and video

```
python trails.py -h
usage: trails.py [-h] [-e EXTENSIONS] [-s SKIP] [-k] [-r] [-kt] [-sv] [-o OUTPUT] [-m MAX_IMAGES] [-op OUTPUT_PREFIX] N [N ...]

Generate Star Trails images

positional arguments:
  N                     List of files / path to process

options:
  -h, --help            show this help message and exit
  -e EXTENSIONS, --extensions EXTENSIONS
                        Keep only files matching this extension
  -s SKIP, --skip SKIP  Only keep every N images
  -k, --keep-intermediate
                        Keep each intermediate picture
  -r, --reverse         Process files in reverse order
  -kt, --keep-timelapse
                        Store timelapse before star trails for intermediate images
  -sv, --save-video     Use ffmpeg to generate a finale video
  -o OUTPUT, --output OUTPUT
                        Where to store the result
  -m MAX_IMAGES, --max-images MAX_IMAGES
                        Only process the first N images
  -op OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX
                        Prefix for the final image
```

Example:

```
python trails.py -e jpg -o final_cleaned_reversed_timelapse -k -r -kt -sv ../milkyway_timelapse
```
