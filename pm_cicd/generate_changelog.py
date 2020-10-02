'''Module with the logic for generating changelog'''
import os
import sys
from datetime import date
import json
from pm_cicd.helpers import find_version_path, COMMIT_MESSAGE, get_ticket_number
from pm_cicd.get_commit_log import get_commits
sys.path.insert(0, os.getcwd())

# Returns true if the commit message starts with 'Merge pull request *'
def is_pull_request(commit):
  parse_array = commit.split(" ")
  if parse_array[0] == 'Merge' and parse_array[1] == 'pull' and parse_array[2] == 'request':
    return True
  return False

def gen_changelog(lang):
  '''Function to generate the changelog'''
  today = date.today()
  # dd/mm/YY
  d1 = today.strftime("%Y/%m/%d")

  # Getting all the commits from git log
  commits = get_commits()

  # Making a set of ticket number
  ticket_numbers = set()

  if is_pull_request(commits[0]):
    contents = ''
    version = ''

    if lang == 'py':
      # It's a python project
      path = find_version_path()

      # Opening the _version.py file
      f = open(path)
      package_contents = f.read()
      package_contents = package_contents.replace('\'', '')
      version = package_contents.split("=")[1]
      f.close()
    elif lang == 'js':
      # It's a javascript project
      path = find_version_path()

      # Opening the package.json file
      f = open(path)

      # Loading the contents of the file
      parsed_json = json.load(f)

      # Determining the new version
      version = parsed_json['version']

    # Removing extra tabs if present in the version
    version = version.replace('\n', '')

    # Adding the version number and the JIRA ticket number
    contents += '## ' + version + ' (' + d1 + ')' + '\n\n'

    for commit in commits:
      if commit != COMMIT_MESSAGE:
        if is_pull_request(commit):
          # Extracting the ticket number
          tokens = commit.split(' ')
          if len(tokens) > 5:
            tokens = tokens[5].split('/')
            if len(tokens) > 2:
              ticket_string = tokens[2]
              ticket = get_ticket_number(ticket_string)
              if ticket is not None:
                ticket_numbers.add(ticket)
      else:
        break

    # Opening the file
    for ticket_number in ticket_numbers:
      # Link to ticket on JIRA
      jira_link = 'https://policyme.atlassian.net/browse/' + ticket_number

      # Adding the version number and the JIRA ticket number
      contents += '* [' + jira_link + '](' + jira_link + ')\n'

    print('writing to changelog:\n{}'.format(contents))
    # Writing to the CHANGELOG.md file
    with open("./CHANGELOG.md", 'r+') as f:
      prev_content = f.read()
      # Prepends the contents to the top of the file
      f.seek(0, 0)
      # Write the contents into the file
      f.write(contents + '\n' + prev_content)
      # Closes the file
      f.close()
