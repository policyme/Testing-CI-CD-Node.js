'''Module for searching and returning the path of the _version.py and package.json file'''
import os
import json
from subprocess import run

from pm_cicd.utils.consts import BRANCHES, BRANCH_TYPE, SKIP_BUMP
from pm_cicd.utils.consts import COLORS

# commit message
def get_commit_message(branch):
  if branch == BRANCHES.MASTER.value:
    return "Updating CHANGELOG.md and bumping the {} version [skip ci]".format(branch)
  return "Bumping the {} version [skip ci]".format(branch)

# checks if the project is python or js
def is_python_project():
  for content in os.listdir(os.getcwd()):
    # if found, then it is a nodejs project, otherwise python
    if os.path.isfile(content):
      if content == "package.json":
        return False
  return True

def get_forked_branch_type(commit):
  # e.g. Merge pull request #152 from glee-pm/feature/ST-1000-beanstalk-config
  if is_merge_pull_request(commit):
    for branch_type in BRANCH_TYPE.list():
      if '/{}/'.format(branch_type) in commit:
        return branch_type
  return None

# Returns true if the commit message starts with 'Merge pull request *'
# skip bump & changelog process if the commit contains skip autobump flag
def is_merge_pull_request(commit):
  parse_array = commit.split(" ")
  if SKIP_BUMP not in commit and parse_array[0] == 'Merge' and\
  parse_array[1] == 'pull' and parse_array[2] == 'request':
    return True
  return False

def find_version_relative_path():
  for content in os.listdir(os.getcwd()):
    # Finding the package.json file
    if os.path.isfile(content):
      if content == "package.json":
        return content
    elif os.path.isdir(content):
      # Finding _version.py file
      for files in os.listdir(os.getcwd() + '/' + content):
        if files == '_version.py':
          return content + '/' + files
  return None

# Logic to search for _version.py file and the package.json file
def find_version_path():
  return os.getcwd() + '/' + find_version_relative_path()

def get_version_py(path):
  version = None

  # Opening the _version.py file
  f = open(path)
  package_contents = f.read()
  package_contents = package_contents.strip().replace('\'', '')
  version = package_contents.split("=")[1]
  f.close()

  return version

def get_version_js(path):
  version = None
  f = open(path)

  # Loading the contents of the file
  parsed_json = json.load(f)

  # Determining the new version
  version = parsed_json['version']
  return version

# runs subprocess. tracks stdout/stderr
def exec_subprocess(raw_cmd):
  print(COLORS.CYAN + 'Running commands....' + COLORS.ENDC)
  for raw_line in cmd.split('\n'):
    line = raw_line.strip()
    print(COLORS.GREEN + '{}'.format(line) + COLORS.ENDC)
    run(line, check=True, shell=True, text=True)

# gets the ticket number from the string text
def get_ticket_number(text):
  parsed_message = text.split('-')
  if len(parsed_message) > 1:
    ticket_type = parsed_message[0].upper()
    ticket_number = parsed_message[1]
    if ticket_number.isdigit():
      return ticket_type + '-' + ticket_number
  return None
