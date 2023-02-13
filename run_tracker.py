mport tifffile

THRESHOLDS = [10, 50, 80 100]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='input tif)', required=True)
    
    args = parser.parse_args()
    
    arr = tifffile.imread(args.input)
    