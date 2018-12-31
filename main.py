from __future__ import unicode_literals
import youtube_dl
import requests
import pyperclip


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def uploadToStreamable(video):
    with open(video, 'rb') as file:
        login = superSecureLoginStorage()
        headers = {'User-Agent': 'Python bot to show our friend videos since youtube is not allowed :v'}
        r = requests.post('https://api.streamable.com/upload', files={video: file}, auth=(login[0], login[1]), headers=headers)
        
        return r.json()["shortcode"]

def superSecureLoginStorage():
    with open('pass.txt', 'r') as f:
        return f.read().splitlines()  # read in username/pass

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now uploading to streamable ...')

print(superSecureLoginStorage())

ydl_opts = {
    'format': 'best',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    url = 'https://www.youtube.com/watch?v=x6LovY_DdEE'  
    result = ydl.extract_info("{}".format(url))
    title = result.get("title", None)
    print(title)
    
    print(ydl.prepare_filename(result))
    shortcode = uploadToStreamable(ydl.prepare_filename(result))
    pyperclip.copy("https://streamable.com/" + shortcode)

