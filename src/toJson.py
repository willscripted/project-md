#!/usr/bin/python

import sys
import json
import re

import zipper

import pandocfilters
from sh import pandoc

def markdownify(pandocJson):
  if type(pandocJson) != type([]):
    pandocJson = [pandocJson]

  doc = [{"unMeta": {}}, pandocJson]
  out = pandoc("-f", "json", "-t", "markdown", _in=json.dumps(doc))
  return str(out)


levelToType = [
    None,
    "project",
    "objective",
    "sub-objective",
    "sub-objective",
    "sub-objective",
    "sub-objective"
]


def isHeader(item):
  return item["t"] == "Header"

def isList(item):
  return item["t"] == "BulletList"

def level(block):
  return block["c"][0]

def headerToProjectJson(block):
  name = pandocfilters.stringify(block["c"][2])
  jsonType = levelToType[level(block)]
  return ["", name, jsonType, []]

# Remember, list order is [description name type ... children?]
def addFillerHeader(top, level):
  fillers = [
      None,
      ["", "-- Missing Project Name --", levelToType[1], []],
      ["", "-- Missing Objective Name --", levelToType[2], []],
      ["", "-- Missing Name --", levelToType[3], []],
      ["", "-- Missing Name --", levelToType[4], []],
      ["", "-- Missing Name --", levelToType[5], []],
      ["", "-- Missing Name --", levelToType[6], []]
  ]
  return top.rightmost().append(fillers[level])

def addHeader(top, headerBlock):
  for i in range(1, level(headerBlock)):
    if top.rightmost().node() == [] or top.rightmost().node()[-1][2] == "task":
      top = addFillerHeader(top, i)
    top = top.rightmost().down().rightmost().down()

  top = top.rightmost().append(headerToProjectJson(headerBlock))

  return zipper.list(top.root())

isTaskRegex = re.compile('\[.\] .*')
taskRegex = re.compile('\[(.)\] (.*)')
def isTask(item):
  task = pandocfilters.stringify(item)
  return isTaskRegex.match(task) != None

def taskToProjectJson(block):
  match = taskRegex.match(pandocfilters.stringify(block))

  isComplete = match.group(1) != " "
  name = match.group(2)

  return ["", name, "task", isComplete]

def addTask(top, block):
  top = top.rightmost_descendant()
  lasttype = top.leftmost().right().right().node()
  if lasttype == "task":
    top = top.up().up().rightmost().append(taskToProjectJson(block))
  else:
    top = top.rightmost().append(taskToProjectJson(block))

  return top

def addTasks(top, block):
  for item in block["c"]:
    if isTask(item):
      top = addTask(top, item)
    else:
      top = addToLastDescription(top, item)
  return top

def addToLastDescription(top, item):
  lastDescriptionLoc = top.rightmost_descendant().leftmost()
  description = lastDescriptionLoc.node()
  return lastDescriptionLoc.replace(description + markdownify(block) + "\n")


def toObjs(top):
  loc = top.leftmost_descendant()

  while loc:
    if type(loc.node()) == type([]):
      item = loc.node()
      if any(map(lambda x: type(x) == type({}), item)) or len(item) == 0:
        pass
      elif item[2] == "task":
        loc = loc.replace({
          "description": item[0],
          "name": item[1],
          "type": item[2],
          "complete": item[3]
        })
      else:
        loc = loc.replace({
          "description": item[0],
          "name": item[1] or "-- missing name --",
          "type": item[2],
          "contents": item[3]
        })

    n = loc.postorder_next()
    if n:
      loc = n
    else:
      return loc.root()


if __name__ == "__main__":
  for line in sys.stdin:
    doc = json.loads(line)

    projects = []
    top = zipper.list(projects)
    for block in doc[1]:
      if isHeader(block):
        top = addHeader(top, block)
        top = zipper.list(top.root())
      elif isList(block):
        top = addTasks(top, block)
        top = zipper.list(top.root())
      else:
        top = addToLastDescription(top, block)
        top = zipper.list(top.root())

    objs = toObjs(zipper.list(top.root()))
    if objs == []:
      objs = toObjs(addFillerHeader(zipper.list(top.root()), 1))
    json.dump(objs, sys.stdout)

