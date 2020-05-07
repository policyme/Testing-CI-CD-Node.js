'''Module with the logic for generating changelog'''
import os
import sys
from datetime import date
from get_commit_log import get_commits
sys.path.insert(0, os.getcwd())
# from package._version import VERSION

def gen_changelog():
  '''Function to generate the changelog'''

  today = date.today()
  # dd/mm/YY
  d1 = today.strftime("%Y/%m/%d")

  # Returns true if the commit message starts with 'Merge pull request *'
  def is_pull_request(commit):
    parse_array = commit.split(" ")
    if parse_array[0] == 'Merge' and parse_array[1] == 'pull' and parse_array[2] == 'request':
      return True
    return False

  # Getting all the commits from git log
  commits = get_commits()

  # Making a set of ticket number
  ticket_number = set()


  if is_pull_request(commits[0]):

    contents = ''

    # Getting the version number
    version = '1.0.0'

    # Adding the version number and the JIRA ticket number
    contents += '# ' + version + ' (' + d1 + ')' + '\n\n'

    for commit in commits:
      if commit != "Updating the CHANGELOG.md and the _version file":
        if is_pull_request(commit):
          # Extracting the ticket number
          parsed_message = commit.split(' ')[5].split('/')[2].split('-')
          parsed_message[0:2] = ['-'.join(parsed_message[0:2])]
          ticket_number.add(parsed_message[0])
          parsed_message = ''
      else:
        break


    # Opening the file

    for ticket_numbers in ticket_number:

      # Link to ticket on JIRA
      jira_link = 'https://policyme.atlassian.net/browse/' + ticket_numbers

      # Adding the version number and the JIRA ticket number
      contents += '* ' + jira_link + '\n'
      jira_link = ''

    # Writing to the CHANGELOG.md file
    with open("../CHANGELOG.md", 'r+') as f:
      prev_content = f.read()
      # Prepends the contents to the top of the file
      f.seek(0, 0)
      # Write the contents into the file
      f.write(contents + '\n' + prev_content)
      # Closes the file
      f.close()
