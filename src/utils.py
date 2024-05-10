from pytube import YouTube
import cv2
import numpy as np
import os
import pytesseract
import json
from .utils import *
from .whisper import *


# Set the tesseract path in the script before calling image_to_string
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#

def extract_text_from_image(image_path):
    dicts = {}
    for i, img_file in enumerate(os.listdir(image_path)):
        img = cv2.imread(os.path.join(image_path, img_file))

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img)
        #add the text to a dictionary
        dicts[i] = text

    return dicts

#image_path = "C:\\Users\\marou\\Desktop\\VIDEO2BLOG\\slidemse"
#dicts = extract_text_from_image(image_path)
#print(dicts)


def combine_dicts(dict1, dict2):
    combined = {}
    for i in range(len(dict1)):
        combined[i] = {
            "path": f"./slidemse/slide_{i}.png",
            "start": dict1[i][0],
            "end": dict1[i][1],
            "descrp": dict2[i]
        }
    return json.dumps(combined, indent=4)





def download(url):
    youtube = YouTube(url)
    video = youtube.streams.get_highest_resolution()
    file_path=video.download('./')     #TODO verify that a file path is returned
    return file_path




def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err



def extract_unique_slides_mse(video_path, mse_threshold=1000):
    if not os.path.exists('./slidemse/'):
        os.makedirs('./slidemse/')

    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, prev_frame = vidcap.read()
    count = 0
    saved_frame = 0
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    slide_times = []
    start_time = 0

    while success:
        success, frame = vidcap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mse_value = mse(prev_gray, gray)
        prev_gray = gray

        current_time = count / fps

        if mse_value > mse_threshold:
            img_path = os.path.join('./slidemse/', f"slide_{saved_frame}.png")
            cv2.imwrite(img_path, frame)
            print(f"Saved slide_{saved_frame}.png at time {current_time} seconds")
            end_time = current_time
            slide_times.append((start_time, end_time))
            start_time = current_time
            saved_frame += 1

        count += 1
    

    vidcap.release()
    print("Done!")
    dict = {}
    for i, (start, end) in enumerate(slide_times):
        dict[i] = (start, end)

    return dict



def videotodataframe(url) -> pd.DataFrame :
    video_path=download(url)
    asyncio.run(process_video_or_playlist(url, max_simultaneous_youtube_downloads, max_workers_transcribe))
    dict_time=extract_unique_slides_mse(video_path, mse_threshold=1000)
    dict_ocr=extract_text_from_image('./slidemse/')
    combined_json = combine_dicts(dict_time, dict_ocr)
    with open('combined.json', 'w') as f:
        f.write(combined_json)
    df=pd.read_csv('outputs/generated_transcript_metadata_tables/pde_chapter_ii_section_22.csv')
    with open("./combined.json", "r") as file:
        data = json.load(file)
        list_of_dicts = list(data.values())
    df_slides = pd.DataFrame(list_of_dicts)
    list = []
# add an column 'text' with the text of the transcript
    for i in range(len(list_of_dicts)):
        start=df_slides['start'][i]
        
        end=df_slides['end'][i]
        print(start,end)
        transcript=""
        for i in range(len(df['text'])):
            if df['start'][i]>=start and df['end'][i]<=end:
                transcript+=df['text'][i]
        list.append(transcript)
    df_slides['text'] = list

    return df_slides








