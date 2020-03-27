#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import urllib
import simplejson as json

import xbmcgui
import xbmcplugin
import xbmcaddon

def getParameters(parameterString):
  commands = {}
  splitCommands = parameterString[parameterString.find('?') + 1:].split('&')
  for command in splitCommands:
    if (len(command) > 0):
      splitCommand = command.split('=')
      key = splitCommand[0]
      value = splitCommand[1]
      commands[key] = value
  return commands


def getLiveStreams():
  streams = {}
  res = urllib.urlopen('https://www.lrt.lt/data-service/module/live/').read()
  data = json.loads(res)

  for name, value in data['response']['data'].items():
    streams[name] = {'title': value['title'], 'type': value['type'], 'url': value['content']}
  return streams

def getMenuList():
  streams = getLiveStreams()

  for name, streamData in streams.items():
    listitem = xbmcgui.ListItem(name)
    listitem.setProperty('IsPlayable', 'true')

    info = { 'plot': streamData['title'] }
    streamType = 'audio' if streamData['type'] == 'radio' else 'video'
    listitem.setInfo(type = streamType, infoLabels = info )

    url = sys.argv[0] + '?' + urllib.urlencode({'mode': 1, 'url': streamData['url'], 'title': name})
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = listitem, isFolder = False, totalItems = 0)

  xbmcplugin.endOfDirectory(int(sys.argv[1]))


def playVideo(url, title):
  if not url:
    dialog = xbmcgui.Dialog()
    ok = dialog.ok( 'LRT Grotuvas' , 'Bloga vaizdo įrašo nuoroda "%s"!' % url )
    return

  listitem = xbmcgui.ListItem(label = title)
  listitem.setPath(url)
  xbmcplugin.setResolvedUrl(handle = int(sys.argv[1]), succeeded = True, listitem = listitem)


def main():
  params = getParameters(sys.argv[2])
  mode = None

  try:
    mode = int(params['mode'])
  except:
    pass

  if mode == None:
    getMenuList()
  elif mode == 1:
    url = urllib.unquote_plus(params['url'])
    title = urllib.unquote_plus(params['title'])
    playVideo(url, title)


main()