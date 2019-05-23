import cv2
import numpy as np
import os

from os.path import isfile, join


def sort_fun(list_data):
   li_data = []
   for i in list_data:
       z = i.split(".")
       li_data.append(int(z[0]))
   # print(li_data)
   sort_list = sorted(li_data)
   # print(sort_list)
   final_list = []
   for i in range(len(list_data)):
       final_list.append(list_data[li_data.index(sort_list[i])])
   return final_list

def convert_frames_to_video(pathIn,pathOut,fps):
   frame_array = []
   files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
   
   files = sort_fun(files)
   for i in range(len(files)):
       filename=pathIn + files[i]
       #reading each files
       img = cv2.imread(filename)
       height, width, layers = img.shape
       print(img.shape)
       size = (width,height)
       # print(filename)
       #inserting the frames into an image array
       frame_array.append(img)
       print("processed files", i)

   # out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
   out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

   for i in range(len(frame_array)):
       # writing to a image array
       out.write(frame_array[i])
   out.release()
   return "success"

def save_video(pathIn, pathOut, fps):

  convert_frames_to_video(pathIn, pathOut, fps)



pathIn = "15/"
pathOut = "video/15.avi"
fps = 32

save_video(pathIn, pathOut, fps)

