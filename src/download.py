from pytube import YouTube

url = 'https://www.youtube.com/watch?v=gSYGOZVugtw'
youtube = YouTube(url)
video = youtube.streams.get_highest_resolution()
video.download('C:\\Users\\marou\\Desktop\\VIDEO2BLOG')