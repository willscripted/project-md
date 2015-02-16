#!/usr/bin/python

import sys
import json
import pandocfilters

from sh import pandoc


# In: project json
# Out: markdown

def getHeader(item, level):
  newline = "\n" if level > 1 else ""
  prefix = newline + "#" * level
  header = prefix + " " + item["name"]
  return header

def itemToMd(item, level=1):
  text = ""
  if item["type"] == "task":
    complete = "x" if item["complete"] == True else " "
    text += "- [" + complete + "] " + item["name"]
    if item["description"] != "":
      text+= "\n\n" + item["description"]
  else:
    text += getHeader(item, level) + "\n"
    if item["description"] != "":
      text += "\n" + item["description"]
    for subitem in item["content"]:
      text += "\n" + itemToMd(subitem, level + 1)

  return text

if __name__ == "__main__":
  js = ""
  for line in sys.stdin:
    js += line

  if js != "":
    projects = json.loads(js)

    mdText = ""
    for project in projects:
      mdText += itemToMd(project)

    sys.stdout.write(mdText)

  sys.stdout.flush()
  sys.stdout.close()
