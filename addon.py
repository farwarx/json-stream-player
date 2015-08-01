import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import urlparse
import urllib2
import json
import ssl

##### Variables #####
__addon__ 	= xbmcaddon.Addon()
__addonname__	= __addon__.getAddonInfo('name')

class MyPlayer(xbmc.Player):
  def __init__(self, *args, **kwargs):
    xbmc.Player.__init__(self, *args, **kwargs)
    self.tracking = False
    self.position = 0
    self.totaltime = 0
    self.tracking = True

  def onPlayBackStopped(self):
    self.tracking = False

  def onPlayBackEnded(self):
    self.tracking = False


##### Functions #####
def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonname__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

##### Play #####
def play(url, title, params):
  #xbmc.sleep(2000)
  listitem = xbmcgui.ListItem (title)
  logline = "URL: %s / Title: %s" % (url, title)
  if( 'thumb' in params ):
    listitem.setThumbnailImage(params['thumb'])
    logline = "%s / Thumbnail: %s" % (logline, params['thumb'])
  #listitem.setProperty("IsPlayable","true")

  log(logline)
  xbmc.Player().play(url, listitem)

  #listitem.setPath(url)
  #xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url, listitem=listitem, isFolder=False)
  #xbmcplugin.addDirectoryItem(int(sys.argv[1]), "", listitem)
  #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
  #xbmcplugin.endOfDirectory(int(sys.argv[1]))

##### Sub #####
def subadd(lang, subtitle):
  xbmc.sleep(2000)
  log("Language: %s / URL: %s" % (lang, subtitle))
  xbmc.Player().setSubtitles(subtitle.encode("utf-8"))


def get_params():
  param = {}

  if(len(sys.argv) > 1):
    for i in sys.argv:
      args = i
      if(args.startswith('?')):
        args = args[1:]
      param.update(dict(urlparse.parse_qsl(args)))

  return param

#the program mode
params = get_params()

if (not 'version' in params) or (int(params['version']) > 2):
  xbmc.executebuiltin('Notification("%s","Addon obsolete",10000)' %(__addonname__) )
  sys.exit(1);

if (not 'version' in params) or (int(params['version']) != 2):
  xbmc.executebuiltin('Notification("%s","Serveur obsolete",10000)' %(__addonname__) )
  sys.exit(1);

player=MyPlayer()

play(params['url'], params['title'], params)
if( 'subtitle' in params ):
  subadd(str(params['lang'][0]), str(params['subtitle'][0]))

mark_as_viewed = False
while( (not xbmc.abortRequested) and (player.tracking) and (not mark_as_viewed) ):
  if player.isPlayingVideo():
    player.position = player.getTime()
    player.totaltime = player.getTotalTime()
    try:
      position = player.position*100 / player.totaltime

      #log("Playing %s at %s %%" %(params['title'], position) )
      if position >= 95:
        log("Mark as viewed")

	# Python = langage de merde donc
	# je decoupe et recalcul mon url
        urlparams = urlparse.urlparse(params['markviewed'])
        urlparams_copie = (urlparams[0], urlparams.netloc.split('@')[1]) + urlparams[2:]
        url = urlparse.urlunparse(urlparams_copie)

	# python = langage de merde donc
	# je cree un contexte pour pas etre emmerde avec ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

	# python = langage de merde donc
	# je cree une requete (c'est peut etre le moins pourri de tout le code)
	# encore que je fait l'authen basic a la main car sinon c'est trop reloud
        req = urllib2.Request(url, 'action=set')
        req.add_header('Authorization', 'Basic ' + (urlparams.username + ':' + urlparams.password).encode('base64').rstrip())

        # Petit detail qui a son importance ca fonctionne toujours pas pour moi !?
        urlhandler = urllib2.urlopen(req, context=ctx)
        data = json.load(urlhandler.read())
        if 'seen' in data:
          mark_as_viewed = True
    except Exception as e:
      log(str(e))

  xbmc.sleep(1000)

if not mark_as_viewed:
  log("Stopped without full view")

#log("-------------------------------------- END --------------------------------------")
