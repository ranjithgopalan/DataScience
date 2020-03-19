
from PIL import Image
from numpy import asarray
import numpy as np
import cv2
import glob, os


def fnConvertImagetoArry(size):

    for infile in glob.glob("Resources/Data/Input/*.jpeg"):
        # file, ext = os.path.splitext(infile)
        file_name = os.path.basename(infile)
        print(file_name)
        im = Image.open(infile)
        im = im.resize(size)
        # im.thumbnail(size)
        print(os.path.splitext(file_name)[0])
        print(os.path.splitext(file_name)[1])
        # print(im.size)
        # print(type(im.size))
        im.save("Resources/Data/Output/"+ os.path.splitext(file_name)[0]+"_Updated" + ".JPEG")
        data = asarray(im)
        with open("Resources/Data/Output/npArrays/"+ os.path.splitext(file_name)[0] + ".txt", 'w') as f:
            f.write(" ".join(map(str, np.array(data))))


    cv2.destroyAllWindows()
    f.close()
size = 400, 400
fnConvertImagetoArry(size)

