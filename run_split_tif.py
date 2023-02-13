import argparse
from pathlib import Path

from PIL import Image

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='The input .tif file to split')
    parser.add_argument('--output', help='Output directory', default='output_split')


    args = parser.parse_args()
    
    path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    im = Image.open(path)
    for i in range(im.n_frames):
        im.seek(i)
        output_path = f"{args.output}/{path.stem}_{i}{path.suffix}"
        print(output_path)
        im.save(output_path)
