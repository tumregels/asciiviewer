import wx


class MyFindReplaceDialog(wx.FindReplaceDialog):
    def __init__(self, parent):
        wx.FindReplaceDialog.__init__(self, parent, wx.FindReplaceData(1), "Search within nodes and cells",
                                      wx.FR_NOMATCHCASE)
        self.resultList = []  # triple list (node,idx in sheet = -1 if node is the interest)
        self.idx = -1
        self.lastSearchString = None
        self.lastWholeWord = None

    def setResult(self, resultList, searchString=None, wholeWord=None):
        self.resultList = resultList
        self.idx = 0
        self.lastSearchString = searchString
        self.lastWholeWord = wholeWord

    def hasQueryChanged(self, searchString, wholeWord):
        return searchString != self.lastSearchString or wholeWord != self.lastWholeWord

    def getCurrentFind(self):
        if self.resultList != []:
            item = self.resultList[self.idx]
        else:
            item = None
        return item

    def getNextFind(self):
        down = self.getFlag()
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
        down = not self.getFlag()
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
        down = (flags & wx.FR_DOWN) > 0
        return down

    def getWholeWord(self):
        flags = self.GetData().GetFlags()
        return (flags & wx.FR_WHOLEWORD) > 0

    def setFlag(self, down):
        flags = 0
        if down: flags += wx.FR_DOWN
        self.GetData().SetFlags(flags)
