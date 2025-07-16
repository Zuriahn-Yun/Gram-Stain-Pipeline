import numpy as np
import pandas as pd
from PIL import Image
import os
import re
import matplotlib.pyplot as plt
import plotly
import webcolors 

def darkness_luminosity(row):
  """ Using the NTSC formula to convert RGB values into Grayscale, this formula closely represents the average persons relative perception of brighness in red,green and blue light. Smaller values represent darker pixels.

  Args:
      row (int): a row from an image dataframe and contains red,green and blue columns
  Returns:
      int : darkness value
  """
  return (0.299 * row['Red'] + 0.587 * row['Green'] + 0.114 * row['Blue'])

def get_color(row):
    """ Turn RGB from each row to string name """
    red = row['Red']
    green = row['Green']
    blue = row['Blue']
    rgb = (red,green,blue)  
    
    try:
        color = webcolors.rgb_to_name(rgb)  
    except ValueError as e:
        
        color = "Has no defined color name"
    return color

def get_rgb(file_path):
    
    """ Convert Image to RGB -> DataFrame """
    image = Image.open(file_path)
    image_array = np.array(image)
    
    """ Flatten the Array, new size is (1440 * 1920, 3) """
    pixels = image_array.reshape(-1,3)
    df = pd.DataFrame(pixels)
    
    """ Name Columns """
    df.columns =["Red","Green","Blue"]
    
    df['Color'] = df.apply(get_color,axis=1)
    return df    

# output = get_rgb("pipeline/test.jpg")
# print(output)

rgb = (38,19,41)
print(webcolors.rgb_to_name(rgb))

