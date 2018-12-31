from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    url = 'https://www.youtube.com/watch?v=BaW_jenozKc'
    result = ydl.extract_info("{}".format(url))
    title = result.get("title", None)
    print(title)
    print(ydl.prepare_filename(result))
    ydl.download([url])