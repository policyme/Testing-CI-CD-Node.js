'''Module for searching and returning the path of the _version.py and package.json file'''
import subprocess
import os
from subprocess import run, PIPE, STDOUT

COMMIT_MESSAGE = "Updating CHANGELOG.md and bumping the dev version [skip ci]"
CHANGELOG_FILE = "CHANGELOG.md"

# Logic to search for _version.py file and the package.json file
def find_version_path():
  for content in os.listdir(os.getcwd()):
    # Finding the package.json file
    if os.path.isfile(content):
      if content == "package.json":
        return os.getcwd() + '/' + content
    elif os.path.isdir(content):
      # Finding _version.py file
      for files in os.listdir(os.getcwd() + '/' + content):
        if files == '_version.py':
          return os.getcwd() + '/' + content + '/' + files

# runs subprocess. tracks stdout/stderr
def exec_subprocess(cmd):
  result = run(cmd, stdout=PIPE, stderr=STDOUT, shell=True,
               check=True, encoding='utf-8', executable='/bin/bash')
  print('exec_subprocess result:\n{}\n'.format(result.stdout))
  if result.returncode != 0:
    raise Exception("subprocess did not run successfully. See logs for details")

# gets the ticket number from the string text
def get_ticket_number(text):
  parsed_message = text.split('-')
  if len(parsed_message) > 1:
    ticket_type = parsed_message[0].upper()
    ticket_number = parsed_message[1]
    if ticket_number.isdigit():
      return ticket_type + '-' + ticket_number
  return None
