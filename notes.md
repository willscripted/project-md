
clean mardown file:

    pandoc -t json -s <in-file.md> | pandoc -f json -t markdown > <out-file.md>
