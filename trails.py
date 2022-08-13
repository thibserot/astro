import os, numpy, glob
import subprocess
import argparse
from PIL import Image


class Trail:
    def __init__(self, paths, extension_filters, output_path, output_prefix, reverse, max_images):
        self.images = []
        for path in paths:
            if os.path.isdir(path):
                path = os.path.join(path, "*")
            self.images.extend(glob.glob(path))
        if extension_filters:
            self.images = [image for image in self.images if os.path.splitext(image)[1].lower()[1:] in extension_filters]
        self.images = sorted(self.images)
        if max_images > 0 and max_images <= len(self.images):
            print(f"Keeping only the first {max_images} images")
            self.images = self.images[0:max_images]
        if reverse:
            self.images = self.images[::-1]
        if output_path:
            os.makedirs(output_path, exist_ok=True)
        else:
            output_path = os.getcwd()
        self.output_path = output_path
        self.output_prefix = output_prefix

    def process(self, skip, keep_intermediate, keep_timelapse, save_video):
        width, height = Image.open(self.images[0]).size
        stack   = numpy.zeros((height, width, 3), float)
        offset = 0
        if save_video:
            keep_intermediate = True
        if keep_timelapse and keep_intermediate:
            for counter, image in enumerate(self.images[::-1]):
                print(f"Processing timelapse image {counter}/{len(self.images)} : {image}")
                image_new = numpy.array(Image.open(image), dtype = float)
                self.save_image(image_new, f"{counter:05}")
            offset = len(self.images)

        for counter, image in enumerate(self.images):
            print(f"Processing image {counter}/{len(self.images)} : {image}")
            if skip != 0 and counter % skip != 0:
                print("   Skipping...")
                continue
            image_new = numpy.array(Image.open(image), dtype = float)
            stack     = numpy.maximum(stack, image_new)
            if keep_intermediate:
                self.save_image(stack, f"{offset+counter:05}")
        self.save_image(stack, "final")
        if save_video:
            # Generate 3 seconds of static image at the end
            print("Generating static image for the video")
            offset += len(self.images)
            for counter in range(0, 90):
                self.save_image(stack, f"{offset+counter:05}")
            self.save_video()

    def save_video(self):
        print("Generating the video using ffmpeg")
        cmd = [
            "ffmpeg",
            "-y",
            "-framerate", "30",
            "-i", os.path.join(self.output_path, f"{self.output_prefix}_%05d.jpg"),
            "-s", "hd1080",
            "-c:v",
            "libx264",
            "-pix_fmt", "yuvj420p",
            os.path.join(self.output_path, f"{self.output_prefix}_final.mp4")
        ]
        print(" ".join(cmd))
        rc = subprocess.call(cmd)
        if rc != 0:
            print("An error occured while saving the video")

    def save_image(self, stack, output_suffix):
        stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)
        output = Image.fromarray(stack, mode = "RGB")
        filename = os.path.join(self.output_path, f"{self.output_prefix}_{output_suffix}.jpg")
        output.save(filename, "JPEG")

def main():
    parser = argparse.ArgumentParser(description='Generate Star Trails images')
    parser.add_argument('paths', metavar='N', nargs='+',
                    help='List of files / path to process')
    parser.add_argument('-e', '--extensions', help='Keep only files matching this extension', action="append")
    parser.add_argument('-s', '--skip', type=int, help='Only keep every N images', default=0)
    parser.add_argument('-k', '--keep-intermediate', help='Keep each intermediate picture', action="store_true")
    parser.add_argument('-r', '--reverse', help='Process files in reverse order', action="store_true")
    parser.add_argument('-kt', '--keep-timelapse', help='Store timelapse before star trails for intermediate images', action="store_true")
    parser.add_argument('-sv', '--save-video', help='Use ffmpeg to generate a finale video', action="store_true")
    parser.add_argument('-o', '--output', help='Where to store the result')
    parser.add_argument('-m', '--max-images', type=int, help='Only process the first N images', default=0)
    parser.add_argument('-op', '--output-prefix', help='Prefix for the final image', default="trails")

    args = parser.parse_args()
    print(args)
    trails = Trail(args.paths, args.extensions, args.output, args.output_prefix, args.reverse, args.max_images)
    trails.process(args.skip, args.keep_intermediate, args.keep_timelapse, args.save_video)

if __name__ == "__main__":
    main()
