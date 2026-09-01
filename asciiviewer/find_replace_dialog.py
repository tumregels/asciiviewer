import wx


class MyFindReplaceDialog(wx.FindReplaceDialog):
    def __init__(self, parent):
        wx.FindReplaceDialog.__init__(self, parent, wx.FindReplaceData(1), "Search within nodes and cells",
                                      wx.FR_NOWHOLEWORD | wx.FR_NOMATCHCASE)
        self.resultList = []  # triple list (node,idx in sheet = -1 if node is the interest)
        self.idx = -1

    def setResult(self, resultList):
        self.resultList = resultList
        self.idx = 0

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

    def setFlag(self, down):
        flags = 0
        if down: flags += wx.FR_DOWN
        self.GetData().SetFlags(flags)
