import imutils
import cv2
from keras.models import load_model
import numpy as np
from imutils.video import VideoStream
import time

def get_labels(dataset_name):
    if dataset_name == 'fer2013':
        return {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
                4: 'sad', 5: 'surprise', 6: 'neutral'}
    elif dataset_name == 'imdb':
        return {0: 'woman', 1: 'man'}
    elif dataset_name == 'KDEF':
        return {0: 'AN', 1: 'DI', 2: 'AF', 3: 'HA', 4: 'SA', 5: 'SU', 6: 'NE'}
    else:
        raise Exception('Invalid dataset name')



def draw_text(coordinates, image_array, text, color, x_offset=0, y_offset=0,
                                                font_scale=2, thickness=2):
    x, y = coordinates[:2]
    cv2.putText(image_array, text, (x + x_offset, y + y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA)


def draw_bounding_box(face_coordinates, image_array, color):
    x, y, w, h = face_coordinates
    cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)


def apply_offsets(face_coordinates, offsets):
    x, y, width, height = face_coordinates
    x_off, y_off = offsets
    return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)


def load_detection_model(prototxt, weights):
    detection_model = cv2.dnn.readNetFromCaffe(prototxt, weights)
    return detection_model



def detect_faces(detection_model, gray_image_array, conf):
    frame = gray_image_array
    # Grab frame dimention and convert to blob
    (h,w) =  frame.shape[:2]
    # Preprocess input image: mean subtraction, normalization
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
    (300, 300), (104.0, 177.0, 123.0))
    # Set read image as input to model
    detection_model.setInput(blob)

    # Run forward pass on model. Receive output of shape (1,1,no_of_predictions, 7)
    predictions = detection_model.forward()
    coord_list = []
    for i in range(0, predictions.shape[2]):
        confidence = predictions[0,0,i,2]
        if confidence > conf:
            # Find box coordinates rescaled to original image
            box_coord = predictions[0,0,i,3:7] * np.array([w,h,w,h])
            conf_text = '{:.2f}'.format(confidence)
            # Find output coordinates
            xmin, ymin, xmax, ymax = box_coord.astype('int')
            coord_list.append([xmin, ymin, (xmax-xmin), (ymax-ymin)])
    print('Coordinate list:', coord_list)
    return coord_list