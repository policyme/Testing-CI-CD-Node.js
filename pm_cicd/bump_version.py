'''Module having the logic for bumping the dev version'''
import os
import sys
import git
sys.path.insert(0, os.getcwd())
from package._version import VERSION as version

def bump_version_py(branch):
  # The version variable from the project
  VERSION = version

  # Hack to prevent the execution of the rest of the script
  repo = git.Repo(search_parent_directories=True)

  # The first message of git log should be a merge pull request
  merge_message = repo.head.object.message

  if branch == "develop":

    if merge_message.split(" ")[0] == 'Merge':

      parse_version = VERSION.split('-')

      if len(parse_version) == 1:
        # Need to append "-dev-1" to it
        VERSION += "-dev-1"
      else:
        # Increment the dev version number
        parse_version[2] = str(int(parse_version[2]) + 1)
        VERSION = ""
        # Keeps the version same but increments the dev version
        VERSION += parse_version[0] + '-' + parse_version[1] + '-' + parse_version[2]


      # Writing contents to the changelog file
      f = open("package/_version.py", "a+")

      # Erasing the contents of the file
      f.truncate(0)

      # Adding the version number and the JIRA ticket number
      contents = 'VERSION=' + "'" +  VERSION + "'" + '\n\n\n'

      # Bumping the version
      f.write(contents)

      # CLosing the file
      f.close()

def bump_version_js(branch):
  pass