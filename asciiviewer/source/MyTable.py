# -*- Coding : UTF-8 -*-
import wx
from wx.grid import GridTableBase


class MyTableColumn(wx.grid.GridTableBase):
    def __init__(self, label, contentList):
        wx.grid.GridTableBase.__init__(self)
        self.nRow = len(contentList)
        self.nCol = 1
        self.contentList = contentList
        self.rowLabels = [str(i) for i in range(1, self.nRow + 1)]
        self.colLabels = [label]

    def GetNumberRows(self):
        return self.nRow

    def GetNumberCols(self):
        return self.nCol

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.contentList[row]

    def SetValue(self, row, col, value):
        pass

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return self.rowLabels[row]


class MySummaryTable(wx.grid.GridTableBase):
    def __init__(self, summary):
        wx.grid.GridTableBase.__init__(self)
        self.nCol = len(summary)
        self.nRow = 1
        self.rowLabels = []
        self.colLabels = []
        for i, (label, contentType, content) in enumerate(summary):
            self.nRow = max(self.nRow, len(content))
            self.colLabels.append(str(label))
        self.rowLabels = [str(i) for i in range(1, self.nRow + 1)]
        self.summary = summary

    def GetNumberRows(self):
        return self.nRow

    def GetNumberCols(self):
        return self.nCol

    def IsEmptyCell(self, row, col):
        label, contentType, content = self.summary[col]
        empty = False
        try:
            value = content[row]
        except IndexError:
            value = ''
            empty = True
        return empty

    def GetValue(self, row, col):
        label, contentType, content = self.summary[col]
        try:
            value = content[row]
        except IndexError:
            value = ''
        return value

    def SetValue(self, row, col, value):
        pass

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return self.rowLabels[row]


class MyCalculationTable(wx.grid.GridTableBase):
    def __init__(self, row, colLabels):
        wx.grid.GridTableBase.__init__(self)
        self.nRow = len(row)
        self.nCol = len(row[0])
        self.row = row
        self.rowLabels = [str(i) for i in range(1, self.nRow + 1)]
        self.colLabels = colLabels

    def GetNumberRows(self):
        return self.nRow

    def GetNumberCols(self):
        return self.nCol

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, iRow, iCol):
        return self.row[iRow][iCol]

    def SetValue(self, row, col, value):
        pass

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return self.rowLabels[row]
