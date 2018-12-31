from __future__ import unicode_literals
import youtube_dl
import requests
import pyperclip
import sys
import os

# these two aren't necessary whatsoever

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now uploading to streamable ...')

def uploadToStreamable(video):
    """This sends uploads the video to Streamable and returns the "Shortcode" of the video. It takes a string of the filename and returns a string"""
    with open(video, 'rb') as file:
        login = superSecureLoginStorage()
        headers = {'User-Agent': 'Python bot to show our friend videos since youtube is not allowed :v'}
        r = requests.post('https://api.streamable.com/upload', files={video: file}, auth=(login[0], login[1]), headers=headers)
        
        return r.json()["shortcode"]

def superSecureLoginStorage():
    """This is a total hack that returns values stored in pass.txt to be used as a username/password"""
    if not os.path.exists('pass.txt'):
        raise ValueError("You need a pass.txt, with the first line username, the next password of a streamable account!")
    with open('pass.txt', 'r') as f:
        values = f.read().splitlines()  # read in username/pass
        if len(values) != 2:
            raise ValueError("one line should be your streamable username, the next should be your password!")
        return values



ydl_opts = {
    'format': 'best',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    if len(sys.argv) != 2:
        print("Call this with a youtube url plz, no other arguments allowed")
    else:
        url = sys.argv[1]
        result = ydl.extract_info("{}".format(url))

        filename = ydl.prepare_filename(result)

        shortcode = uploadToStreamable(filename)
        print("File uploaded, copying to clipboard and deleting")
        link = "https://streamable.com/" + shortcode
        pyperclip.copy(link)
        print(link)
        os.remove(filename)


