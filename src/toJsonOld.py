#!/usr/bin/python

import sys
import json

import zipper

import pandocfilters

missingHeaders = [
        {},
  {"description":"", "content": [], "type": "projcet", "name": "-- Missing Project Title --"},
  {"description":"", "content": [], "type": "objective", "name": "-- Missing Objective Title --"},
  {"description":"", "content": [], "type": "objective", "name": "-- Missing Sub-Objective Title --"},
  {"description":"", "content": [], "type": "objective", "name": "-- Missing Sub-Objective Title --"},
  {"description":"", "content": [], "type": "objective", "name": "-- Missing Sub-Objective Title --"},
  {"description":"", "content": [], "type": "objective", "name": "-- Missing Sub-Objective Title --"}
]

def isHeader(item):
  return item["t"] == "Header"

# Last content at level 0 is tree
# Last content at level 1 is
#   
# 
# Last content at level 2 is tree
# Last content at level 3 is tree
# 
def getLastContentAtLevel(tree, level):
  if level < 1:
    return tree
  if level == 1:
    # Add project if it is missing
    if len(tree) == 0:
      tree.append(missingHeaders[level])
      return tree[-1]["content"]
  else:
    # Add all higher levels
    oneUpContent = getLastContentAtLevel(tree, level - 1)

    # Add this level
    if len(oneUpContent) == 0:
      oneUpContent.append(missingHeaders[level])

    # return this next highest level
    return oneUpContent[-1]["content"]

def last(tree, maxdepth=10):
  depth = 0
  if len(tree) == 0:
    getLastContentAtLevel(tree, 1)
  last = tree[-1]
  while True:
    depth += 1
    if depth == maxdepth:
      return last
    if len(last["content"]) == 0:
      return last
    else:
      last = last["content"][-1]


if __name__ == "__main__":
  for line in sys.stdin:
    doc = json.loads(line)

    def reducer(acc, item):
      json.dump(item, sys.stderr)
      sys.stderr.write("\n\n-------\n\n")
      if isHeader(item):
        level = item["c"][0]
        lastContent = getLastContentAtLevel(acc, item["c"][0] - 1)
        lastContent.append({
            "name": pandocfilters.stringify(item["c"]),
            "description": "",
            "type": "project", # TODO change me
            "content": []
        })
      else:
        lastProjectMdNode = last(acc)
        # json.dump(lastProjectMdNode, sys.stderr)
        lastProjectMdNode["description"] += pandocfilters.stringify(item)
      return acc

    things = reduce(reducer, doc[1], [])
    json.dump(things, sys.stdout)

    # for block in doc[1]:
    #   if block["t"] == "Header" and block["c"][0] == 1:
    #     altered["name"] = pandocfilters.stringify(block["c"])
    #     altered["type"] = "project"
    #     altered["description"] = ""
    #     altered["content"] = []
    #     # json.dump(altered, sys.stdout)

  sys.stdout.flush()
  sys.stdout.close()



# TODO
## while more_nodes
#    if header:
#      from top, find-or-add each successive header until desired depth is reached
#    else if contains_tasks
#      add tasks
#    else
#      Add to description of last (header or task)
