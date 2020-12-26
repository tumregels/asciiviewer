# -*- coding: utf-8 -*-

from __future__ import print_function


class MyRefcase:
    def __init__(self):
        self.dicoIsotope = {}
        self.filterIsope = []
        self.filterPanel = None
        self.setXS = set()
        self.filteredXS = ['All']
        self.ngroup = 0
        self.filteredGroup = []

    def getComboBoxesList(self):
        cbList = []
        choicesXS = ['All']
        listXS = list(self.setXS)
        listXS.sort()
        choicesXS.extend(listXS)
        # choicesGroup = ['All']
        # listGroup = []
        # for g in range(self.ngroup):
        # listGroup.append(str(g+1))
        # choicesGroup.extend(listGroup)
        # cbList.append(('Energy group',self.getDefaultGroup(),choicesGroup))
        cbList.append(('Cross section', self.getDefaultXS(), choicesXS))
        return cbList

    def getDefaultXS(self):
        """return the default value of the comboBox XSname"""
        stringDefault = 'All'
        if len(self.filteredXS) != len(self.setXS):
            stringDefault = self.filteredXS[0]
        return stringDefault

    def getDefaultGroup(self):
        """return the default value of the comboBox Energy group"""
        stringDefault = 'All'
        if len(self.filteredGroup) != self.ngroup:
            stringDefault = str(self.filteredGroup[0])
        return stringDefault

    def getFilterValue(self, i):
        try:
            idx = self.filterMuplet[i][0] - 1
            return str(self.pvalList[i][idx])
        except IndexError:
            return 'All'

    def setFilterPanel(self, filterPanel):
        self.filterPanel = filterPanel

    def addXS(self, isotope, eltData):
        nameXS = eltData.label
        dicoXS = {}
        if self.dicoIsotope.has_key(isotope):
            dicoXS = self.dicoIsotope[isotope]
        if dicoXS.has_key(nameXS):
            print("XS ", nameXS, " already defined for this isotope ", isotope)
        dicoXS[nameXS] = eltData.content
        self.dicoIsotope[isotope] = dicoXS
        self.setXS.add(nameXS)
        # self.ngroup = len(eltData.content)
        # self.filteredGroup = range(self.ngroup+1)[1:]

    def createUserComputedMacroIsotope(self):
        dicoMacro = {}
        for nameIso, dicoXS in self.dicoIsotope.items():
            for nameXS, valueList in dicoXS.items():
                nValue = len(valueList)
                if not (dicoMacro.has_key(nameXS)):
                    dicoMacro[nameXS] = [0.] * nValue
                elif nValue > len(dicoMacro[nameXS]):
                    dicoMacro[nameXS] = [0.] * nValue
        self.dicoIsotope['USER-MACRO'] = dicoMacro

    def computeMacro(self):
        dicoMacro = self.dicoIsotope['USER-MACRO']
        for nameIso, dicoXS in self.dicoIsotope.items():
            if nameIso != 'USER-MACRO':
                density = float(dicoXS['DENSITY'][0])
                for nameXS, valueList in dicoXS.items():
                    for i in range(len(valueList)):
                        dicoMacro[nameXS][i] = dicoMacro[nameXS][i] + float(valueList[i]) * density

    def initFilter(self):
        npval = len(self.parkey)
        self.filterMuplet = [[]] * npval
        # self.filterMuplet[0]=[1,4]

    def OnApplyFilter(self, evt):
        evt.Skip()
        filterList = self.filterPanel.filterList
        for name, combobox in filterList:
            value = str(combobox.GetValue())
            if name == 'Cross section':
                if value == 'All':
                    self.filteredXS = list(self.setXS)
                else:
                    self.filteredXS = [value]
