import pandas as pd
import yaml
import pydriller as pydrill
from git import Repo
import os
import subprocess
from pathlib import Path

def read_columns(url):
    data = pd.read_excel(url, engine='openpyxl')
    print(data)

repo_url = 'https://github.com/claranet/spryker-demoshop.git'
target_dir = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\spryker-demoshop'
LOG_FILE_PATH = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\log.txt'

def clone_repo(url, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        return 
    repo = Repo.clone_from(url, target_dir)
    return repo

def get_default_branch(repo_path):
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

def locate_json_files(workdir):
    json_files = []
    for extensions in ('*.json'):
        json_files.extend(Path(workdir).rglob(extensions))
    return json_files

def print_yaml_files(workdir):
    res = []
    empty_dict = {"dir_path": [], "sub_dir_paths": [], "yml_file_names": []}
    for (dir_path, dir_names, file_names) in os.walk(workdir):
        empty_dict["dir_path"].append(dir_path)
        empty_dict["sub_dir_paths"].extend(dir_names)
        empty_dict["yml_file_names"].extend(file_names)

        for file_name in file_names:
            if file_name[-4:] == ".yml":
                res.append(file_name)
    return res

def print_json_files(workdir):
    res = [] 
    for (dir_path, dir_names, file_names) in os.walk(workdir):
        for file_name in file_names:
            if file_name.endswith('.json'):  # Correct filtering for json files
                res.append(os.path.join(dir_path, file_name))
    return res

def write_list_to_file(file_path, lst):
    with open(file_path, 'a') as file:  # Open in append mode
        for item in lst:
            file.write(f"{item}\n")

def write_to_file(file_path, text):
    with open(file_path, 'a') as file:  # Open in append mode
        file.write(text + '\n')

def main(): 
    file_path = 'output.txt'
    text = 'Hello, this is a sample text written to a file.'

    new_repo = clone_repo(repo_url, target_dir)
    default_branch = get_default_branch(target_dir)
    write_to_file(file_path, f"default branch: {default_branch}")

    yaml_files_directory = locate_yaml_files(target_dir)
    list_of_yaml_files = print_yaml_files(target_dir)
    json_files_directory = locate_json_files(target_dir)
    list_of_json_files = print_json_files(target_dir)

    read_columns('P.U_merged_filtered - Final_merged_only_not_excluded_yes_ms_unarchived_commit_hash v2.0.xlsx')

    write_to_file(file_path, text)

    write_to_file(file_path, "yaml files directory")
    write_list_to_file(file_path, yaml_files_directory)

    write_to_file(file_path, "list of yaml files")
    write_list_to_file(file_path, list_of_yaml_files)

    write_to_file(file_path, "json files directory")
    write_list_to_file(file_path, json_files_directory)

    write_to_file(file_path, "list of json files")
    write_list_to_file(file_path, list_of_json_files)

main()
