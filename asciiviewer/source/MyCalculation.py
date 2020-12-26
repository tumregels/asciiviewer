# -*- coding: utf-8 -*-

from __future__ import print_function
from MyFilterPanel import MyFilterPanel
from MyTable import MyCalculationTable


class MyMicroLib:
    def __init__(self, stateVector, name=[], dens=[], temp=[], todo=[], Stype=[], used=[], vol=[]):
        self.nIsotope = int(stateVector[1])
        self.nGroup = int(stateVector[2])
        self.nAnisoOrder = int(stateVector[3])
        self.isotopeRname = name
        self.isotopeSdens = dens
        self.isotopeStemp = temp
        self.isotopeStodo = todo
        self.isotopeStype = Stype
        self.isotopeSused = used
        self.isotopeSvol = vol
        self.isotopeXs = {}
        self.setXS = set()
        for isotope in self.isotopeRname:
            self.isotopeXs[isotope] = {}

    def getInfo(self, xs, g, isotope='*MAC*RES'):
        try:
            xsg = ['None']
            if xs in self.isotopeXs[isotope]:
                xsAllGroup = self.isotopeXs[isotope][xs]
                if xs[:4] in ['SCAT']:
                    xsg = xsAllGroup[g * self.nGroup:(g + 1) * self.nGroup]
                else:
                    xsg = [xsAllGroup[g]]
        except IndexError as e:
            xsg = ['Error']
        return xsg

    def addIsotope(self, isotope, eltXSList):
        xsStorage = self.isotopeXs[isotope]
        # ijj/njj are list of IJJ/NJJ for increasing anisotropy order
        ijj = [[]] * self.nAnisoOrder
        njj = [[]] * self.nAnisoOrder
        scat = [[]] * self.nAnisoOrder
        for xs in eltXSList:
            self.setXS.add(xs.label)
            if xs.label[:4] in ['IJJS', 'NJJS', 'SCAT']:
                for l in range(self.nAnisoOrder):
                    ijjLabel = 'IJJS%02d' % l
                    njjLabel = 'NJJS%02d' % l
                    scatLabel = 'SCAT%02d' % l
                    if xs.label == ijjLabel:
                        ijj[l] = xs.content.getContent()
                    elif xs.label == njjLabel:
                        njj[l] = xs.content.getContent()
                    elif xs.label == scatLabel:
                        scat[l] = xs.content.getContent()
            else:
                # simply store regular XS
                xsStorage[xs.label] = xs.content.getContent()
        # check consistency
        if ijj.count([]) > 0 or njj.count([]) > 0:
            raise AssertionError('Problem with anisotropy order')
        # reconstruct scattering matrix from compressed scattering matrix
        for l in range(self.nAnisoOrder):
            scatLabel = 'SCAT%02d' % l
            scatUnzipped = [str(0.)] * (self.nGroup * self.nGroup)
            departureGroup = range(self.nGroup)
            idx = 0
            for gd in departureGroup:
                i = int(ijj[l][gd])
                n = int(njj[l][gd])
                arrivalGroup = range(i - n, i)[::-1]
                for ga in arrivalGroup:
                    scatUnzipped[gd * self.nGroup + ga] = scat[l][idx]
                    idx += 1
            xsStorage[scatLabel] = scatUnzipped
        # try to compute diffusion coefficient from STRD
        if 'STRD' in xsStorage:
            myLabel = 'USER-DIFF'
            self.setXS.add(myLabel)
            myContent = []
            for xs in xsStorage['STRD']:
                diffStr = '%.8E' % (1 / (3 * float(xs)))
                myContent.append(diffStr)
            xsStorage[myLabel] = myContent
            if 'TRANC' in xsStorage:
                myLabel = 'USER-DIFF-TRANC'
                self.setXS.add(myLabel)
                myContent = []
                for g in range(self.nGroup):
                    strd_f = float(xsStorage['STRD'][g])
                    tranc_f = float(xsStorage['TRANC'][g])
                    myContent.append('%.8E' % (1 / (3 * (strd_f - tranc_f))))
                xsStorage[myLabel] = myContent
        # try to compute flux1 / flux2 in an homogeneous infinite medium
        if ('SCAT00' in xsStorage) and ('NTOT0' in xsStorage):
            scat_1_1 = float(xsStorage['SCAT00'][0 * self.nGroup + 0])  # 1 <- 2
            scat_1_2 = float(xsStorage['SCAT00'][0 * self.nGroup + 1])  # 1 <- 2
            scat_2_1 = float(xsStorage['SCAT00'][1 * self.nGroup + 0])  # 2 <- 1
            scat_2_2 = float(xsStorage['SCAT00'][1 * self.nGroup + 1])  # 1 <- 2
            sigtot_1 = float(xsStorage['NTOT0'][0])
            sigtot_2 = float(xsStorage['NTOT0'][1])
            sigr_1 = sigtot_1 - scat_1_1
            sigr_2 = sigtot_2 - scat_2_2
            flux_1_over_flux_2 = sigr_2 / scat_2_1
            myLabel = 'Flux1/Flux2'
            self.setXS.add(myLabel)
            myContent = ['%.8E' % flux_1_over_flux_2]
            xsStorage[myLabel] = myContent
            # try to compute kinf in an homogeneous infinite medium
            if 'NUSIGF' in xsStorage:
                nusigf_1 = float(xsStorage['NUSIGF'][0])
                nusigf_2 = float(xsStorage['NUSIGF'][1])
                kinf = (nusigf_1 * flux_1_over_flux_2 + nusigf_2) / (sigr_1 * flux_1_over_flux_2 - scat_1_2)
                myLabel = 'USER-KINF'
                self.setXS.add(myLabel)
                myContent = ['%.8E' % kinf]
                xsStorage[myLabel] = myContent
        # save
        self.isotopeXs[isotope] = xsStorage


