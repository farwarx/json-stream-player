# json-stream-player
Json Stream Player for Kodi - Can send a stream with thumb,subtitle,title to Kodi in JSON.

It's a video addon for Kodi.
Works with Kodi 14.0 Helix Unwinds.

# Explanation
I create this to use with the yify-pop projet.
Because, i can't send a title or subtitle URL with JSON, i create an addon to support this.
I add a simple form to yify-pop to play my stream on my Kodi (Raspberry-Pi Openelec).

# Usage
Send a JSON request with this parameters:

url = "URL of your video stream"
title = "Title of your video"
thumb = "URL of the cover thumb"
lang = "LANG of the subtitle"
subtitle = "URL of the subtitle file"

{
  "jsonrpc": "2.0",
  "method": "Addons.ExecuteAddon",
  "params":
  {
    "addonid": "plugin.video.stream.player",
    "params":
    {
      "url":"URL",
      "title": "TITLE",
      "thumb": "THUMB",
      "lang": "LANG",
      "subtitle": "SUBTITLE"
    }
  },
  "id": 1
}

# Example

{
  "jsonrpc": "2.0",
  "method": "Addons.ExecuteAddon",
  "params":
  {
    "addonid": "plugin.video.stream.player",
    "params":
    {
      "url":"http://domain.tld:8889",
      "title": "Movie title",
      "thumb": "http://cover.domaine.tld/mycover.jpg",
      "lang": "fr",
      "subtitle": "http://subtitle.domain.tld/subtitle.fr.srt"
    }
  },
  "id": 1
}

# Extra links
Kodi:  http://kodi.tv/
Yify-pop : https://github.com/farwarx/yify-pop


Farwarx.
