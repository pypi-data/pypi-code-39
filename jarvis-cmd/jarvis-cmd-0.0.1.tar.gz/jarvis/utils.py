"""
  Desc: Set of utility functions
"""
from os import path, makedirs
from constants import jarvis_config_home, openproject_config_file

def create_if_doesnt_exist(file_path):
  if not path.exists(file_path):
    open(file_path, 'a').close()

def check_folder_and_files():
  if not path.exists(jarvis_config_home):
    makedirs(jarvis_config_home)
  create_if_doesnt_exist(openproject_config_file)