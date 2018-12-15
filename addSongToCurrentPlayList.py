#!/usr/bin/python3
#-*- coding: UTF-8 -*-

import requests
import urllib
import re
import sys
import os

def regex(page, reg):
    data = re.search(reg, page.text)
    if data is not None:
        return data.group(1)
    else:
        return ""

def getInfo(page, tag):
    return regex(page, '<meta property="'+tag+'" content="([^"]+)">')

session = requests.Session()

def addOneSong(url):
    page = session.get(url)
    #page = session.get("https://open.spotify.com/track/0oirge6JFaWcDYEcigWXeK?si=YTwZL3SxR2auAKtu2g0nbg")

    title = getInfo(page, "og:title")
    musician = getInfo(page, "twitter:audio:artist_name")
    spotifyId = getInfo(page, "og:url")
    duration = regex(page,'"duration_ms":(\d+),')
    album = regex(page,'"name":"([^"]+)","release_date":"')

    spotifyId = spotifyId.replace("https://open.spotify.com/track/", "spotify:track:")

    print(title)

    open("/tmp/song.xspf", "w").write("""<?xml version="1.0" encoding="UTF-8"?>
<playlist version="1" xmlns="http://xspf.org/ns/0/">
  <trackList>
    <track>
      <location>"""+spotifyId+"""</location>
      <title>"""+title+"""</title>
      <creator>"""+musician+"""</creator>
      <duration>"""+duration+"""</duration>
      <album>"""+album.encode().decode("unicode-escape")+"""</album>
    </track>
</playlist>
""")

    os.system("/usr/bin/clementine -a /tmp/song.xspf")
    return

if (len(sys.argv) > 1 ):
    addOneSong(sys.argv[1])

while(True):
    for uri in input("Uri: ").split(" "):
        addOneSong(uri)
