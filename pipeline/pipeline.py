import numpy as np
import pandas as pd
from PIL import Image
import os
import re
import matplotlib.pyplot as plt

# Turn image into a Dataframe, 
def image_to_df(image):
  # imageArray will have shape (height,width,3)
  imageArray = np.array(image)
  # reshaped size is (height * width, 3)
  reshaped = imageArray.reshape(-1,3)
  return reshaped

# Function to Calculate percentages
def percent(value,total):
  return (value / total) * 100

def darkness_luminosity(row):
        # This is the NTSC formula to convert RGB values into Grayscale
        # "This formula closely represents the average person's relative perception of the brightness of red, green and blue light."
        # The smaller the values the darker the pixel
       return (0.299 * row['Red'] + 0.587 * row['Green'] + 0.114 * row['Blue'])
    
# Tiff to JPG Function and save with same filename as given replaced with "jpg"
def saveTifftoJPG(base_path):
  tiff_image = Image.open(base_path)
  new_path = base_path[:-3] + "jpg"
  jpge_image = tiff_image.convert("RGB")
  jpge_image.save(new_path)


# TIff to Jpg, returns the JPG image but does not save it
def convertTifftoJPG(base_path):
  tiff_image = Image.open(base_path)
  new_path = base_path[:-3] + "jpg"
  jpgImage = tiff_image.convert("RGB")
  return jpgImage

# Greater than this is considered white or nothing
white_threshold = 225

# Greater than this is labeled as gram positive, less than this is a black pixel 
gram_positive_threshold = 35

# This is for calculting the positive negative percentages for a single ImageDataFram, might have to be edited for 5 images
def PositiveNegativePercentages(ImageDataFrame):
  white_threshold = 225
  gram_positive_threshold = 35
  white = (ImageDataFrame['Darkness'] > white_threshold).sum()
  gram_positive = (ImageDataFrame['Darkness'] < gram_positive_threshold).sum()
  gram_negative = ((gram_positive_threshold < ImageDataFrame['Darkness']) & (ImageDataFrame['Darkness'] < white_threshold)).sum()
  
# This will prints the percents of each type 
def printPercents(ImageDataFrame,white,gram_positive,gram_negative):
  print('Percent of White ' + str(percent(white,len(ImageDataFrame))) + '%')
  print('Percent of gram positive ' + str(percent(gram_positive ,len(ImageDataFrame)))+ '%')
  print('Percent of gram negative ' + str(percent(gram_negative, len(ImageDataFrame)))+ '%')
  
def extract_numbers(text):
  numbers_str = re.findall(r'\d+', text)
  numbers_int = [int(num) for num in numbers_str]
  return numbers_int


def image_to_df(image):
    imageArray = np.array(image)
    reshaped = imageArray.reshape(-1, 3)
    df = pd.DataFrame(reshaped, columns=["Red", "Green", "Blue"])
    df["Darkness"] = df.apply(darkness_luminosity, axis=1)
    return df

def get_mouse_summary_df(mouse_name, folderPath):
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

# Path to Kaplan Lab HDD
# "D:" Goes to the HDD, After that inset file name
folderPath = ""

# Hashmap to Hold all of the Dataframes for each mouse and day
miceNames = {}

# Iterate through files in folder Path
for filename in os.listdir(folderPath):
    fileTypeTag = str(filename[-3:]).strip()
    nameSplit = filename.split("_")
    dayNumber = extract_numbers(nameSplit[0])[0]
    imageNumber = nameSplit[1]
    name = nameSplit[2]
    fileTypeTag = str(filename[-3:]).strip()
    
    # Counting the Number of Photos 
    if name in miceNames:
        currLists = miceNames[name]
        
        thislist = currLists[dayNumber - 1]
        thislist.append(filename)
    else:
        miceNames[name] = days = [[] for _ in range(15)]
        currLists = miceNames[name]
        
        thislist = currLists[dayNumber - 1]
        thislist.append(filename)