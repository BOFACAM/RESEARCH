import pandas as pd
from git import Repo
import os
import subprocess
import shutil
import stat
from tqdm import tqdm
import json



LOG_FILE_PATH = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\log.txt'

#lets define the file extensions
IAC_TOOLS = {
    'Terraform': ['.tf', '.tf.json'],#  we might have to look at like specific files within the directories of the repo that each tool must have? or most likely has?
    'Pulumi': ['.yaml', '.yml',],
    'Crossplane': ['.yaml', '.yml'],
    'AWS CloudFormation': ['.yaml', '.yml', '.json'],
    'Azure Resource Manager': ['.json'],
    'Google Cloud Deployment Manager': ['.yaml'],
    'Ansible': ['.yaml', '.yml'],
    'Chef': ['.rb'],
    'Puppet': ['.conf', '.pp'], #im gonna have to include full extension like puppet.conf
    'SaltStack': ['.sls'],
    'Bicep': ['.bicep'],
    'OpenTofu': ['.tf', '.tf.json'],
    'Vagrant': ['.vm', '.ssh', '.winrm', '.winssh', '.vagrant'],
    'Docker Compose': ['.yaml', '.yml']  
}


UNIQUE_KEYS = {
    'Terraform': ['resource', 'provider', 'variable', 'output', 'data','locals'],
    'Pulumi': ['name', 'runtime', 'description', 'config', 'main'],
    'Crossplane': ['apiVersion', 'kind', 'metadata', 'spec'],
    'AWS CloudFormation': ['AWSTemplateFormatVersion', 'Resources', 'Outputs'],
    'Azure Resource Manager': ['$schema', 'contentVersion', 'resources'],
    'Google Cloud Deployment Manager': ['resources', 'imports'],
    'Ansible': ['name', 'hosts', 'vars', 'tasks'],
    'Chef': ['file', 'name', 'action'],
    'Puppet': ['file', 'service', 'package', 'node', 'class'],
    'SaltStack': ['pkg.installed', 'service.running', 'file.managed'],
    'Bicep': ['targetScope', 'param', 'var', 'resource', 'module', 'output'],
    'OpenTofu': ['resource', 'module', 'provider'],
    'Vagrant': ['Vagrant.configure', 'config.vm.box', 'config.vm.network'],
    'Docker Compose': ['version', 'services', 'volumes', 'networks'] 
}


def get_home_directory(): #this should just return like your basic home directory this should not matter as we are deleting 

    return os.path.expanduser("~")

def process_dataframe(csv):
    home_dir = get_home_directory()
    data = pd.read_csv(csv)
    results = []
    iac_dataset = {}
    for index,rows in tqdm(data.iterrows(),total = data.shape[0],desc= "Processing REPOS"):
        repo_url = rows["URL"]
        identifer = rows["Identifier"]
        target_dir = os.path.join(home_dir,identifer.replace('/', '\\'))
        clone_repo(repo_url,target_dir)

        list_of_possible,found_extensions = store_extenstion_format_files(target_dir,repo_url)

        iac_dataset[identifer] = {
            'id':identifer,
            'url' : repo_url,
            'found_extensions': found_extensions,
            'files' : list_of_possible

        }

        #tools_used = identify_iac_tools(target_dir)
        #results.append({'Identifier': identifer, 'Possible IAC Tools Used':tools_used})

        #shutil.rmtree(target_dir,onerror=onerror)
        os.rmdir(target_dir)
    
    with open('iac_dataset.json','w') as json_file:
        json.dump(iac_dataset,json_file,indent= 1)
        
    
    


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


"""def identify_iac_tools(work_dir):
    tools_found = set()
    for (dir_path, __, file_names) in os.walk(work_dir):
        for file_name in file_names:
            file_ext = os.path.splitext(file_name)[1] # 0 is the root and then the [1] is extension when you use splittext
            file_path =os.path.join(dir_path,file_name)
            for tool,extensions in IAC_TOOLS.items():
                if file_ext in extensions:
                    if identify_tool_by_template(tool,file_path):#compare the tool template to the file that we get per file path
                        tools_found.add(tool)
    return list(tools_found)

def identify_tool_by_template(tool, file_path):
    patterns = UNIQUE_KEYS.get(tool,[])
    with open(file_path,'r',encoding= 'utf-8') as file:
        template = file.read()
        for pattern in patterns:
            if pattern in template:
                return True"""

def store_extenstion_format_files(work_dir,repo_url): # should return a dict holding all of the possible iac format files based off extensions?
    list_of_file_names_per_repo =[]
    found_extensions =set()
    for dir_path,__,file_names in os.walk(work_dir):
        for file_name in file_names:
            file_ext = os.path.splitext(file_name)[1]
            file_path = os.path.join(dir_path,file_name)
            for extensions in IAC_TOOLS.values():
                if file_ext in extensions:
                    found_extensions.add(file_ext)
                    github_path = file_path.replace(work_dir,repo_url)
                    list_of_file_names_per_repo.append(github_path)
    return list_of_file_names_per_repo,list(found_extensions)

    


def main(): 
    process_dataframe("samplecsv5.csv")

main()

