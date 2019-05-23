from statistics import mode
import imutils
import cv2
import numpy as np
from imutils.video import VideoStream
import time
import os
from preprocessor import preprocess_input

import pickle as pkl

# Support functions

def get_labels(dataset_name):
    if dataset_name == 'KDEF':
        return {0: 'AN', 1: 'DI', 2: 'AF', 3: 'HA', 4: 'SA', 5: 'SU', 6: 'NE'}
    else:
        raise Exception('Invalid dataset name')


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
    count = 0
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


def draw_text(coordinates, image_array, text, color, x_offset=0, y_offset=0,
                                                font_scale=2, thickness=2):
    x, y = coordinates[:2]
    cv2.putText(image_array, text, (x + x_offset, y + y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA)


def draw_bounding_box(face_coordinates, image_array, color, identity):
    x, y, w, h = face_coordinates
    cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)
    cv2.putText(image_array, str(identity), (x+5,y-5), font, 1, (255,255,255), 2)


def apply_offsets(face_coordinates, offsets):
    x, y, width, height = face_coordinates
    x_off, y_off = offsets
    return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)


def load_detection_model(prototxt, weights):
    detection_model = cv2.dnn.readNetFromCaffe(prototxt, weights)
    return detection_model

font = cv2.FONT_HERSHEY_SIMPLEX

frame_window = 10
face_offsets = (30, 40)
emotion_offsets = (20, 40)
confidence = 0.6

# face_detection_size = (40, 40)
counter = 0
# frame_process_counter = 0

def crop_face(file_name, face_detection, dirName):
    dire = "cropped_faces/" + dirName
    try:
        os.makedirs(dire)    
        print("Directory " , dire  ,  " Created ")
    except FileExistsError:
        print("Directory " , dire ,  " already exists")  


    face_detection_size = (40, 40)
    counter = 0
    frame_process_counter = 0

    # starting video streaming
    cv2.namedWindow('Attendence_Tracker', cv2.WINDOW_NORMAL)
    # cv2.namedWindow('Attendence_Tracker')
    # file_name = '../top10/person1.mp4'
    video_capture = cv2.VideoCapture(file_name)

    time.sleep(1.0)

    while (video_capture.isOpened()):
        ret, bgr_image = video_capture.read()
        if ret == False:
            break
        counter += 1
        if counter % 1 == 0:
            frame_process_counter += 1
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            faces = detect_faces(face_detection, bgr_image,confidence)
            count = 0
            for face_coordinates in faces:
                x1, x2, y1, y2 = apply_offsets(face_coordinates, face_offsets)
                rgb_face = rgb_image[y1:y2, x1:x2]
        
                print("len", len(rgb_face))
                # print(rgb_face)
                if len(rgb_face) != 0 and counter % 1 ==0:
                    cv2.imwrite(dire +"/"+dirName+"_{}".format(counter) + ".jpg", cv2.cvtColor(rgb_face, cv2.COLOR_RGB2BGR))
                    print("image saved-------------------", counter)              
                count += 1
                try:
                    rgb_face = cv2.resize(rgb_face, (face_detection_size))
                except:
                    continue
                rgb_face = np.expand_dims(rgb_face, 0)
                rgb_face = preprocess_input(rgb_face, False)

                # Bounding box color            
                color = (255, 0, 0)
                identity = "this is me"
                draw_bounding_box(face_coordinates, rgb_image, color, identity)
            bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            cv2.imshow('Attendence_Tracker', bgr_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Total frames processed:', counter, frame_process_counter)
            break
    video_capture.release()
    # out.release()
    cv2.destroyAllWindows()

    return "successful"


