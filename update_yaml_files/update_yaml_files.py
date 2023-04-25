import argparse
import ruamel.yaml
import glob


def parse_args():
    # Parse input argument to script (which should contain path to folder)
    parser=argparse.ArgumentParser(description="a script to update yaml files in a directory")
    parser.add_argument("-p", "--path", help="Fully qualified path to directory containing yaml files")
    args=parser.parse_args()

    print("returning args")
    return args


def list_yaml_files(folder_path):
    # Retrieve all yml files in directory and return them as a list
    files = glob.glob(folder_path + "/" + "*.yml")
    return files


def update_yml_file(yml_file):
    # Leverage ruamel.yaml to read the yaml file (*.yml extension), check if the "partitions" field is equal to [], and update it accordingly (to empty)
    # Write the result back to the same yaml file
    yaml = ruamel.yaml.YAML()
    # yaml.preserve_quotes = True

    print("opening yaml file")
    with open(yml_file) as fp:
        data = yaml.load(fp)

    # Retrieving sources in yaml file and iterate to find partition file
    print("iterating on sources within yaml")
    sources = data["sources"]
    for source in sources:

        # Within each source, check the available tables and iterate on them
        print("iterating on tables within the source")
        tables = source["tables"]
        for table in tables:

            # Check if the partitions field is equal to [], if so make it empty
            print("checking if partitions is equal to []")
            if table["external"]["partitions"] == []:
                print("indeed it is equal to [] so let's make it an empty string")
                table["external"]["partitions"] = None

    print("done iterating")
    print("final data check and dumping the output yaml before writing back to the file")
    print(data)

    # Write to yaml file
    with open(yml_file, 'w') as fp:
        yaml.dump(data, fp)
    

def main():
    # Parse input args, retrieve the list of yaml files (from provided directory path), and update the yml files accordingly (for partitions from [] to empty)
    inputs=parse_args()

    print("retrieving yaml files from path")
    yml_files = list_yaml_files(inputs.path)

    print("beginning the yml update process")
    for yml_file in yml_files:
        update_yml_file(yml_file)
    
    print("script complete - please double check the results")


if __name__ == "__main__":
    print("Kicking off update_yaml_files.py script")
    main()