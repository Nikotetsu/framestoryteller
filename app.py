import streamlit as st
import numpy as np
import cv2
import os
import random

from gradio_client import Client

st.title('Take a story from a random videoframe!')
uploaded_file = st.file_uploader("Choose a video", ["mp4","mov","avi"]) #videouploader

temp_file_to_save = './temp_file.mp4'
temp_frame = 'random_frame.jpg'

if os.path.exists(temp_file_to_save):
    os.remove(temp_file_to_save)
if os.path.exists(temp_frame):
    os.remove(temp_frame)

def write_bytesio_to_file(filename, bytesio):
    with open(filename, "wb") as outfile:
        outfile.write(bytesio.getbuffer())

if uploaded_file is not None:
    write_bytesio_to_file(temp_file_to_save, uploaded_file)
    vidcap =  cv2.VideoCapture(temp_file_to_save)
    totalFrames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    #st.text(str(totalFrames))
    randomFrameNumber=random.randint(0, totalFrames)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(temp_frame, image)
    st.write('This is a random frame from your video')
    st.image(temp_frame)

    vidcap.release()

    client = Client("https://tonyassi-image-story-teller.hf.space/--replicas/liw84/")
    result = client.predict(temp_frame, api_name="/predict")
    st.write(result)
  
if os.path.exists(temp_file_to_save):
    os.remove(temp_file_to_save)
if os.path.exists(temp_frame):
    os.remove(temp_frame)
