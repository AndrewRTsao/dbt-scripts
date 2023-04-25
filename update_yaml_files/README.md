# What does this script do?

Leverages the [ruamel.yaml](https://pypi.org/project/ruamel.yaml/) package to programmatically read a set of YAML files in a specified directory, check if the `partitions` property is set to `[]`, and make it empty. 

This script is meant to be a starting point but can easily be adapted to update any property in your YAML files programmatically if you need to mass update these values. A couple things to note:
- Check the version of python being used to make sure it's compatible with ruamel.yaml
- Script requires passing in the fully qualified path to the directory containing the YAML files you wish to update (don't include the `/` at the end of the folder path)
- Only checks for files with `*.yml` extensions and accepts only one directory as an input

# How can I use this script? 

Make sure that you have the correct dependencies installed (i.e. requirements.txt). Then, use the following command:

```python
python update_yaml_files.py -p /full/path/to/folder
```