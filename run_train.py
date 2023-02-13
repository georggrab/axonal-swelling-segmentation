import sklearn.model_selection
import argparse
from pathlib import Path
import logging

import pretrained_microscopy_models as pmm
import segmentation_models_pytorch as smp

from train import get_model, get_training_augmentation, get_preprocessing
from data import get_dataset
from logger import setup_logging
from visualize import plot_training_curve

log = logging.getLogger(__name__)

architecture = 'UnetPlusPlus'
encoder = 'resnet50'
pretrained_weights = 'micronet'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', help='Output folder (Model Checkpoint, Graphs, etc.)', default='output_train')
    parser.add_argument('--input', help='input directory containing training data (xyz.tif and xyz_mask.tif combination)', default='output_split')
    
    args = parser.parse_args()
    
    setup_logging("run_train")
    
    # Get Data
    dataset = get_dataset(args.input)
    images = list(map(lambda f: str(f[0]), dataset))
    masks = list(map(lambda f: str(f[1]), dataset))
    classes = {
        'swelling': [255,255,255]
    }
    images_train, images_val, masks_train, masks_val = sklearn.model_selection.train_test_split(images, masks, test_size=0.3)
    
    log.info("Gathered test data: #train: %d, #val: %d", len(images_train), len(images_val))
    
    model = get_model(architecture, encoder, pretrained_weights)
    
    fn = smp.encoders.get_preprocessing_fn(encoder, 'imagenet') 

    ds_train = pmm.io.Dataset(
        images=images_train,
        masks=masks_train,
        class_values=classes,
        augmentation=get_training_augmentation(),
        preprocessing=get_preprocessing(fn)
    )
    ds_val = pmm.io.Dataset(
        images=images_val,
        masks=masks_val,
        class_values=classes,
        preprocessing=get_preprocessing(fn)
    )
    
    state = pmm.segmentation_training.train_segmentation_model(
        model=model,
        architecture=architecture,
        encoder=encoder,
        train_dataset=ds_train,
        validation_dataset=ds_val,
        class_values=[255,255,255],
        patience=30,
        lr=2e-4,
        batch_size=6,
        val_batch_size=6,
        save_folder=args.output,
        save_name='SwelSegm_UnetPlusPlus_resnet50.pth.tar'
    )
    
    plot_training_curve(state, Path(args.output) / "train_loss.pdf")