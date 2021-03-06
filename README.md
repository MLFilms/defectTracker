# Setup:
clone the repo
Create a new GPU-enabled tensorflow environment with "conda create --name ENVIRONMENT_NAME tensorflow-gpu"
activate the new environment
Use the command "pip install -r requirements.txt"
cd into the uppermost darkflow folder
run "setup.py build_ext --inplace"

go to 
https://drive.google.com/drive/folders/1c_xrWVKNBuqZUwXGvv_MBamOHNa1wBKy?usp=sharing
and download yolo.weights. Put the weights file in a bin folder in the main darkflow folder. The path to this file can be modified in config.json



# Tools for labeling:
BBox-Label-Tool allows you to draw bounding boxes on images
Place the images inside the BBox-Label-Tool folder inside Images\001 (or other folder)
Inside the main BBox-Label-Tool folder, run python main.py. Enter the folder number in the top and click load. Must use python 2
Draw boxes around the objects you want detected. Annotations will be output into AnnotationsXML
For converting files containing bounding box coordinates into properly formatted xml annotations, use the tools inside ImageAnnotation

# Using darkflow:
To facilitate training and running the model, several scripts have been included in the darkflow folder.

Modify the config.json file to change targets and options. 
## config.json summary

training_annotations- this should point to the folder containing your xml annotations for training a new model
training_images- the path to the images corresponding to the xml annotations for training
run_directory- directory containing images you would like to run detection on. Uses model specified by meta_file and pb_file
image_ext- the extension of the images you wish to use (for training or running)
meta_file - path to the .meta file for your trained model. Meta file is generated after training reaches its last epoch.
pb_file - path to the .pb file for your trained model. Meta file is generated after training reaches its last epoch.
validation_detection_path- path to the folder containing .json files generated when running a model on an image set.
validation_truth_path- path to the folder containing ground truth xml annotations
mAPPath- path to the mAP folder containing scripts necessary for validation

threshold- certainty threshold beneath which detections are thrown out. 0-1
learning_rate- metaparameter for model training. 1e-5 generally works. Raising trains the model faster but can make it less accurate. Lower values can slighly increase accuracy.
model- cfg file containing the network configuration. use cfg/yolo_custom2.cfg for single object detection
batch_size- number of images in a training batch. Bigger is generally better until you run out of memory
epoch- number of epochs in training. Each image gets used once per epoch.

starting_weights- file containing the starting weights to use when training a new model
gpu_usage- how much of the gpu to use when running or training the model
labels_file- file containing the labels you'd like to be detected
json- file specifying whether you'd like json files containing detections to be generated.


## Script Usage
There are four scripts in the main darkflow folder that are used for training, running, and validating a model.

trainFlow.py trains a new model from the starting weights based on the image and annotation paths. Batch size, epoch, and learning rate will affect this process. Make sure you have the proper image extension set. When the model is finished training, a .pb and a .meta file will be generated in the built_graph folder. You will generally want to move these to your bin folder.

trainFlowP.py is used to continue training a model from checkpoints. After every 250 steps of training checkpoint files will be generated in ckpt. If you want to continue training from these checkpoint files, run trainFlowP.py. You can lower the learning_rate to further refine a trained model.

runFlowPB.py is used to run a trained model stored in the .pb and .meta files. Make sure to change targets in the config file. You'll usually want to check meta_file, pb_file, and run_directory. The model will be run for all images in the target folder with the matching extension. An output folder will be created containing marked images and .json files with the detections.

validate.py is used to validate detections against ground-truth xml annotations. validation_detection_path should point to the folder generated by runFlowPB.py. validation_truth_path should point to a folder containing xml annotations in the same format as training annotations. It can be useful to validate a model using the training annotations as a first check to make sure the model was successfully trained, but to actually check the effectiveness of a model it should be validated on a set of data not used for training.

As a reminder, training requires an initial weights file. Download the yolo.weights file from https://drive.google.com/drive/folders/1c_xrWVKNBuqZUwXGvv_MBamOHNa1wBKy?usp=sharing
and put it in a bin folder in the darkflow folder. The google drive folder also contains several .pb and .meta files trained used in our lab.


## Other tools
Inside the matlab folder are scripts for generating training data containing circles. circlemaker.m generates a very noisy image with circles and circlemakerCLEAN.m generates
images with greatly reduced noise. 
The houghAnnotate scripts generate annotations using the circular hough transform. These are used for testing a ML pipeline and new features. A model trained on the circle annotations should be very effective.












