from __future__ import print_function
import os, time
import cv2
import numpy as np
import urllib.request
from ipywidgets import Button, Box, Text, IntSlider, VBox, Label, Layout, Tab
from PIL import ImageFont, ImageDraw, Image

folderText = Text(value = 'images')
intervalSlider = IntSlider(value = 0, min = 1, max = 60, step = 1)
totalTimeSlider = IntSlider(value = 0, min = 1, max = 120, step = 1)
downloadBtn = Button(description = 'Download')

def download_btn_clicked(a):
    rootfolder = folderText.value
    interval = intervalSlider.value
    totalTime = totalTimeSlider.value
    
    if not os.path.exists(rootfolder):
        os.makedirs(rootfolder)
    
    for gap in range (int(totalTime*60/interval)):
        process("http://108.49.186.55/jpg/1/image.jpg", rootfolder, "first")
        process("http://108.49.186.56/jpg/1/image.jpg", rootfolder, "second")
        time.sleep(interval*60)
    
downloadBtn.on_click(download_btn_clicked)    
  
def process(imageurl, folder, name):
    if not os.path.exists(folder + '/' + name):
        os.makedirs(folder + '/' + name)
        
    try:
        data = urllib.request.urlopen(imageurl).read()
        imageName = 'boston_' + name + '_' + time.strftime("%b-%d-%Y-%H-%M-%S") + '.jpg'
        filepath = os.path.join(folder + '/' + name + '/' + imageName)
        image = open(filepath, 'wb')
        image.write(data)
        image.close()
        
        # add timestamp to images
        font = ImageFont.truetype("Roboto-Regular.ttf", 50)
        img = cv2.imread(filepath)
        height, width, c = img.shape
        pos = (80, height-80)
        cv2_im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        draw = ImageDraw.Draw(pil_im)
        draw.text(pos, imageName[-24:-4], font = font)
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        cv2.imwrite(filepath, cv2_im_processed)
        
        print ("Successfully download " + imageName)
        
        
    except Exception as ex_results:
        print ('Error: ', ex_results)
        
    pass

tab0_items = [
    Box([Label(value = "Saving Image Folder:", layout = Layout(width = '200px')), folderText]),
    Box([Label(value = "Downloading Interval (min):", layout = Layout(width = '200px')), intervalSlider]),
    Box([Label(value = "Downloading Time (hr):", layout = Layout(width = '200px')), totalTimeSlider]),
    Box([downloadBtn])
]
tab0Box = VBox(tab0_items)


imgsDicText = Text()
videoNameText = Text(value = 'output')
fpsSlider = IntSlider(value = 10, min = 10, max = 120, step = 10)
cvtBtn = Button(description = 'Convert')


def imgCvtVideo(img_dir,fps):
    images = []
    for img in os.listdir(img_dir):
        if img.endswith('.jpg'):
            images.append(img)
    images.sort()
    img_path = os.path.join(img_dir, images[0])
    frame = cv2.imread(img_path)
    height, width, channels = frame.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(videoNameText.value + '.mp4', fourcc, fps, (width, height))
    for img in images:
        img_path = os.path.join(img_dir, img)
        frame = cv2.imread(img_path)
        out.write(frame)
    
    out.release()
    
def convert_btn_clicked(a):
    try:
        imgCvtVideo(imgsDicText.value, fpsSlider.value)
        print ("Successfully convert images to " + videoNameText.value + '.mp4')
    
    except Exception as ex_results:
        print ('Error: ', ex_results)
    
cvtBtn.on_click(convert_btn_clicked)


    
tab1_items = [
    Box([Label(value = "Images Folder:", layout = Layout(width = '200px')), imgsDicText]),
    Box([Label(value = "Video Name:", layout = Layout(width = '200px')), videoNameText]),
    Box([Label(value = "Frames Per Second:", layout = Layout(width = '200px')), fpsSlider]),
    Box([cvtBtn])
]
tab1Box = VBox(tab1_items)





tab_nest = Tab()
tab_nest.children = [tab0Box, tab1Box]
tab_nest.set_title(0, 'Download')
tab_nest.set_title(1, 'ImgCvtVideo')

display(tab_nest)
    
    
