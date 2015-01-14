import xbmc
import xbmcaddon
import xbmcgui
import urlparse

##### Variables #####
__addon__ 	= xbmcaddon.Addon()
__addonname__	= __addon__.getAddonInfo('name')

##### Functions #####
def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonname__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

##### Play #####
def play(url, title, thumb):
  xbmc.sleep(2000)
  listitem = xbmcgui.ListItem (title, thumbnailImage=thumb)
  log("URL: %s / Title: %s / Thumbnail: %s" % (url, title, thumb))
  xbmc.Player().play(url, listitem)

##### Sub #####
def subadd(lang, subtitle):
  xbmc.sleep(2000)
  log("Language: %s / URL: %s" % (lang, subtitle))
  xbmc.Player().setSubtitles(subtitle.encode("utf-8"))


##### Execute #####
# Ajout securite
# Recuperation des parametres JSON
params = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)


play(str(params['url'][0]), str(params['title'][0]), str(params['thumb'][0]))
xbmc.sleep(2000)
subadd(str(params['lang'][0]), str(params['subtitle'][0]))

log("End")
