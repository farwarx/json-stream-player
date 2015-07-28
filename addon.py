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
def play(url, title, params):
  xbmc.sleep(2000)
  listitem = xbmcgui.ListItem (title)
  logline = "URL: %s / Title: %s" % (url, title)
  if( 'thumb' in params ):
    listitem.setThumbnailImage(str(params['thumb'][0]))
    logline = "%s / Thumbnail: %s" % (logline, str(params['thumb'][0]))

  log(logline)
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

play(str(params['url'][0]), str(params['title'][0]), params)
xbmc.sleep(2000)
if( 'subtitle' in params ):
  subadd(str(params['lang'][0]), str(params['subtitle'][0]))

log("End")
