Axonal Swelling Segmentation
============================

Source Code Repository for Axonal Swelling Segmentation.

* Preprocessing ImageJ Macro (Maximum Intensity Projection etc): `preprocess.ijm`

The analysis pipeline works as follows:

1. The images are preprocessed using `preprocess.ijm` and then saved as `.tiff` stacks
2. Using `run_split_tif.py` The images are split from stack into individual files
3. A couple of these files are then manually segmented using ImageJ (or similar tool), such that background is black and axonal swellings are assigned (255, 255, 255) colors. These files are then saved as `..._mask.tif` and form the training set.
4. `run_train.py` is being run that loads the pretrained microscopy model and fine tunes using transfer learning according to the training set defined in step 3.
5. After training, `run_segmenter.py` can be used for segmentation - it outputs a `.tif` in identical dimensions to the input image, and individual pixel intensities are probability values that the given pixel belongs to an axonal swelling.

The output of this pipeline is the probability map - this can be further processed using `ilastik` or similar tools in a tracking workflow.
