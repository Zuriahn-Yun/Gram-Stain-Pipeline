import numpy as np
import pandas as pd
from PIL import Image
import os
import re
import matplotlib.pyplot as plt

def image_to_df(image):
  """Return image reshaped as an ndarray"""
  imageArray = np.array(image)
  reshaped = imageArray.reshape(-1,3)
  return reshaped
def percent(value,total):
  """ return the percent of the value with a base of the total"""
  return (value / total) * 100
def darkness_luminosity(row):
  """ Using the NTSC formula to convert RGB values into Grayscale, this formula closely represents the average persons relative perception of brighness in red,green and blue light. Smaller values represent darker pixels.

  Args:
      row (int): a row from an image dataframe and contains red,green and blue columns
  Returns:
      int : darkness value
  """
  return (0.299 * row['Red'] + 0.587 * row['Green'] + 0.114 * row['Blue'])
def saveTifftoJPG(base_path):
  """ Turn a tiff to a jpg, using the same path name but replacing the tiff with a jpg and using some image conversion

  Args:
      base_path (file_path):  saves the image as a jpg at the same file_path
  """
  tiff_image = Image.open(base_path)
  new_path = base_path[:-3] + "jpg"
  jpge_image = tiff_image.convert("RGB")
  jpge_image.save(new_path)
def convertTifftoJPG(base_path):
  """ Convert Tiff to JPG and return it

  Args:
      base_path (file_path): relative path of the tiff file 

  Returns:
      Image : returns image as a JPG directly does not save it
  """
  tiff_image = Image.open(base_path)
  new_path = base_path[:-3] + "jpg"
  jpgImage = tiff_image.convert("RGB")
  return jpgImage

def PositiveNegativePercentages(ImageDataFrame):
  """Calculating the positive negative and white percentages for a single ImageDataframe, this edits the datafrme to contain the number of pixels that are between the thresholds. These thresholds can be changed. Also a threshold for balck pixels should be added.
  
  Args:
      ImageDataFrame (DataFrame): Image in Dataframe form
  """
  white_threshold = 225
  gram_positive_threshold = 35
  white = (ImageDataFrame['Darkness'] > white_threshold).sum()
  gram_positive = (ImageDataFrame['Darkness'] < gram_positive_threshold).sum()
  gram_negative = ((gram_positive_threshold < ImageDataFrame['Darkness']) & (ImageDataFrame['Darkness'] < white_threshold)).sum()
def printPercents(ImageDataFrame,white,gram_positive,gram_negative):
    """ Print the Percents of white,gram_positive and gram_negative in a given image

    Args:
        ImageDataFrame (_npArray_): Image as a number Dataframe
        white (_int_): # of white pixels
        gram_positive (_int_): # of positive classified pixels
        gram_negative (_int_): # of negative classified pixels
    """
    print('Percent of White ' + str(percent(white,len(ImageDataFrame))) + '%')
    print('Percent of gram positive ' + str(percent(gram_positive ,len(ImageDataFrame)))+ '%')
    print('Percent of gram negative ' + str(percent(gram_negative, len(ImageDataFrame)))+ '%')
  
def extract_numbers(file_name):
    """ Extract the numbers from a file name 

    Args:
        file_name (text): Local file path 

    Returns:
        _type_: the numbers in the filename
    """
    numbers_str = re.findall(r'\d+', file_name)
    numbers_int = [int(num) for num in numbers_str]
    return numbers_int


def image_to_df(image):
    """ Turn an image into a dataframe containing a darkness column
    
    Args:
        image (_jpg_): Image FilePath

    Returns:
        _DataFrame_: Image -> DataFrame while adding Darkness Column
    """
    imageArray = np.array(image)
    reshaped = imageArray.reshape(-1, 3)
    df = pd.DataFrame(reshaped, columns=["Red", "Green", "Blue"])
    df["Darkness"] = df.apply(darkness_luminosity, axis=1)
    return df

def get_mouse_summary_df(mouse_name, folderPath):
    miceNames = ["mouse1"]
    white_threshold = 225
    gram_positive_threshold = 35
    listofDays = miceNames.get(mouse_name)
    if not listofDays:
        print(f"No data for mouse: {mouse_name}")
        return None

    # For each day, calculate percentages and store in a list
    results = []

    for day_index in range(len(listofDays)):
        image_files = listofDays[day_index]
        if len(image_files) == 0:
            continue

        # Combine all image data from this day into one big DataFrame
        day_df = pd.DataFrame()

        for filename in image_files:
            full_path = os.path.join(folderPath, filename)

            if filename.lower().endswith(("tif", "tiff")):
                image = convertTifftoJPG(full_path)
            else:
                image = Image.open(full_path)

            single_image_df = image_to_df(image)
            day_df = pd.concat([day_df, single_image_df], ignore_index=True)

        # Calculate percentages
        total_pixels = len(day_df)
        white_pixels = (day_df['Darkness'] > white_threshold).sum()
        gram_pos = (day_df['Darkness'] < gram_positive_threshold).sum()
        gram_neg = ((day_df['Darkness'] >= gram_positive_threshold) & (day_df['Darkness'] <= white_threshold)).sum()

        results.append({
            "Day": day_index + 1,
            "Percent White": percent(white_pixels, total_pixels),
            "Percent Gram Positive": percent(gram_pos, total_pixels),
            "Percent Gram Negative": percent(gram_neg, total_pixels)
        })

    df = pd.DataFrame(results)
    df.to_csv(mouse_name, index=False)
    return df

""" Everything Below was Case Specific for Cohort 1"""
# Path to Kaplan Lab HDD
# "D:" Goes to the HDD, After that inset file name
# folderPath = ""

# Hashmap to Hold all of the Dataframes for each mouse and day
# miceNames = {}

# Iterate through files in folder Path
# for filename in os.listdir(folderPath):
#     fileTypeTag = str(filename[-3:]).strip()
#     nameSplit = filename.split("_")
#     dayNumber = extract_numbers(nameSplit[0])[0]
#     imageNumber = nameSplit[1]
#     name = nameSplit[2]
#     fileTypeTag = str(filename[-3:]).strip()
    
#     # Counting the Number of Photos 
#     if name in miceNames:
#         currLists = miceNames[name]
        
#         thislist = currLists[dayNumber - 1]
#         thislist.append(filename)
#     else:
#         miceNames[name] = days = [[] for _ in range(15)]
#         currLists = miceNames[name]
        
#         thislist = currLists[dayNumber - 1]
#         thislist.append(filename)