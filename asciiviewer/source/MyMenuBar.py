import wx

ID_ABOUT = 101
ID_EXIT = 102
ID_OPEN = 103
ID_CLOSE = 104
ID_EXPAND_ALL = 105
ID_COLLAPSE_ALL = 106
ID_COLLAPSE_CHILDREN = 107
ID_SEARCH = 108


class MyMenuBar(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)

        menuFile = wx.Menu()
        menuFile.Append(ID_OPEN, '&Open')
        menuFile.Append(ID_CLOSE, '&Close')
        menuFile.Append(ID_EXIT, 'Quit')
        self.Append(menuFile, '&File')

        menuEdit = wx.Menu()
        menuEdit.Append(ID_EXPAND_ALL, '&Expand all')
        menuEdit.Append(ID_COLLAPSE_ALL, '&Collapse all')
        menuEdit.Append(ID_COLLAPSE_CHILDREN, 'Collapse C&hildren')
        menuEdit.Append(ID_SEARCH, '&Search')
        self.Append(menuEdit, '&Edit')

        menuHelp = wx.Menu()
        menuHelp.Append(ID_ABOUT, "&About")
        self.Append(menuHelp, '&Help')
