import pandas as pd
import yaml
import pydriller as pydrill
from git import Repo
import os
import subprocess
from pathlib import Path

#lets first read a xls file and get that url from the first column
# lets do one repo first
# https://github.com/claranet/spryker-demoshop


"""Let us try to read from the pre-defined spreadsheet and create a DF that gives us """
# https://docs.google.com/spreadsheets/d/1qgfrOlkIbml5htR9DPiV63Rh4ZWSebrJUOo9zRaN6MM/edit#gid=1867004712

def read_columns(url):
    data = pd.read_excel(url,engine ='openpyxl')
    print(data)


# Define the URL of the repository and the target directory
repo_url = 'https://github.com/claranet/spryker-demoshop.git'
target_dir = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\spryker-demoshop'
LOG_FILE_PATH = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\log.txt'


def clone_repo(url, target_dir): #clones directory to target directory 
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        return 
    repo = Repo.clone_from(url, target_dir)
    return repo


def get_default_branch(repo_path):
    """
    Identifies the default branch of the concerning repository
    """
    # Command to get the default branch name
    result = subprocess.run(["git", "remote", "show", "origin"], cwd=repo_path, text=True, capture_output=True)
    if result.returncode == 0:
        for line in result.stdout.split('\n'):
            if 'HEAD branch' in line:
                return line.split(':')[1].strip()
    else:
        print("--Failed to get default branch information")
        with open(LOG_FILE_PATH, 'a') as f:
            f.write(str("-- Failed to get default branch information") + ";" + repo_path + '\n')


def locate_yaml_files(workdir):
    yaml_files = []
    for extensions in ('*.yml', '*.yaml'):
        yaml_files.extend(Path(workdir).rglob(extensions))
    return yaml_files

def print_yaml_files(workdir):
        # list to store files name
    res = []
    empty_dict = {"dir_path": [], "sub_dir_paths": [], "yml_file_names": []}
    for (dir_path, dir_names, file_names) in os.walk(workdir):
        

        empty_dict["dir_path"].append(dir_path)
        empty_dict["sub_dir_paths"].extend(dir_names)
        empty_dict["yml_file_names"].extend(file_names)

        for file_name in file_names:

            if file_name[-4:] == ".yml":
                res.append(file_name)
    #print(empty_dict)
    return res


def main(): 
    new_repo = clone_repo(repo_url,target_dir)
    #print(new_repo)
    default_branch = get_default_branch(target_dir)
    #print(default_branch)

    yaml_files_directory = locate_yaml_files(target_dir)
    list_of_yaml_files = print_yaml_files(target_dir)
    read_columns(' Final_merged_only_not_excluded_yes_ms_unarchived_commit_hash v2.0.csv')
    # i guess we gotta change this into a csv link for us to use the read_csv function

    #print(yaml_files_directory)
    #print(list_of_yaml_files)

main()


