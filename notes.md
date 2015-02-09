
clean mardown file:

    pandoc -t json -s <in-file.md> | pandoc -f json -t markdown > <out-file.md>


### toMd

- Accepts project json
- Converts project json to pandoc json
- Converts pandoc json to Markdown


### toJson

- Accepts Markdown
- Converts markdown to pandoc json
- Converts pandoc json to project json

### Clean

- Accepts Markdown
- Converts to project JSON (toJson)
- Converts back to Markdown (toMd)
