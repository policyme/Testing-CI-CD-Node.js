'''Module with the logic for generating changelog'''
import os
import sys
from datetime import date

from pm_cicd.utils.consts import (
  CHANGELOG_FILE,
  BRANCHES
)

from pm_cicd.utils.helpers import (
  get_commit_message,
  get_ticket_number,
  is_merge_pull_request
)
from pm_cicd.utils.get_commit_log import get_commits

sys.path.insert(0, os.getcwd())

# creates/appends content to changelog
def add_to_changelog(contents):
  print('writing to changelog:\n{}'.format(contents))
  # create file if it doesn't exist
  if not os.path.exists(CHANGELOG_FILE):
    open(CHANGELOG_FILE, 'a').close()

  # add contents to the changelog
  with open(CHANGELOG_FILE, 'r+') as f:
    prev_content = f.read()
    # Prepends the contents to the top of the file
    f.seek(0, 0)
    # Write the contents into the file
    f.write(contents + '\n' + prev_content)
    # Closes the file
    f.close()

def gen_changelog(path, new_version):
  '''Function to generate the changelog'''
  today = date.today()
  # dd/mm/YY
  d1 = today.strftime("%Y/%m/%d")

  # Getting all the commits from git log
  commits = get_commits()

  # Making a set of ticket number
  ticket_numbers = set()

  if is_merge_pull_request(commits[0]):
    contents = ''

    # Removing extra tabs if present in the version
    version = new_version.replace('\n', '')

    # Adding the version number and the JIRA ticket number
    contents += '## ' + version + ' (' + d1 + ')' + '\n\n'

    for commit in commits:
      if commit != get_commit_message(BRANCHES.MASTER.value):
        if is_merge_pull_request(commit):
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
        # no need to read the rest of the commits
        break

    # Opening the file
    for ticket_number in ticket_numbers:
      # Link to ticket on JIRA
      jira_link = 'https://policyme.atlassian.net/browse/' + ticket_number

      # Adding the version number and the JIRA ticket number
      contents += '* [' + jira_link + '](' + jira_link + ')\n'

    add_to_changelog(contents)
