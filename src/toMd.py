#!/usr/bin/python

import sys
import json
import pandocfilters

from sh import pandoc


# In: project json
# Out: pandoc json

if __name__ == "__main__":
  for line in sys.stdin:
    projects = json.loads(line)

    headers = []
    for project in projects:
      project_name = "# " + project["name"]
      for chunk in pandoc(["-f", "markdown", "-t", "json"], _in=project_name ):
        header = json.loads(chunk)[1][0]
        headers.append(header)
        sys.stderr.write(str(header) + "\n#####\n")

    doc = [{"unMeta": {}}, headers]
    json.dump(doc, sys.stdout)

  sys.stdout.flush()
  sys.stdout.close()
