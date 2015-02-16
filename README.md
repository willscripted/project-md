
Project Markdown  - Parsable Todo Lists
===========

##### `${GIT_ROOT}/.todo`

    # Project Name

    Short description of project.

    ## Some objective

    Description of the objective.

    ```
    .example(codeBlock);
    ```

    [ ] Task 1
    [ ] Task 2
    [ ] Task 3

    Description of `Task 3`

    ## Another objective

    [x] Task 4
    [x] Task 5
    [ ] Task 6


Convert to JSON

```
cat .todo | ./bin/toJson
```

#### JSON

```
{
  "name": "Project Name",
  "type": "project",
  "description": "Short description of *project*.",
  "contents": [
    {
      "name": "Some Objective",
      "type": "objective",
      "description": "Description of the _objective_.\n\n```\n.example(codeBlock);\n```\n",
      "contents": [
        {"type": "task", "name": "Task 1", "complete": false, "description": ""},
        {"type": "task", "name": "Task 2", "complete": false, "description": ""},
        {"type": "task", "name": "Task 3", "complete": false, "description": "Description of `Task 3`"}
      ]
    },
    {
      "name": "Another Objective",
      "type": "objective",
      "description": "",
      "contents": [
        {"type": "task", "name": "Task 4", "complete": true, "description": ""},
        {"type": "task", "name": "Task 5", "complete": true, "description": ""},
        {"type": "task", "name": "Task 6", "complete": false, "description": ""}
      ]
    }
  ]
}
```

Convert back to Markdown

```
cat project.json | ./bin/toMd
```

    Project Name
    ============

    Short description of project.

    Some objective
    ------------

    Description of the objective.

    ```
    .example(codeBlock);
    ```

     - [ ] Task 1
     - [ ] Task 2
     - [ ] Task 3

      Description of `Task 3`

    Another objective
    ------------

     - [x] Task 4
     - [x] Task 5
     - [ ] Task 6



## Demo

Run demo on port 3000.

```
make run
```



# License

Copyright 2015 Will O'Brien

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

