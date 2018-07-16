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
parser.add_argument('--config', required=True , help='Path to .pbtxt file.')
parser.add_argument('--input', help='Path to images folder.')
parser.add_argument('--threshold', default=0.5, type=float, help='Threshold for confidence of detection.')
parser.add_argument('--classes', default="coco_class_labels.txt", help='Path to COCO class labels.')

args = parser.parse_args()


modelFile = args.model
configFile = args.config
threshold = args.threshold
classFile = args.classes

with open(classFile) as fi:
    labels = fi.readline().strip().split()

net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

winName = "OpenCV Tensorflow Object Detection"
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(args.input if args.input else 0)

while(1):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (300, 300))
    rows = frame.shape[0]
    cols = frame.shape[1]

    net.setInput(cv2.dnn.blobFromImage(frame, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), True))
    out = net.forward()

    for i in range(out.shape[2]):
        score = float(out[0, 0, i, 2])
        classId = int(out[0, 0, i, 1])

        x = int(out[0, 0, i, 3] * cols)
        y = int(out[0, 0, i, 4] * rows)
        w = int(out[0, 0, i, 5] * cols - x)
        h = int(out[0, 0, i, 6] * rows - y)

        if score > threshold:
            cv2.putText(frame, "{}".format(labels[classId]), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), cv2.FONT_HERSHEY_DUPLEX)
        

    cv2.imshow(winName, frame)
    k = cv2.waitKey(10)
    if k == 27 :
        break

cv2.destroyAllWindows()
