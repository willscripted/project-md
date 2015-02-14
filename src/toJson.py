#!/usr/bin/python

import sys
import json

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

def level(block):
  return block["c"][0]

def headerToProjectJson(block):
  name = pandocfilters.stringify(block["c"][2])
  jsonType = levelToType[level(block)]
  return ["", name, jsonType, []]

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
  return zipper.list(top.rightmost().append(fillers[level]).root())

def addHeader(top, headerBlock):
  for i in range(1, level(headerBlock)):
    if top.rightmost().node() == []:
      top = addFillerHeader(top, i)
    top = top.rightmost().down().down()

  top = top.rightmost().append(headerToProjectJson(headerBlock))

  return zipper.list(top.root())


if __name__ == "__main__":
  for line in sys.stdin:
    doc = json.loads(line)

    projects = []
    top = zipper.list(projects)
    for block in doc[1]:
      if isHeader(block):
        top = addHeader(top, block)
        top = zipper.list(top.root())
      else:
        lastDescriptionLoc = top.rightmost_descendant().leftmost()
        description = lastDescriptionLoc.node()
        top = zipper.list(lastDescriptionLoc.replace(description + markdownify(block)).root())



    json.dump(top.root(), sys.stdout)


# TODO
## while more_nodes
#    if header:
#      from top, find-or-add each successive header until desired depth is reached
#    else if contains_tasks
#      add tasks
#    else
#      Add to description of last (header or task)
