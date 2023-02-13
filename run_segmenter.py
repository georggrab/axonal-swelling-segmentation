import argparse
from pathlib import Path
import logging

import torch
import numpy as np
import pretrained_microscopy_models as pmm
from PIL import Image
from tqdm import tqdm
import tifffile

from logger import setup_logging

log = logging.getLogger(__name__)

def segment_images(model_path, input_path, output_path, device):
    model, preprocessing_fn = pmm.segmentation_training.load_segmentation_model(model_path, classes=1)
    model = model.to(device)
    
    img = Image.open(input_path)
    log.info("Starting segmentation of %s consisting of %d frames", input_path, img.n_frames)
    
    out = np.zeros((img.n_frames, 512, 512), dtype=np.float16)
    for i in tqdm(range(img.n_frames), total=img.n_frames):
        img.seek(i)
        img.resize((512, 512))
        img_arr = np.array(img)
        test_im_arr_prep = preprocessing_fn(img_arr)
        t = torch.tensor(test_im_arr_prep).unsqueeze(0).transpose(1,3).to(device, torch.float32)

        res = model(t.to(device))
        res_np = res.squeeze().cpu().detach().numpy().transpose()
        out[i, :, :] = res_np
    tifffile.imsave(output_path, out, compress=1)
    log.info("Saved %s", output_path)

if __name__ == '__main__':
    setup_logging("run_segmenter")

    parser = argparse.ArgumentParser(description='Segment a microscopy TIF image using a specified model.')
    parser.add_argument('--model', type=str, help='Path to the segmenter model.', default='output_models/model_best.pth.tar')
    parser.add_argument('--input', type=str, help='Path to the microscopy TIF image.', required=True)
    parser.add_argument('--output', type=str, help='Path to the output segmentation.', required=True)
    
    args = parser.parse_args()
    
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    log.info("Using device %s", device)

    segment_images(args.model, args.input, args.output, device)