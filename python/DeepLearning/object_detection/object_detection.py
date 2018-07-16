import os
import cv2
import argparse

'''
Model files can be downloaded from the Tensorflow Object Detection Model Zoo
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

Once you download the model, extract the files and run the tf_text_graph_ssd.py file 
with input as the path to the frozen_graph.pb file and output as desired.
The python file is available at https://github.com/opencv/opencv/blob/master/samples/dnn/tf_text_graph_ssd.py

Then pass these two files as model and config files to this code
'''
parser = argparse.ArgumentParser(description='Tensorflow Object Detection using OpenCV')
parser.add_argument('--model', required=True, help='Path to frozen_inference_graph.pb')
parser.add_argument('--config', help='Path to .pbtxt file.', required=True)
parser.add_argument('--input', default='images', help='Path to images folder.', required=True)
parser.add_argument('--threshold', default=0.5, type=float, help='Threshold for confidence of detection.')
parser.add_argument('--classes', default="coco_class_labels.txt", help='Path to COCO class labels.')

args = parser.parse_args()


modelFile = args.model
configFile = args.config
image_dir = args.input
threshold = args.threshold
classFile = args.classes

with open(classFile) as fi:
    labels = fi.read().split("\n")

# Read the Tensorflow network
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

# For ach file in the directory
for filename in os.listdir(image_dir):
    frame = cv2.imread(os.path.join(image_dir, filename))

    # Resize the image to the dimension required for SSD
    rows = frame.shape[0]
    cols = frame.shape[1]
    frameResized = cv2.resize(frame, (300, 300))


    # Create a blob from the image and pass it to the network
    net.setInput(cv2.dnn.blobFromImage(frameResized, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), True))
    
    # Peform Prediction
    out = net.forward()
    
    # For every Detected Object
    for i in range(out.shape[2]):
        # Find the class and confidence 
        classId = int(out[0, 0, i, 1])
        score = float(out[0, 0, i, 2])
        
        # The locations given are normalized. They should be multiplied by the height and width of the input
        x = int(out[0, 0, i, 3] * cols)
        y = int(out[0, 0, i, 4] * rows)
        w = int(out[0, 0, i, 5] * cols - x)
        h = int(out[0, 0, i, 6] * rows - y)
        
        # Check if the detection is of good quality
        if score > threshold:
            cv2.putText(frame, "{}".format(labels[classId]), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), cv2.FONT_HERSHEY_DUPLEX)


    cv2.imwrite('imout.jpg', frame)
    cv2.imshow("Tensoflow OpenCV Object Detection", frame)
    k = cv2.waitKey(0)
    if k == 27 :
        break

cv2.destroyAllWindows()
