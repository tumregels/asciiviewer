# -*- Coding : UTF-8 -*-

import wx
from wx.lib import sheet

# TODO bind mousewheel and scroll bar
# TODO cell selection with shift+page up/down


class _DiscardedCellEditor(wx.grid.GridCellTextEditor):
    # wx.lib.sheet.CSheet's real CCellEditor is broken (raises TypeErrors on
    # edit) and deprecated (subclasses wx.grid.PyGridCellEditor), so we
    # replace GRID_VALUE_STRING's editor with the stock GridCellTextEditor
    # right after CSheet.__init__ runs - see MySheet.__init__ below.
    #
    # But CSheet.__init__ itself still constructs one CCellEditor(self) just
    # to register it, and that lone construction is enough to trigger the
    # deprecation warning even though we throw the result away a moment
    # later. This class is a drop-in swap for CCellEditor (same (self, grid)
    # constructor signature) that CSheet can build without ever touching the
    # deprecated base class. It's a real GridCellEditor so wx's C++ side
    # still accepts it - it just does nothing beyond that.
    def __init__(self, grid):
        super().__init__()


sheet.CCellEditor = _DiscardedCellEditor


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
            wx.Font(self.pointSize, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        )
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

    def SetTable(self, table, *args, **kwargs):
        # wx.grid.Grid.SetTable() defaults to takeOwnership=False, so the C++ grid
        # keeps only a raw pointer to the table and calls back into its Python
        # GridTableBase methods during the swap. The table objects here (eltData.table)
        # are otherwise only kept alive by the tree item's data, which gets freed
        # when the tree is rebuilt for a new file (see MainWindow.OnOpenFile). If that
        # drops the outgoing table's last reference, CPython deallocates it immediately -
        # while the C++ side is still using it to detach - and segfaults. Keep it alive
        # (via self._currentTable) until after SetTable() has finished the swap.
        result = super().SetTable(table, *args, **kwargs)
        self._currentTable = table
        return result

    def autosizeRowLabel(self):
        nDigits = len(str(self.GetNumberRows()))
        self.SetRowLabelSize((nDigits + 1) * self.pointSize)

    def setColFormat(self, summary):
        for i, (label, contentType, content) in enumerate(summary):
            if contentType == 1:
                self.SetColFormatNumber(i)

    def SetNumberRows(self, nrow):
        super().SetNumberRows(nrow)
        self.autosizeRowLabel()

    def onKeyDown(self, evt):
        keyCode = evt.GetKeyCode()
        if evt.ControlDown() and keyCode == 67:  # key 'c'
            self.Copy()  # should be overloaded to take advantage of wx.GridTableBase
        evt.Skip()

    def resetSize(self):
        resizeExistingCols = True
        self.SetDefaultColSize(130, resizeExistingCols)
        table = self.GetTable()
        for i in range(self.GetNumberCols()):
            if table is not None and self.isColNumeric(table, i):
                self.SetColFormatFloat(i)
        self.ForceRefresh()

    def isColNumeric(self, table, col):
        """
        The float column editor asserts if the underlying value can't be
        parsed as a float, so only format a column as float when every cell
        actually is one (leaf columns can just as well hold plain text, e.g.
        node labels).
        """
        for row in range(table.GetNumberRows()):
            value = table.GetValue(row, col)
            if value in (None, ''):
                continue
            try:
                float(value)
            except (TypeError, ValueError):
                return False
        return True

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
