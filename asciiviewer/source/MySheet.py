# -*- Coding : UTF-8 -*-

import wx
from wx.lib import sheet

from MyCalculation import MyCalculation
from MyRefcase import MyRefcase


# TODO bind mousewheel and scroll bar
# TODO cell selection with shift+page up/down

class MySheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.parent = parent
        # self.row = self.col = 0
        self.pointSize = 10
        self.resetSize()
        self.SetNumberRows(5)
        self.SetNumberCols(5)
        self.SetDefaultCellFont(
            wx.Font(self.pointSize, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

    def autosizeRowLabel(self):
        nDigits = len(str(self.GetNumberRows()))
        self.SetRowLabelSize((nDigits + 1) * self.pointSize)

    def setColFormat(self, summary):
        for i, (label, contentType, content) in enumerate(summary):
            if contentType == 1:
                self.SetColFormatNumber(i)

    def SetNumberRows(self, nrow):
        super(MySheet, self).SetNumberRows(nrow)
        self.autosizeRowLabel()

    def onKeyDown(self, evt):
        keyCode = evt.GetKeyCode()
        if evt.ControlDown():
            if keyCode == 67:
                # key 'c'
                self.Copy()  # should be overloaded to take advantage of wx.GridTableBase
        evt.Skip()

    def resetSize(self):
        resizeExistingCols = True
        self.SetDefaultColSize(130, resizeExistingCols)
        for i in range(self.GetNumberCols()):
            self.SetColFormatFloat(i)
        self.ForceRefresh()

    def addColLabel(self, colIndex, stringList):
        """Add all the string in stringList as column label after the last column (colIndex = -1)"""
        if colIndex == -1:
            ncol = self.GetNumberCols()
        else:
            ncol = colIndex
        nnewcols = len(stringList)
        self.SetNumberCols(ncol + nnewcols)
        i = 0
        for s in stringList:
            self.SetColLabelValue(ncol + i, s)
            i = i + 1

    def pasteRow(self, rowIndex, colIndex, stringList):
        if rowIndex < 0 or colIndex < 0:
            raise AssertionError("Index must be strict positive integer")
        i = 0
        for s in stringList:
            self.SetCellValue(rowIndex, colIndex + i, str(s))
            i = i + 1

    def pasteCol(self, rowIndex, colIndex, stringList):
        if rowIndex < 0 or colIndex < 0:
            raise AssertionError("Index must be strict positive integer")
        i = 0
        for s in stringList:
            self.SetCellValue(rowIndex + i, colIndex, str(s))
            i = i + 1

    # def displayCalculation(self,calculation):
    # """Display the content of MyCalculation object in the sheet"""
    # XSList = calculation.filteredXS
    # set the column labels
    # colLabelList = calculation.getDisplayLabel()
    # self.addColLabel(0,colLabelList)
    # if XSList != ['All']:
    # row = calculation.getDisplayRow()
    # self.SetNumberRows(len(row))
    # i = 0
    # for r in row:
    # self.pasteRow(i,0,r)
    # i+=1
    # self.resetSize()

    def displayRefcase(self, refcase, XSList=[], GrList=[]):
        """Display the content of MyRefCase object in the sheet"""
        # pvalList = calculation.pvalList
        dicoIsotope = refcase.dicoIsotope
        # set the column labels
        if XSList[0] == 'All':
            XSList = list(refcase.setXS)
            XSList.sort()
        ncol = 1 + len(XSList)
        colLabelList = ['isotope']
        for xs in XSList:
            for g in GrList:
                xslabel = str(xs) + " groupe %2d" % g
                colLabelList.append(str(xslabel))
        self.addColLabel(0, colLabelList)
        # recover all calculations and sort them
        i = 0
        isotopeList = dicoIsotope.keys()
        # mupletList = calculation.getFilteredMupletList()
        isotopeList.sort()
        self.SetNumberRows(len(isotopeList))
        #
        for isotope in isotopeList:
            # convert int muplet into value muplet
            self.pasteRow(i, 0, [isotope])
            # paste XS
            j = 0
            dicoXS = dicoIsotope[isotope]
            for xs in XSList:
                for g in GrList:
                    try:
                        xsvalue = [dicoXS[xs][g - 1]]
                    except:
                        xsvalue = ["None"]
                    self.pasteRow(i, 1 + j, xsvalue)
                    j = j + 1
            i = i + 1
        self.resetSize()
