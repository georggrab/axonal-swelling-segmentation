import torch
import albumentations as albu
import pretrained_microscopy_models as pmm


def get_training_augmentation():
    train_transform = [
        albu.Flip(p=0.75),
        albu.RandomRotate90(p=1),       
        albu.GaussNoise(p=0.5),
        
        albu.OneOf(
            [
                albu.CLAHE(p=1),
                albu.RandomBrightness(p=1, limit=0.25),
                albu.RandomGamma(p=1),
            ],
            p=0.50,
        ),

        albu.OneOf(
            [
                albu.Sharpen(p=1),
                albu.Blur(blur_limit=3, p=1),
                #albu.MotionBlur(blur_limit=3, p=1),
            ],
            p=0.50,
        ),

        albu.OneOf(
            [
                albu.RandomContrast(p=1, limit=0.3),
                albu.HueSaturationValue(p=1),
            ],
            p=0.50,
        ),
    ]
    return albu.Compose(train_transform)

def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')


def get_preprocessing(preprocessing_fn):
    """Construct preprocessing transform
    
    Args:
        preprocessing_fn (callbale): data normalization function 
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose
    
    """
    
    _transform = [
        albu.Lambda(image=preprocessing_fn),
        albu.Lambda(image=to_tensor, mask=to_tensor),
    ]
    return albu.Compose(_transform)


def get_model(
  architecture: str,
  encoder: str,
  pretrained_weights: str,
  device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
):

    model = pmm.segmentation_training.create_segmentation_model(
        architecture=architecture,
        encoder = encoder,
        encoder_weights=pretrained_weights, # use encoder pre-trained on micronet
        classes=1 # Indicate Binary Classification task.
        )
    return model