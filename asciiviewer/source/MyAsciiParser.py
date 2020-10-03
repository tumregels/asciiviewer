#!/usr/bin/python
# -*- coding: utf-8 -*-

# author : Benjamin Toueg
# date : 24/11/09

import wx
from MyParserTool import *

def asciiToElementList(filePath):
  with open(filePath) as inputfile:
    # print the entire file into one big string
    readablefile=inputfile.read()
  if readablefile[:2]=='->':
    # if the first two characters are "->" it's most certainly a Version4 ASCII file 
    return asciiToElementListVersion4(readablefile)
  else:
    # we suppose it's a Version3 ASCII file
    return asciiToElementListVersion3(readablefile)

def asciiToElementListVersion4(readablefile):
  # split the string according to <- and ->
  print 'reading file...'
  readablefile=readablefile.split('->')
  print 'organizing data...'
  elementList=[]
  id = 0
  for r in readablefile:
    if r != '':
      try:
	left,right = r.split('<-')
      except ValueError:
	raise AssertionError('Problem while parsing the following :\n'+'*'*70+'\n->'+r+'*'*70)
      # process the left part of <-
      level, labelType, contentType, contentSize = map(int,left.split())
      # process the right part of <-
      if labelType != 0:
	# get rid of the spaces between <- and the string label
        right = right.lstrip()
      label = right[0:12].strip()
      if contentSize!=0:
	content = Content(contentType,contentSize,right,False)
	element = LinkedListElement(id,level,labelType,label,contentType,content)
	elementList.append(element)
	id=id+1
  print 'building tree...'
  return elementList

def asciiToElementListVersion3(readablefile):
  readablefile=readablefile.replace('\n','')
  def readNodeHeader(string):
    header = string[0:38]
    string = string[38:]
    level = int(header[0:8])
    label = header[9:21]
    contentType = int(header[22:30])
    contentSize = int(header[30:38])
    return string, level, label, contentType, contentSize

  def readNodeContent(string,contentType,contentSize):
    if contentType==0:
      length = 0
      content = []
    elif contentType==1:
      length = contentSize*10
      content = string[0:length].split()
    elif contentType==2:
      length = contentSize*16
      content = string[0:length].split()
    elif contentType==3:
      length = contentSize
      raw_content = string[0:length]
      content = []
      step = fancyStep(raw_content)
      if step == 0:
        content = raw_content.split()
      else:
        while raw_content != '':
          content.append(raw_content[0:step].strip())
          raw_content = raw_content[step:]
    else:
      pass
    string = string[length:]
    return string, content

  elementList=[]
  id = 0
  while readablefile!='':
    readablefile, level, label, contentType, contentSize = readNodeHeader(readablefile)
    readablefile, content = readNodeContent(readablefile,contentType, contentSize)
    content = Content(contentType,contentSize,content,False)
    content.processed = True
    element = LinkedListElement(id,level,'12',label,contentType,content)
    elementList.append(element)
    id=id+1
  return elementList

def asciiToTree(filePath,tree):
  # this function was designed to be a faster alternative to asciiToElementList and then ConstructAsciiTree
  # but it's not that fast
  # we make the file a 1 line string and we split it according to <- and ->
  with open(filePath) as inputfile:
    #readablefile=inputfile.read().replace(' 4\n',' 4 \n').replace('\n','').split('->')
    readablefile=inputfile.read().split('->')

  #elementList=[]
  previousLevel = 0
  root = tree.GetRootItem()
  previousNode = root
  parent = root
  parentLevel = 0
  id = 0
  for r in readablefile:
    if r != '':
      pos_key=r.split('<-')
      if len(pos_key) != 2:
        print 'Problem with readable file'
        print r
      # process the left part of <-
      pos_key[0] = pos_key[0].split()
      level = int(pos_key[0][0])
      if level < 0:
        # we are climbing down the tree
        tree.SortChildren(parent)
        if parentLevel > 1 and tree.GetChildrenCount(parent) > 10:
          pass
        else:
          tree.Expand(parent)
        parent = tree.GetItemParent(parent)
        parentLevel -= 1
        previousLevel = level
      else:
        labelType = int(pos_key[0][1])
        contentType = int(pos_key[0][2])
        contentSize = int(pos_key[0][3])
        # process the right part <-
        if labelType != 0:
          pos_key[1] = pos_key[1].lstrip()
        label = pos_key[1][0:12].strip()
        pos_key[1] = pos_key[1][13:]
        pos_key[1] = pos_key[1].lstrip(' ')
        pos_key[1] = pos_key[1].replace('\n','')
        if contentSize!=0:
          if contentType==3:
            pos_key[1]=pos_key[1][10*contentSize:]
            pos_key[1]=pos_key[1].replace('\n','')
            step = fancyStep(pos_key[1])
            content = []
            if step == 0:
              content = pos_key[1].split()
            else:
              while pos_key[1] != '':
                content.append(pos_key[1][0:step].strip())
                pos_key[1] = pos_key[1][step:]
          else:
            content=None
            if contentSize>0:
              content=pos_key[1].split()
          if previousLevel < 0: # we know that level >= 0.
            parent = tree.GetItemParent(previousNode)
            while tree.GetPyData(parent).level >= level:
              parent = tree.GetItemParent(parent)
              if parent == root:
                break
          elif level > previousLevel:
            # we are climbing up the tree
            parent = previousNode
            parentLevel = previousLevel
          # create a LinkedListElement
          element = LinkedListElement(id,level,labelType,label,contentType,content)
          node = tree.AppendItem(parent, element.label, data=element)
          #elementList.append(element)
          id+=1
          previousLevel = level
          previousNode = node
  tree.SortChildren(root)
  tree.Expand(root)
  #return elementList

if __name__ == "__main__":
  import sys
  try:
    myFilePath = sys.argv[1]
  except:
    myFilePath="../example/MultiCompoV4"
  elementList=asciiToElementList(myFilePath)
  for e in elementList:
    if True:#e.level < 2:
      print e