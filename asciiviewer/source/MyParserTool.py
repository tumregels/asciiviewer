#!/usr/bin/python
# -*- coding: utf-8 -*-

# author : Benjamin Toueg
# date : 30/10/10

from __future__ import print_function


def elementListFromFile(filePath):
    with open(filePath) as inputfile:
        # read the 4 first character
        head = inputfile.read(4)
    if '$XSM' in head:
        # if the first four characters are "$XSM" it's most certainly a XSM file
        from MyXsmParser import xsmToElementList
        return xsmToElementList(filePath)
    else:
        # we suppose it's an ASCII file
        from MyAsciiParser import asciiToElementList
        return asciiToElementList(filePath)


# ----------------------------------------------------------------------#

class LinkedListElement:
    def __init__(self, id, level, labelType, label, contentType, content):
        self.id = id
        self.level = level
        self.labelType = labelType
        self.label = str(label)
        self.contentType = contentType
        self.content = content
        self.table = None  # MyTableColumn(self.label,self.content)

    def __str__(self):
        s = "==LinkedListElement=="
        s += str(self.id) + " " + str(self.level) + " " + str(self.labelType) + " " + str(self.label) + " " + str(
            self.contentType)
        if self.content != None:
            s += " " + str(self.content.content)
        return s


class Content:
    def __init__(self, contentType, contentSize, content, bProcess, rawFormat="ASCII"):
        self.rawFormat = rawFormat  # "ASCII" or "XSM"
        self.contentType = contentType
        self.contentSize = contentSize
        self.content = content
        self.processed = False
        if bProcess:
            self.process()

    def process(self):
        if not (self.processed):
            if self.rawFormat == "ASCII":
                self.content = getContent(self.contentType, self.contentSize, self.content)
            elif self.rawFormat == "XSM":
                self.content = getContent2(self.contentType, self.contentSize, self.content)
            else:
                raise AssertionError("Unexpected raw format " + self.rawFormat)
        self.processed = True
        return True

    def getContent(self):
        self.process()
        return self.content

    def setContent(self, content):
        self.content = content
        self.processed = True


def getContent(contentType, contentSize, rhs):
    rhs = rhs[13:]
    rhs = rhs.lstrip(' ')
    rhs = rhs.replace('\n', '')
    if contentType == 3:
        rhs = rhs[10 * contentSize:]
        rhs = rhs.replace('\n', '')
        step = fancyStep(rhs)
        content = []
        if step == 0:
            content = rhs.split()
        else:
            while rhs != '':
                content.append(rhs[0:step].strip())
                rhs = rhs[step:]
    else:
        content = None
        if contentSize > 0:
            content = rhs.split()
    return content


def getContent2(contentType, contentSize, rhs):
    if contentType == 3:
        rhs = rhs.replace('\n', '')
        step = fancyStep(rhs)
        content = []
        if step == 0:
            content = rhs.split()
        else:
            while rhs != '':
                content.append(rhs[0:step].strip())
                rhs = rhs[step:]
    elif contentType == 2:
        content = None
        if contentSize > 0:
            content = ["%1.8E" % f for f in rhs]
    elif contentType == 10:
        content = []
    else:
        content = rhs
    return content


def fancyStep(string):
    """Try to find a proper step to cut the string"""
    n = len(string)
    stepList = [12, 8, 4]
    myStep = 0
    for s in stepList:
        # try cutting 's' chars by 's' chars
        properStep = (n % s == 0)
        if properStep:
            startingCharList = string[0::s]
            for car in startingCharList:
                if car == ' ':
                    properStep = False
                    break
        if properStep:
            copy = string[:]
            while copy != '':
                if copy[0:s].strip() == '':
                    properStep = False
                    break
                copy = copy[s:]
        if properStep:
            myStep = s
            break
    return myStep


def comupl(nvp, nptot, ical, ncals, debarb, arbval):
    """function described in IGE295 as SUBROUTINE COMUPL"""
    """Returns an int list"""
    muplet = []
    i = nvp - (ncals - 1)
    io = -1
    while (i < nvp + 1):
        if (int(debarb[i]) == int(ical)):
            io = i
            break
        i = i + 1
    muplet.insert(0, int(arbval[io - 1]))
    ipar = nptot - 1
    while (ipar > 0):
        for i in range(nvp):
            if int(debarb[i]) == 0:
                print("problem", i)
            if int(debarb[i]) > io:
                io = i
                break
        muplet.insert(0, int(arbval[io - 1]))
        ipar = ipar - 1
    return muplet
