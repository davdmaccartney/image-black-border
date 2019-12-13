# import the necessary packages
from imutils import paths
import os
import gc
import numpy as np
from osgeo import gdal
import easygui
import fnmatch
import sys



def cls():
    os.system('cls' if os.name=='nt' else 'clear')



def update_progress(progress):
    barLength = 30 # Modify this to change the length of the progress bar
    
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% ".format( "#"*block + "-"*(barLength-block), int(progress*100))
    sys.stdout.write(text)
    sys.stdout.flush()


dirname = easygui.diropenbox(msg=None, title="Please select a directory", default=None)
total_con=len(fnmatch.filter(os.listdir(dirname), '*.tif'))
msg = str(total_con) +" files do you want to continue?"
title = "Please Confirm"
if easygui.ynbox(msg, title, ('Yes', 'No')): # show a Continue/Cancel dialog
    pass # user chose Continue else: # user chose Cancel
else:
    exit(0)

file_Dir = os.path.basename(dirname)
f = open(dirname+"/"+file_Dir+"-result-border.txt", "w")
i=0

cls()
# loop over the input images


for imagePath in paths.list_images(dirname):
 i = i+1
 image = gdal.Open(imagePath, gdal.GA_ReadOnly)
 xwidth=(image.RasterXSize)
 yheight=(image.RasterYSize)

 a_image = image.ReadAsArray()
 image = None
 if a_image.dtype == np.uint16:
    a_image = ( a_image/256).astype('uint8')
 
 s_image = np.dstack((a_image[0],a_image[1],a_image[2]))
 a_image = None

 rgb=[0,0,0]

 rgb[0] = int(s_image[0, 0, 0])
 rgb[1] = int(s_image[0, 0, 1])
 rgb[2] = int(s_image[0, 0, 2])

 colorHG = rgb[0]+rgb[1]+rgb[2]

 rgb[0] = int(s_image[xwidth-1, 0, 0])
 rgb[1] = int(s_image[xwidth-1, 0, 1])
 rgb[2] = int(s_image[xwidth-1, 0, 2])

 colorHD = rgb[0]+rgb[1]+rgb[2]


 rgb[0] = int(s_image[xwidth-1, yheight-1, 0])
 rgb[1] = int(s_image[xwidth-1, yheight-1, 1])
 rgb[2] = int(s_image[xwidth-1, yheight-1, 2])


 colorBD = rgb[0]+rgb[1]+rgb[2]


 rgb[0] = int(s_image[0, yheight-1, 0])
 rgb[1] = int(s_image[0, yheight-1, 1])
 rgb[2] = int(s_image[0, yheight-1, 2])

 colorBG = rgb[0]+rgb[1]+rgb[2]

 s_image = None

 if (colorHG == 0 or colorHD == 0 or colorBD == 0 or colorBG == 0):
      f.write(os.path.splitext(os.path.basename(imagePath))[0] + '.tif\n')
      f.flush

 
 update_progress(i/total_con)
f.close()
print('Done')