class MyCalculation:
    def __init__(self, ngroup):
        self.ngroup = ngroup
        self.maxAnisoOrder = 0
        self.mupletMicroLib = {}
        self.filterPanel = None
        self.parkey = []
        self.parfmt = []
        self.pvalList = []
        self.setXS = set()
        self.filteredMuplet = None
        self.filteredXS = ['All']
        self.filteredGroup = range(1, self.ngroup + 1)
        self.xsToDisplayNormal = ['CHI',
                                  'H-FACTOR',
                                  'N2N',
                                  'N3N',
                                  'N4N',
                                  'NA',
                                  'NFTOT',
                                  'NG',
                                  'NTOT0',
                                  'NUSIGF',
                                  'NWT0',
                                  'OVERV',
                                  'STRD',
                                  'TRANC',
                                  'USER-DIFF',
                                  'USER-DIFF-TRANC',
                                  'Flux1/Flux2',
                                  'USER-KINF',
                                  ]
        self.xsToDisplayAniso = ['SCAT', 'SIGS']

    def setFilterPanel(self, filterPanel):
        self.filterPanel = filterPanel

    def initializeOnceFilled(self):
        self.initXs()
        self.initFilteredMuplet()
        self.initFilteredXS()

    def initXs(self):
        """
        Replace 'SCAT' with 'SCAT00' 'SCAT01' 'SCAT...' in self.xsToDisplayAniso
        """
        labelList = []
        for lbl in self.xsToDisplayAniso:
            for l in range(self.maxAnisoOrder):
                labelList.append(lbl + '%02d' % l)
        self.xsToDisplayAniso = labelList

    def initFilteredMuplet(self):
        """
        Reset the muplet filter to ALL : [ [] , [] , [] , ... ]
        """
        npval = len(self.parkey)
        self.filteredMuplet = [[]] * npval

    def initFilteredXS(self):
        self.setXS = self.setXS & set(self.xsToDisplayNormal + self.xsToDisplayAniso)
        self.filteredXS = list(self.setXS)
        self.filteredXS.sort()

    def getComboBoxesList(self):
        cbList = []
        parkey = self.parkey
        pvalList = self.pvalList
        choicesXS = ['All']
        listXS = list(self.setXS)
        listXS.sort()
        choicesXS.extend(listXS)
        choicesGroup = ['All']
        listGroup = []
        for g in range(self.ngroup):
            listGroup.append(str(g + 1))
        choicesGroup.extend(listGroup)
        for i in range(len(parkey)):
            choices = ['All']
            for pval in pvalList[i]:
                choices.append(str(pval))
            cbList.append((parkey[i], self.getFilterValue(i), choices))
        cbList.append(('Energy group', self.getDefaultGroup(), choicesGroup))
        cbList.append(('Cross section', self.getDefaultXS(), choicesXS))
        return cbList

    def getDefaultXS(self):
        """
        Returns the default value of the comboBox XSname
        """
        if len(self.filteredXS) == len(self.setXS):
            stringDefault = 'All'
        else:
            stringDefault = self.filteredXS[0]
        return stringDefault

    def getDefaultGroup(self):
        """
        Returns the default value of the comboBox Energy group
        """
        if len(self.filteredGroup) == self.ngroup:
            stringDefault = 'All'
        else:
            stringDefault = str(self.filteredGroup[0])
        return stringDefault

    def getFilterValue(self, i):
        try:
            idx = self.filteredMuplet[i][0] - 1
            return str(self.pvalList[i][idx])
        except IndexError:
            return 'All'

    def addCalc(self, muplet, microLib):
        muplet = tuple(muplet)
        if self.mupletMicroLib.has_key(muplet):
            raise AssertionError('mupletMicroLib should not have any microLib for this muplet yet')
        self.mupletMicroLib[muplet] = microLib
        self.maxAnisoOrder = max(self.maxAnisoOrder, microLib.nAnisoOrder)
        self.setXS = self.setXS | microLib.setXS  # union

    def setPvalList(self, pvalList):
        """Set value list and format for each parameter"""
        self.pvalList = []
        for valList in pvalList:
            try:
                isIntList = True
                for val_s in valList:
                    val_f = float(val_s)
                    val_i = int(val_f)
                    if val_i != val_f:
                        isIntList = False
                        break
                if isIntList:
                    ivalList = []
                    for val_s in valList:
                        val_s = '%d' % int(float(val_s))
                        ivalList.append(val_s)
                    self.pvalList.append(ivalList)
                else:
                    optimized_precision = '1'
                    for val_s in valList:
                        val_f = float(val_s)
                        val_s2 = '%.' + optimized_precision + 'f'
                        val_s2 = val_s2 % val_f
                        while float(val_s2) != float(val_s) and int(optimized_precision) < 8:
                            optimized_precision = str(int(optimized_precision) + 1)
                            val_s2 = '%.' + optimized_precision + 'f'
                            val_s2 = val_s2 % val_f
                    if int(optimized_precision) < 8:
                        format = '%.' + optimized_precision + 'f'
                        evalList = []
                        for val_s in valList:
                            val_s = format % float(val_s)
                            evalList.append(val_s)
                        self.pvalList.append(evalList)
                    else:
                        self.pvalList.append(valList)
            except ValueError:
                self.pvalList.append(valList)

    def setParkey(self, parkey):
        self.parkey = parkey

    def OnApplyFilter(self, evt):
        evt.Skip()
        filterList = self.filterPanel.filterList
        for name, combobox in filterList:
            value = str(combobox.GetValue())
            if name == 'Cross section':
                if value == 'All':
                    self.filteredXS = list(self.setXS)
                    self.filteredXS.sort()
                else:
                    self.filteredXS = [value]
            elif name == 'Energy group':
                if value == 'All':
                    self.filteredGroup = range(1, self.ngroup + 1)
                else:
                    self.filteredGroup = [int(value)]
            else:
                try:
                    idxparkey = self.parkey.index(name)
                    if value == 'All':
                        self.filteredMuplet[idxparkey] = []
                    else:
                        try:
                            idxvalue = self.pvalList[idxparkey].index(value)
                            self.filteredMuplet[idxparkey] = [idxvalue + 1]
                        except ValueError:
                            print('Warning : ', value, ' not found in ', self.pvalList[idxparkey])
                except ValueError:
                    print('Warning : ', name, ' not found in parkey ', self.parkey)

    def getFilteredMupletList(self, isotope='*MAC*RES'):
        """
        Returns a list of muplet according to the filter
        """
        mupletList = self.mupletMicroLib.keys()
        filteredMupletList = []
        mFilter = self.filteredMuplet
        for m in mupletList:
            keep = True
            for i in range(len(mFilter)):
                # if mFilter[i] is empty it means it's not filtered, so we keep it
                if mFilter[i] != [] and not m[i] in mFilter[i]:
                    keep = False
                    break
            if keep:
                filteredMupletList.append(m)
        filteredMupletList.sort()
        return filteredMupletList

    def getDisplayRow(self):
        """
        Returns a list of microLib content to be used in MySheet
        """
        row = []
        mupletList = self.getFilteredMupletList()
        for muplet in mupletList:
            # convert int muplet into value muplet
            j = 0
            mValue = []
            for m in muplet:
                value_s = self.pvalList[j][m - 1]
                mValue.append(value_s)
                j = j + 1
            # recover cross sections
            microLib = self.mupletMicroLib[muplet]
            for xs in self.filteredXS:
                if xs in ['Flux1/Flux2', 'USER-KINF']:
                    mValue += microLib.getInfo(xs, 0)
                else:
                    for g in self.filteredGroup:
                        mValue += microLib.getInfo(xs, g - 1)
            row.append(mValue)
        return row

    def getDisplayLabel(self):
        """
        Returns a list of labels to be used in MySheet
        """
        # fill labels with computation parameters
        labelParamList = []
        for p in self.parkey:
            labelParamList.append(str(p))
        # fill label with cross sections
        labelXsList = []
        for xs in self.filteredXS:
            if xs in ['Flux1/Flux2', 'USER-KINF']:
                labelXsList.append(xs)
            else:
                for g in self.filteredGroup:
                    xslabel = str(xs)
                    if xslabel[:4] in ['SCAT']:
                        for ga in self.filteredGroup:
                            xslabel = str(xs) + ' %2d <- %2d' % (g, ga)
                            labelXsList.append(xslabel)
                    else:
                        xslabel += ' gr%2d' % g
                        labelXsList.append(xslabel)
        return labelParamList + labelXsList

    def getTable(self):
        return MyCalculationTable(self.getDisplayRow(), self.getDisplayLabel())
