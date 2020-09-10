# -*- coding: utf-8 -*-
import wx

class MyFilterPanel(wx.Panel):
  def __init__(self,parent,id):
    wx.Panel.__init__(self,parent,id)
    self.panelList = []
    self.cbList = [] # list of MyComboBoxContent item
    self.filterList = [] # list of couple string,combobox
    self.initialize()

  def initLayout(self):
    self.vbox_top = wx.BoxSizer(wx.HORIZONTAL)
    self.vbox = wx.BoxSizer(wx.VERTICAL)

  def setLayout(self):
    self.vbox_top.Add(self.vbox, 1, wx.LEFT, 5)
    self.SetSizer(self.vbox_top)

    self.Centre()
    #self.Update()
    self.Show()

    #self.appendButton('Apply Filter')

  def initialize(self):
    self.initLayout()

    # panel1

    panel1 = wx.Panel(self, -1)
    grid1 = wx.GridSizer(2, 2)
    grid1.Add(wx.StaticText(panel1, -1, 'Find: ', (5, 5)), 0,  wx.ALIGN_CENTER_VERTICAL)
    grid1.Add(wx.ComboBox(panel1, -1, size=(120, -1)))
    grid1.Add(wx.StaticText(panel1, -1, 'Replace with: ', (5, 5)), 0, wx.ALIGN_CENTER_VERTICAL)
    grid1.Add(wx.ComboBox(panel1, -1, size=(120, -1)))

    panel1.SetSizer(grid1)
    self.panelList.append(panel1)
    self.vbox.Add(panel1, 0, wx.BOTTOM | wx.TOP, 9)

    # panel2

    panel2 = wx.Panel(self, -1)
    hbox2 = wx.BoxSizer(wx.HORIZONTAL)

    sizer21 = wx.StaticBoxSizer(wx.StaticBox(panel2, -1, 'Direction'), orient=wx.VERTICAL)
    sizer21.Add(wx.RadioButton(panel2, -1, 'Forward', style=wx.RB_GROUP))
    sizer21.Add(wx.RadioButton(panel2, -1, 'Backward'))
    hbox2.Add(sizer21, 1, wx.RIGHT, 5)

    sizer22 = wx.StaticBoxSizer(wx.StaticBox(panel2, -1, 'Scope'), orient=wx.VERTICAL)
    # we must define wx.RB_GROUP style, otherwise all 4 RadioButtons would be mutually exclusive
    sizer22.Add(wx.RadioButton(panel2, -1, 'All', style=wx.RB_GROUP))
    sizer22.Add(wx.RadioButton(panel2, -1, 'Selected Lines'))
    hbox2.Add(sizer22, 1)

    panel2.SetSizer(hbox2)
    self.panelList.append(panel2)
    self.vbox.Add(panel2, 0, wx.BOTTOM, 9)

    # panel3

    panel3 = wx.Panel(self, -1)
    sizer3 = wx.StaticBoxSizer(wx.StaticBox(panel3, -1, 'Options'), orient=wx.VERTICAL)
    vbox3 = wx.BoxSizer(wx.VERTICAL)
    grid = wx.GridSizer(3, 2, 0, 5)
    grid.Add(wx.CheckBox(panel3, -1, 'Case Sensitive'))
    grid.Add(wx.CheckBox(panel3, -1, 'Wrap Search'))
    grid.Add(wx.CheckBox(panel3, -1, 'Whole Word'))
    grid.Add(wx.CheckBox(panel3, -1, 'Incremental'))
    vbox3.Add(grid)
    vbox3.Add(wx.CheckBox(panel3, -1, 'Regular expressions'))
    sizer3.Add(vbox3, 0, wx.TOP, 4)

    panel3.SetSizer(sizer3)
    self.panelList.append(panel3)
    self.vbox.Add(panel3, 0, wx.BOTTOM, 15)

    # panel4

    panel4 = wx.Panel(self, -1)
    sizer4 = wx.GridSizer(2, 2, 2, 2)
    sizer4.Add(wx.Button(panel4, -1, 'Find', size=(120, -1)))
    sizer4.Add(wx.Button(panel4, -1, 'Replace/Find', size=(120, -1)))
    sizer4.Add(wx.Button(panel4, -1, 'Replace', size=(120, -1)))
    sizer4.Add(wx.Button(panel4, -1, 'Replace All', size=(120, -1)))

    panel4.SetSizer(sizer4)
    self.panelList.append(panel4)
    self.vbox.Add(panel4, 0, wx.BOTTOM, 9)

    # panel5

    panel5 = wx.Panel(self, -1)
    sizer5 = wx.BoxSizer(wx.HORIZONTAL)
    sizer5.Add((191, -1), 1, wx.EXPAND | wx.ALIGN_RIGHT)
    sizer5.Add(wx.Button(panel5, -1, 'Close', size=(50, -1)))

    panel5.SetSizer(sizer5)
    self.panelList.append(panel5)
    self.vbox.Add(panel5, 1, wx.BOTTOM, 9)

    self.setLayout()

  def initialize2(self):
    self.initLayout()
    self.create()
    self.setLayout()

  def deleteAllSubPanel(self):
    while self.panelList != []:
      self.panelList.pop(0).Destroy()

  def appendComboBox(self,name="Default ComboBox",defaultValue='Default Value',choices=[]):
    self.cbList.append(MyComboBoxContent(name,defaultValue,choices))

  def setComboBoxes(self,tripletList):
    for triplet in tripletList:
      self.appendComboBox(triplet[0],triplet[1],triplet[2])

  def create(self):
    panel1 = wx.Panel(self, -1)
    grid1 = wx.GridSizer(len(self.cbList), 2)
    while self.cbList != []:
      cb = self.cbList.pop(0)
      comboBox1 = wx.ComboBox(panel1, -1, size=(120, -1), value = cb.defaultValue, choices = cb.choices)
      comboBox1.SetEditable(False)
      grid1.Add(wx.StaticText(panel1, -1, cb.name, (5, 5)), 0,  wx.ALIGN_CENTER_VERTICAL)
      grid1.Add(comboBox1)
      #keep track of those combo boxes
      self.filterList.append((cb.name,comboBox1))
    panel1.SetSizer(grid1)
    self.panelList.append(panel1)
    self.vbox.Add(panel1, 0, wx.BOTTOM | wx.TOP, 9)

    panel5 = wx.Panel(self, -1)
    sizer5 = wx.BoxSizer(wx.HORIZONTAL)
    sizer5.Add((191, -1), 1, wx.EXPAND | wx.ALIGN_RIGHT)
    self.buttonApplyFilter = wx.Button(panel5, wx.ID_DELETE, 'Apply filter')
    sizer5.Add(self.buttonApplyFilter)

    panel5.SetSizer(sizer5)
    self.panelList.append(panel5)
    self.vbox.Add(panel5, 1, wx.BOTTOM, 9)

  def bind(self, method):
    self.buttonApplyFilter.Bind(wx.EVT_BUTTON, method, self.buttonApplyFilter)

  def appendButton(self,name="Default Button"):
    button = wx.Button(self, -1, name)
    self.sizerFilter.Add(button, 1, wx.EXPAND)
    self.SetSizer(self.sizerFilter)

  def clear(self):
    self.vbox_top.Clear()
    self.deleteAllSubPanel()
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.filterList = []

class MyComboBoxContent:
  def __init__(self,name="Default ComboBox",defaultValue='Default Value',choices=[]):
    self.name = name
    self.defaultValue = defaultValue
    self.choices = choices