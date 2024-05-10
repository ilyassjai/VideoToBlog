from pytube import YouTube
import cv2
import numpy as np
import os



def download(url):
    url = 'https://www.youtube.com/watch?v=gSYGOZVugtw'
    youtube = YouTube(url)
    video = youtube.streams.get_highest_resolution()
    video.download('./')




def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err



def extract_unique_slides_mse(video_path, output_folder, mse_threshold=1000):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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
            img_path = os.path.join(output_folder, f"slide_{saved_frame}.png")
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


if __name__=='__main__':
    video_path = "./PDE - Chapter II - Section 22.mp4"
    output_folder = "./slidemse/"
    dict = extract_unique_slides_mse(video_path, output_folder)
    
    print(dict)


