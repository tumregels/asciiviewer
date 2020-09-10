# -*- coding: utf-8 -*-

import wx

class MyFindReplaceDialog(wx.FindReplaceDialog):
  def __init__(self,parent):
    wx.FindReplaceDialog.__init__(self,parent,wx.FindReplaceData(1),"Search within nodes and cells",wx.FR_NOWHOLEWORD)
    self.resultList = [] # triple list (node,idx in sheet = -1 if node is the interest)
    self.idx = -1

  def setResult(self,resultList):
    self.resultList = resultList
    self.idx = 0

  def getCurrentFind(self):
    if self.resultList != []:
      item = self.resultList[self.idx]
    else:
      item = None
    return item

  def getNextFind(self):
    down,wholeWord,matchCase = self.getFlag()
    if down:
      i = 1
    else:
      i = -1
    if self.resultList != []:
      self.idx = (self.idx + i) % len(self.resultList)
      item = self.resultList[self.idx]
    else:
      item = None
    return item

  def getPrevFind(self):
    down,wholeWord,matchCase = self.getFlag()
    down = not down
    if down:
      i = 1
    else:
      i = -1
    if self.resultList != []:
      self.idx = (self.idx + i) % len(self.resultList)
      item = self.resultList[self.idx]
    else:
      item = None
    return item

  def getFlag(self):
    flags = self.GetData().GetFlags()
    # uncompress flags
    matchCase =  (flags & wx.FR_MATCHCASE) > 0
    wholeWord =  (flags & wx.FR_WHOLEWORD) > 0
    down =  (flags & wx.FR_DOWN) > 0
    return down,wholeWord,matchCase

  def setFlag(self,down,wholeWord,matchCase):
    flags = 0
    if down: flags+=wx.FR_DOWN
    if wholeWord: flags+=wx.FR_WHOLEWORD
    if matchCase: flags+=wx.FR_MATCHCASE
    self.GetData().SetFlags(flags)

