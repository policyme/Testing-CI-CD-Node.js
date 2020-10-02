'''Module having the logic for bumping the dev version'''
import os
import sys
import json
import git
from pm_cicd.helpers import find_version_path
sys.path.insert(0, os.getcwd())

def format_version(version):
  # Hack to prevent the execution of the rest of the script
  repo = git.Repo(search_parent_directories=True)

  # The first message of git log should be a merge pull request
  merge_message = repo.head.object.message

  if merge_message.split(" ")[0] == 'Merge':
    parse_version = version.split('-')

    if len(parse_version) == 1:
      # Need to append "-dev-1" to it
      version += "-dev-1"
    else:
      # Increment the dev version number
      parse_version[2] = str(int(parse_version[2]) + 1)
      version = ""
      # Keeps the version same but increments the dev version
      version += parse_version[0] + '-' + parse_version[1] + '-' + parse_version[2]

    return version

  # Do not bump dev version
  return None


def bump_version_py(branch):
  if branch == "gabe-test":
    # Importing the required version variable
    path = find_version_path()

    # Opening the _version.py file
    f = open(path)
    package_contents = f.read()
    package_contents = package_contents.replace('\'', '')
    version = package_contents.split("=")[1]
    f.close()

    # The version variable from the project
    VERSION = format_version(version)
    print('New Version: {}'.format(VERSION))

    if VERSION is not None:
      # Writing contents to the changelog file
      f = open(path, "a+")

      # Erasing the contents of the file
      f.truncate(0)

      # Adding the version number and the JIRA ticket number
      contents = 'VERSION=' + "'" +  VERSION + "'" + '\n\n\n'

      # Bumping the version
      f.write(contents)

      # CLosing the file
      f.close()


def bump_version_js(branch):
  if branch == "gabe-test":
    # Opening the pacjage.json file
    path = find_version_path()
    f = open(path)

    # Loading the contents of the file
    parsed_json = json.load(f)

    # Determining the new version
    VERSION = format_version(parsed_json['version'])

    if VERSION is not None:
      # Updating the version
      parsed_json['version'] = VERSION

      # Dumping the updated json into the package.json file
      with open(path, 'w') as fp:
        json.dump(parsed_json, fp, indent=2)
