import collections.abc
import configparser
import os

import wx

from asciiviewer.calculation import MyCalculation, MyMicroLib
from asciiviewer.parser import parser_tool
from asciiviewer.parser.parser_tool import LinkedListElement
from asciiviewer.ref_case import MyRefcase


class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)

    def bind(self, mainWindow):
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, mainWindow.OnItemExpanded, self)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, mainWindow.OnItemCollapsed, self)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, mainWindow.OnSelChanged, self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, mainWindow.OnActivated, self)

    def getResolvedContent(self, node):
        """
        node's data.content is either a raw Sequence or a lazy Content
        object (needs .getContent()); resolve it to a Sequence in both cases.
        """
        content = self.GetItemData(node).content
        if content is None:
            return []
        if isinstance(content, collections.abc.Sequence):
            return content
        return content.getContent()

    def cellTexts(self, c):
        """
        Numeric cells are stored raw (often scientific notation, e.g.
        '2.90595646E+01') but the sheet displays them formatted as a fixed-point
        float (SetColFormatFloat, e.g. '29.059565'). Search both representations
        so a user can find a cell by what they actually see on screen.
        """
        texts = [str(c)]
        try:
            texts.append(f'{float(c):f}')
        except (TypeError, ValueError):
            pass
        return texts

    def find(self, root, searchString, searchAll=True, wholeWord=False):
        """
        Return node,-1 for if node's label if ok
        Return node,idx for if sheet's idxth cell if ok
        If wholeWord is True, a node's label or a cell's value must match
        searchString exactly rather than merely contain it.
        FIXME : searchAll=False should break when the first item is found
        """

        def matches(text):
            return text == searchString if wholeWord else searchString in text

        nodeList = []
        nc = self.GetChildrenCount(root, False)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)

        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(root, cookie)
            GetChild = self.GetNextChild
            if matches(self.GetItemText(child)):
                nodeList.append((child, -1))
            if self.ItemHasChildren(child):
                nodeList += self.find(child, searchString, searchAll, wholeWord)
            else:
                content = self.getResolvedContent(child)
                for i, c in enumerate(content):
                    if any(matches(text) for text in self.cellTexts(c)):
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
        childId, _childData = self.getChildIdAndData(parent, childText)
        return childId

    def getChildData(self, parent, childText):
        _childId, childData = self.getChildIdAndData(parent, childText)
        return childData

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
        childrenId, _childrenData = self.getChildrenIdAndData(parent)
        return childrenId

    def getChildrenData(self, parent):
        _childrenId, childrenData = self.getChildrenIdAndData(parent)
        return childrenData

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
        config = configparser.RawConfigParser()
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
        _root = self.AddRoot(filePath)
        elementList = parser_tool.elementListFromFile(filePath)
        self.BuildTree(elementList, fExpand, fSort)

    def getSummary(self, eltId):
        # getSummary aims to give a view of the first rank children, if relevant
        # returns a list of couples (string,list of strings)
        summary = []
        childrenId, childrenData = self.getChildrenIdAndData(eltId)
        for i, nodeId in enumerate(childrenId):
            content = childrenData[i].content.getContent()
            if isinstance(content, collections.abc.Sequence) and content != []:
                summary.append((self.GetItemText(nodeId), childrenData[i].contentType, content))
            else:
                summary.append((self.GetItemText(nodeId), 3, ["Directory"]))
        return summary

    def computeMulticompoCalculation(self, eltId, eltData, parentId, parentData):
        nameDirId = self.GetItemParent(self.GetItemParent(self.GetItemParent(eltId)))
        _nameDirData = self.GetItemData(nameDirId)
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
            muplet = parser_tool.comupl(nvp, nptot, ical, ncals, debarb, arbval)
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
            microLib = MyMicroLib(
                stateVector.content.getContent(),
                nameData.content.getContent(),
                densData.content.getContent(),
                tempData.content.getContent(),
                todoData.content.getContent(),
                typeData.content.getContent(),
                usedData.content.getContent(),
                volData.content.getContent(),
            )
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
                eltDens = LinkedListElement(
                    id=-1,
                    level=-1,
                    labelType=-1,
                    label='DENSITY',
                    contentType=2,
                    content=[isotopeDensList[isotopeNameList.index(c.label)]],
                )
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
