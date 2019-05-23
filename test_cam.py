import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
detector = MTCNN()

filename = "video/video10.mp4"

# cv2.namedWindow('Attendence_Tracker', cv2.WINDOW_NORMAL)

# cap = cv2.VideoCapture(filename)
# # cap = cv2.VideoCapture(0)
# while True: 
#     #Capture frame-by-frame
#     __, frame = cap.read()
    
#     #Use MTCNN to detect faces
#     result = detector.detect_faces(frame)
#     if result != []:
#         for person in result:
#             bounding_box = person['box']
#             keypoints = person['keypoints']
    
#             cv2.rectangle(frame,
#                           (bounding_box[0], bounding_box[1]),
#                           (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
#                           (0,155,255),
#                           2)
    
#             cv2.circle(frame,(keypoints['left_eye']), 2, (0,155,255), 2)
#             cv2.circle(frame,(keypoints['right_eye']), 2, (0,155,255), 2)
#             cv2.circle(frame,(keypoints['nose']), 2, (0,155,255), 2)
#             cv2.circle(frame,(keypoints['mouth_left']), 2, (0,155,255), 2)
#             cv2.circle(frame,(keypoints['mouth_right']), 2, (0,155,255), 2)
#     #display resulting frame
#     cv2.imshow('Attendence_Tracker',frame)
#     if cv2.waitKey(1) &0xFF == ord('q'):
#         break
# #When everything's done, release capture
# cap.release()
# cv2.destroyAllWindows()

img = "align/3.jpg"

def adjust_gamma(image, gamma=1.5):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

image = cv2.imread(img)
img = adjust_gamma(image)
result = detector.detect_faces(image)

print(result)
