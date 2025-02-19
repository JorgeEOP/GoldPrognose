import matplotlib.pyplot as plt
import os
import subprocess
import glob

def generateVideo(folder, videoName) -> None:
    os.chdir(folder)
    subprocess.call([
        'ffmpeg', '-framerate', '8', '-i', 'GoldKurs%d.png', '-y', '-r', '30', '-pix_fmt', 'yuv420p',
        videoName + '.mp4'
    ])
    for file_name in glob.glob("*.png"):
        os.remove(file_name)