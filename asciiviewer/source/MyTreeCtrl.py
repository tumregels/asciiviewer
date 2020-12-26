# -*- coding: utf-8 -*-

from __future__ import print_function
import os, sys, ConfigParser
from operator import isSequenceType

import wx

import MyAsciiParser, MyParserTool
from MyParserTool import LinkedListElement
from MyCalculation import MyMicroLib, MyCalculation
from MyRefcase import MyRefcase

try:
    import ROOT
    from ROOT import gROOT, TCanvas, TH2F
except ImportError:
    print("ROOT couldn't be imported, continuing anyway...")


class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)

    def bind(self, mainWindow):
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, mainWindow.OnItemExpanded, self)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, mainWindow.OnItemCollapsed, self)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, mainWindow.OnSelChanged, self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, mainWindow.OnActivated, self)

    def find(self, root, searchString, searchAll=True):
        """
        Return node,-1 for if node's label if ok
        Return node,idx for if sheet's idxth cell if ok
        FIXME : searchAll=False should break when the first item is found
        """
        nodeList = []
        nc = self.GetChildrenCount(root, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(root, cookie)
            GetChild = self.GetNextChild
            if searchString in self.GetItemText(child).lower():
                nodeList.append((child, -1))
            if (self.ItemHasChildren(child)):
                nodeList += self.find(child, searchString)
            else:
                content = self.GetItemData(child).content
                for i, c in enumerate(content):
                    if searchString in c.lower():
                        nodeList.append((child, i))
        return nodeList

    def findMatchCase(self, root, searchString):
        """
        Return node,-1 for if node's label if ok
        Return node,idx for if sheet's idxth cell if ok
        """
        nodeList = []
        nc = self.GetChildrenCount(root, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(root, cookie)
            GetChild = self.GetNextChild
            if searchString in self.GetItemText(child):
                nodeList.append((child, -1))
            if (self.ItemHasChildren(child)):
                nodeList += self.find(child, searchString)
            else:
                content = self.GetItemData(child).content
                for i, c in enumerate(content):
                    if searchString in c:
                        nodeList.append((child, i))
        return nodeList

    # def findCell(self,root,searchString,matchCase = False,matchWholeField = False):
    # """
    # Return the first cell for which the label is searchString
    # """
    # i = -1
    # search = None
    # nc = self.GetChildrenCount(root,False)

    # def GetFirstChild(parent, cookie):
    # return self.GetFirstChild(parent)

    # GetChild = GetFirstChild
    # cookie = 1
    # for i in range(nc):
    # child,cookie = GetChild( root, cookie )
    # GetChild = self.GetNextChild
    # if( self.ItemHasChildren( child ) ):
    # search = self.findCell( child, searchString, matchCase, matchWholeField )
    # if( search != None ):
    # break
    # else:
    # content = self.GetItemData(child).content
    # if matchWholeField:
    # if searchString in content:
    # search = child
    # i = content.index(searchString)
    # break
    # else:
    # for i,c in enumerate(content):
    # if searchString in c:
    # search = child
    # break
    # if search != None:
    # break
    # return search

    # ----------------------------------------------------------------------#

    def getChildIdAndData(self, parent, childText):
        childId = None
        childData = None
        nc = self.GetChildrenCount(parent, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            if self.GetItemText(child) == childText:
                childId = child
                childData = self.GetItemData(child)
                break
        return childId, childData

    def getChildId(self, parent, childText):
        childId, childData = self.getChildIdAndData(parent, childText)
        return childId

    def getChildData(self, parent, childText):
        childId, childData = self.getChildIdAndData(parent, childText)
        return childData

    # ----------------------------------------------------------------------#

    def getChildrenIdAndData(self, parent):
        childrenId = []
        childrenData = []
        nc = self.GetChildrenCount(parent, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            childrenId.append(child)
            childrenData.append(self.GetItemData(child))
        return childrenId, childrenData

    def getChildrenId(self, parent):
        childrenId, childrenData = self.getChildrenIdAndData(parent)
        return childrenId

    def getChildrenData(self, parent):
        childrenId, childrenData = self.getChildrenIdAndData(parent)
        return childrenData

    # ----------------------------------------------------------------------#

    def expandAllChildren(self, parent):
        nc = self.GetChildrenCount(parent, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            self.expandAllChildren(child)
            self.Expand(child)

    def collapseAllChildren(self, parent):
        nc = self.GetChildrenCount(parent, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            self.collapseAllChildren(child)
            self.Collapse(child)

    def collapseChildren(self, parent):
        nc = self.GetChildrenCount(parent, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            self.Collapse(child)

    def expandAll(self):
        self.expandAllChildren(self.GetRootItem())

    def GetPrevVisible(self, item):
        lastVisibleChild = item
        parent = self.GetItemParent(item)
        nc = self.GetChildrenCount(parent, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            if child == item:
                break
            GetChild = self.GetNextChild
            if self.IsVisible(child):
                lastVisibleChild = child

        if lastVisibleChild == item:
            lastVisibleChild = parent

        return lastVisibleChild

    def recoverAsciiFile(self, filePath):
        config = ConfigParser.RawConfigParser()
        config.read(os.path.expanduser('~/.asciiviewer.cfg'))
        sort = config.getboolean('mainconfig', 'sort')
        expand = config.getboolean('mainconfig', 'expand')

        def fPass(item):
            pass

        if sort:
            fSort = self.SortChildren
        else:
            fSort = fPass
        if expand:
            fExpand = self.Expand
        else:
            fExpand = fPass
        root = self.AddRoot(filePath)
        elementList = MyParserTool.elementListFromFile(filePath)
        self.BuildTree(elementList, fExpand, fSort)

    def getSummary(self, eltId):
        # getSummary aims to give a view of the first rank children, if relevant
        # returns a list of couples (string,list of strings)
        summary = []
        childrenId, childrenData = self.getChildrenIdAndData(eltId)
        for i, nodeId in enumerate(childrenId):
            content = childrenData[i].content.getContent()
            if isSequenceType(content) and content != []:
                summary.append((self.GetItemText(nodeId), childrenData[i].contentType, content))
            else:
                summary.append((self.GetItemText(nodeId), 3, ["Directory"]))
        return summary

    def computeMulticompoCalculation(self, eltId, eltData, parentId, parentData):
        nameDirId = self.GetItemParent(self.GetItemParent(self.GetItemParent(eltId)))
        nameDirData = self.GetItemData(nameDirId)
        eltDataStateVector = self.getChildData(nameDirId, "STATE-VECTOR")
        eltGlobalId = self.getChildId(nameDirId, "GLOBAL")
        eltParkey = self.getChildData(eltGlobalId, "PARKEY")
        calcIdList = self.getChildrenId(eltId)
        eltDataTreeId = self.getChildId(parentId, "TREE")
        eltDataDebarb = self.getChildData(eltDataTreeId, "DEBARB")
        eltDataArbval = self.getChildData(eltDataTreeId, "ARBVAL")
        eltDataNvp = self.getChildData(eltDataTreeId, "NVP")
        eltDataNcals = self.getChildData(eltDataTreeId, "NCALS")
        ngroup = int(eltDataStateVector.content.getContent()[1])
        nvp = int(eltDataNvp.content.getContent()[0])
        nptot = len(eltParkey.content.getContent())
        ncals = int(eltDataNcals.content.getContent()[0])
        debarb = eltDataDebarb.content.getContent()
        arbval = eltDataArbval.content.getContent()
        myCalculation = MyCalculation(ngroup)
        for cId in calcIdList:
            c = self.GetItemData(cId)
            ical = int(c.label)
            muplet = MyParserTool.comupl(nvp, nptot, ical, ncals, debarb, arbval)
            c.contentType = 1
            c.content = muplet
            stateVector = self.getChildData(cId, "STATE-VECTOR")
            nameData = self.getChildData(cId, "ISOTOPERNAME")
            densData = self.getChildData(cId, "ISOTOPESDENS")
            tempData = self.getChildData(cId, "ISOTOPESTEMP")
            todoData = self.getChildData(cId, "ISOTOPESTODO")
            typeData = self.getChildData(cId, "ISOTOPESTYPE")
            usedData = self.getChildData(cId, "ISOTOPESUSED")
            volData = self.getChildData(cId, "ISOTOPESVOL")
            microLib = MyMicroLib(stateVector.content.getContent(), nameData.content.getContent(),
                                  densData.content.getContent(), tempData.content.getContent(),
                                  todoData.content.getContent(), typeData.content.getContent(),
                                  usedData.content.getContent(), volData.content.getContent())
            for isotope in microLib.isotopeRname:
                eltIsoId = self.getChildId(cId, isotope)
                eltXSList = self.getChildrenData(eltIsoId)
                microLib.addIsotope(isotope, eltXSList)
            myCalculation.addCalc(muplet, microLib)
        pvalList = []
        for i in range(len(eltParkey.content.getContent())):
            pvali = "pval%08d" % (i + 1)
            eltPvali = self.getChildData(eltGlobalId, pvali)
            pvalList.append(eltPvali.content.getContent())
        myCalculation.setParkey(eltParkey.content.getContent())
        myCalculation.setPvalList(pvalList)
        myCalculation.initializeOnceFilled()
        # myCalculation.computeDiffFromSTRD()
        eltData.content.setContent(myCalculation)

    def computeEditionRefcase(self, eltId, eltData, parentId, parentData):
        isotopeNameList = self.getChildData(eltId, "ISOTOPERNAME").content
        isotopeDensList = self.getChildData(eltId, "ISOTOPESDENS").content
        for i in range(len(isotopeNameList)):
            isotopeNameLength = len(isotopeNameList[i])
            if isotopeNameLength != 8:
                addSpace = ' ' * (8 - isotopeNameLength)
                isotopeNameList[i] = isotopeNameList[i] + addSpace
            isotopeNameList[i] = isotopeNameList[i] + "%04d" % 1
        calcIdList = self.getChildrenId(eltId)
        dicoRefcase = MyRefcase()
        for cId in calcIdList:
            c = self.GetItemData(cId)
            if c.label in isotopeNameList:
                eltXSList = self.getChildrenData(cId)
                for eltXS in eltXSList:
                    dicoRefcase.addXS(c.label, eltXS)
                eltDens = LinkedListElement(id=-1, level=-1, labelType=-1, label='DENSITY', contentType=2,
                                            content=[isotopeDensList[isotopeNameList.index(c.label)]])
                dicoRefcase.addXS(c.label, eltDens)
        dicoRefcase.createUserComputedMacroIsotope()
        dicoRefcase.computeMacro()
        eltData.content = dicoRefcase

    def computeReactionRate(self, eltId, eltData, parentId, parentData):
        groupIdList = self.getChildrenId(eltId)
        ngroup = len(groupIdList)
        meshXData = self.getChildData(parentId, "MESHX")
        meshYData = self.getChildData(parentId, "MESHY")
        meshZData = self.getChildData(parentId, "MESHZ")
        nx = len(meshXData.content)
        ny = len(meshYData.content)
        nz = len(meshZData.content)
        # nameDirId = self.GetItemParent(self.GetItemParent(self.GetItemParent(eltId)))
        # nameDirData = self.GetItemData(nameDirId)
        # eltDataStateVector = self.getChildData(nameDirId, "STATE-VECTOR")
        # eltGlobalId = self.getChildId(nameDirId, "GLOBAL")
        # eltParkey = self.getChildData(eltGlobalId, "PARKEY")
        # calcIdList = self.getChildrenId(eltId)
        # eltDataTreeId = self.getChildId(parentId, "TREE")
        # eltDataDebarb = self.getChildData(eltDataTreeId, "DEBARB")
        # eltDataArbval = self.getChildData(eltDataTreeId, "ARBVAL")
        # eltDataNvp = self.getChildData(eltDataTreeId, "NVP")
        # eltDataNcals = self.getChildData(eltDataTreeId, "NCALS")

        # nvp = int(eltDataNvp.content[0])
        # nptot = len(eltParkey.content)
        # ncals = int(eltDataNcals.content[0])
        # debarb = eltDataDebarb.content
        # arbval = eltDataArbval.content
        myCalculation = MyCalculation(ngroup)
        for gId in groupIdList:
            g = self.GetItemData(gId)
            igr = int(g.label)
            for ix, mx in enumerate(meshXData.content):
                for iy, my in enumerate(meshYData.content):
                    for iz, mz in enumerate(meshZData.content):
                        muplet = [ix, iy, iz, igr]
                        print(muplet, ix + nx * iy + nx * ny * iz)
            # c.contentType = 1
            # c.content = muplet
            # stateVector  = self.getChildData(cId, "STATE-VECTOR")
            # nameData = self.getChildData(cId, "ISOTOPERNAME")
            # densData = self.getChildData(cId, "ISOTOPESDENS")
            # tempData = self.getChildData(cId, "ISOTOPESTEMP")
            # todoData = self.getChildData(cId, "ISOTOPESTODO")
            # typeData = self.getChildData(cId, "ISOTOPESTYPE")
            # usedData = self.getChildData(cId, "ISOTOPESUSED")
            # volData  = self.getChildData(cId, "ISOTOPESVOL")
            # microLib = MyMicroLib(stateVector.content, nameData.content, densData.content, tempData.content, todoData.content, typeData.content, usedData.content, volData.content)
            # for isotope in microLib.isotopeRname:
            # eltIsoId = self.getChildId(cId, isotope)
            # eltXSList   = self.getChildrenData(eltIsoId)
            # microLib.addIsotope(isotope,eltXSList)
            # myCalculation.addCalc(muplet,microLib)
        # pvalList=[]
        # for i in range(len(eltParkey.content)):
        # pvali = "pval%08d" % (i+1)
        # eltPvali    = self.getChildData(eltGlobalId,pvali)
        # pvalList.append(eltPvali.content)
        # myCalculation.setParkey(eltParkey.content)
        # myCalculation.setPvalList(pvalList)
        # myCalculation.initializeOnceFilled()
        ##myCalculation.computeDiffFromSTRD()
        # eltData.content = myCalculation

    def computeFluxMap(self, eltId, eltData, parentId, parentData):
        groupList = self.getChildrenId(eltId)
        self.c = []
        fluxMapList = []
        for gElt in groupList:
            groupNumber = self.GetItemText(gElt)
            gData = self.getChildData(gElt, 'FLUX-INTG')
            fluxMapList.append(gData.content)
        gNb = 0
        nx = 60
        ny = 60
        nz = 29
        # for each energy group
        for fluxMap in fluxMapList:
            gNb += 1
            groupNumber = '%d' % gNb
            gROOT.Reset()
            c = TCanvas(groupNumber, '2D Histograms of group ' + groupNumber + ' (FLUX-INTG)', 0, 0, 700, 600)
            histFlux = TH2F(groupNumber, 'Flux of group ' + groupNumber, nx, -nx / 2, nx / 2, ny, -ny / 2, ny / 2)
            histFlux.GetXaxis().SetTitle("X axis title")
            histFlux.GetXaxis().SetDecimals(ROOT.kTRUE)
            histFlux.GetYaxis().SetTitle("Y axis title")
            for n in range(nx * ny):
                x = n / nx - (nx + 1) / 2
                y = n % ny - (ny + 1) / 2
                z = float(fluxMap[(nz - 1) * nx * ny + n])
                histFlux.Fill(int(x), int(y), z)
            histFlux.DrawCopy('LEGO2')
            ROOT.gStyle.SetPalette(1)
            c.Update()
            self.c.append(c)
        # for group 1 over group 2
        gROOT.Reset()
        c = TCanvas('ratio', '2D Histograms of group 1 over group 2 ratio (FLUX-INTG)', 0, 0, 700, 600)
        histFlux = TH2F('ratio', 'Flux ratio', nx, -nx / 2, nx / 2, ny, -ny / 2, ny / 2)
        histFlux.GetXaxis().SetTitle("X axis title")
        histFlux.GetYaxis().SetTitle("Y axis title")
        for n in range(nx * ny):
            x = n / nx - (nx + 1) / 2
            y = n % ny - (ny + 1) / 2
            z = float(fluxMapList[0][(nz - 1) * nx * ny + n]) / float(fluxMapList[1][(nz - 1) * nx * ny + n])
            histFlux.Fill(x, y, z)
        histFlux.DrawCopy('LEGO2')
        ROOT.gStyle.SetPalette(1)
        c.Update()
        self.c.append(c)

    def BuildTree(self, elementList, fExpand, fSort):
        root = self.GetRootItem()
        for e in elementList:
            if e.level == 1:
                parent = self.AppendItem(root, e.label, data=e)
                self.AddAsciiChildren(elementList, e, parent, fExpand, fSort)
                fSort(parent)
                fExpand(parent)
        fSort(root)
        fExpand(root)

    def AddAsciiChildren(self, elementList, e, parent, fExpand, fSort):
        parentLevel = e.level
        i = e.id + 1
        nextLevel = parentLevel + 1
        imax = len(elementList)
        while abs(nextLevel) > parentLevel and i < imax:
            nextElt = elementList[i]
            nextLevel = nextElt.level
            if nextLevel == parentLevel + 1:
                node = self.AppendItem(parent, nextElt.label, data=nextElt)
                self.AddAsciiChildren(elementList, elementList[i], node, fExpand, fSort)
                fSort(node)
                if self.GetChildrenCount(node) < 10:
                    fExpand(node)
            i = i + 1
