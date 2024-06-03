import pandas as pd
import yaml
import pydriller as pydrill
from git import Repo
import os
import subprocess
from pathlib import Path
import shutil
import stat


LOG_FILE_PATH = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\log.txt'

#lets define the file extensions
IAC_TOOLS = {
    'Terraform': ['.tf', '.tf.json'],
    'Pulumi': ['.yaml', '.yml', '.ts', '.js', '.py', '.cs'],
    'Crossplane': ['.yaml', '.yml'],
    'AWS CloudFormation': ['.yaml', '.yml', '.json'],
    'Azure Resource Manager': ['.json'],
    'Google Cloud Deployment Manager': ['.yaml'],
    'Ansible': ['.yaml', '.yml'],
    'Chef': ['.rb'],
    'Puppet': ['.conf', '.pp'],
    'SaltStack': ['.sls'],
    'Bicep': ['.bicep'],
    'OpenTofu': ['.tf', '.tf.json'],
    'Vagrant': ['.vm', '.ssh', '.winrm', '.winssh', '.vagrant']
}


def get_home_directory(): #this should just return like your basic home directory this should not matter as we are deleting 

    return os.path.expanduser("~")

def process_dataframe(csv):
    home_dir = get_home_directory()
    data = pd.read_csv(csv)
    for index,rows in data.iterrows():
        repo_url = rows["URL"]
        identifer = rows["Identifier"]
        target_dir = os.path.join(home_dir,identifer.replace('/', '\\'))
        clone_repo(repo_url,target_dir)
        get_default_branch(target_dir)

        list_of_yaml_files = print_yaml_files(target_dir)
        print(f"Identifer:{identifer}, FILES:{list_of_yaml_files}") 

        shutil.rmtree(target_dir,onerror=onerror)
      

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read-only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage: ``shutil.rmtree(path, onerror=onerror)``
    """
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise




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


"""def locate_yaml_files(workdir):
    yaml_files = []
    for extensions in ('*.yml', '*.yaml'):
        yaml_files.extend(Path(workdir).rglob(extensions))
    return yaml_files"""

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
    return res


def main(): 
    process_dataframe("samplecsv.csv")

main()


