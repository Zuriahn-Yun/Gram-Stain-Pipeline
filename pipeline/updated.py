import numpy as np
import pandas as pd
from PIL import Image
import os
import re
import matplotlib.pyplot as plt
import plotly
import webcolors 

def get_rgb(file_path):
    
    """ Convert Image to RGB -> DataFrame """
    image = Image.open(file_path)
    image_array = np.array(image)
    image_array.reshape(-1,3)
    df = pd.DataFrame(image_array)
    
    """ Name Columns """
    df.Columns =["Red","Green","Blue"]
    return df

output = get_rgb("pipeline/test.jpg")
print(output)
