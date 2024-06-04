#import necessities 
import csv
import shutil
import git
from git import Repo
import os
import pandas as pd
import yaml

import pydriller as pydrill
from pydriller import Repository

import subprocess
from pathlib import Path
links_dict = {}
classification_dict = {}

#pulls 3 elements at a time, delete processed keys from dictionary
def process_in_chunks(links_dict, chunk_size=3):
    keys = list(links_dict.keys())[:chunk_size]  # Get the first chunk_size keys

    for key in keys:
        print(f"Processing {key}: {links_dict[key]}")
        # Add your processing logic here
        process_three_repos(keys)
    # Remove processed items from the dictionary
    for key in keys:
        del links_dict[key]

    print("Remaining dictionary items after processing:")
    print(links_dict)

def clone_repo(url, target_dir): #clones directory to target directory 
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        return 
    repo = Repo.clone_from(url, target_dir)
    return repo
    
def delete_repo(target_dir):
    # Deletes the cloned repository from the target directory
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        print(f"Deleted repository at {target_dir}")
    else:
        print(f"No repository found at {target_dir} to delete")

def process_three_repos(keys):
    for key in keys:
        
        repo_url = key
        print(f"Processing repo URL: {repo_url}")
        str  = "" + links_dict[key]
        target_dir = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\\' + str
        print(f"Target directory: {target_dir}") 
        LOG_FILE_PATH = r'C:\Users\camyi\OneDrive\Documents\ClonedRepos\log.txt'
        clone_repo(repo_url, target_dir)
        classification_dict[repo_url] = "done"
        print(classification_dict)
        #delete_repo(target_dir)
        # Add your repository processing logic here

#opens csv, appends github link and file path identifier to a dictionary, the prints it. 
def open_csv_file():
    # Define the path to the CSV file
    csv_file_path = 'P.U_merged_filtered - Final_merged_only_not_excluded_yes_ms_unarchived_commit_hash v2.0.csv'
    
    
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            print(f"Trying encoding: {encoding}")
            with open(csv_file_path, mode='r', newline='', encoding=encoding) as file:
                csv_reader = csv.reader(file)
                
                # Print the first column of each row in the CSV file
                for row in csv_reader:
                    if row:  # Check if the row is not empty
                        first_column = row[0]  # Get the first column value
                        print(first_column)
                        identifier = get_github_link_identifier(first_column)
                        if identifier!=None:
                            links_dict[first_column] = identifier
            break  # Exit the loop if no error occurs
        except UnicodeDecodeError as e:
            print(f"Encoding {encoding} failed: {e}")
        except FileNotFoundError:
            print(f"Error: The file '{csv_file_path}' does not exist.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    # Print the dictionary
    print("Links and their identifiers:")
    for first_column, identifier in links_dict.items():
        print(f"{first_column}: {identifier}")

#extracts the identifer from the github link and switches all / to \ to get the file path iden
def get_github_link_identifier(url):
    prefix = 'https://github.com/'
    if prefix in url:
        identifier = url.split(prefix)[1]
        identifier = identifier.replace('/', '\\')
        print(f"Identifier: {identifier}")
        return identifier  # Ensure the identifier is returned
    else:
        print("Prefix not found in URL")

def main():
    print('begin')
    open_csv_file()
    #process all elements 3 at a time until they the dictionary has none left
    
    process_in_chunks(links_dict,3)

main()
