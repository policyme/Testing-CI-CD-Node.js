'''Module for parsing git log commit messages'''
import subprocess
import re

LEADING_4_SPACES = re.compile('^    ')

def get_commits():
  lines = subprocess.check_output(
    ['git', 'log'], stderr=subprocess.STDOUT
  ).decode("utf-8").split('\n')
  commits = []
  current_commit = {}

 # Saves the cureent commit message into the data structure
  def save_current_commit():
    title = current_commit['message'][0]
    current_commit['title'] = title
    commits.append(current_commit['title'])

  # Iterating through all the git log messages
  # and extracting only the messages
  for line in lines:
    if not line.startswith(' '):
      if line.startswith('commit '):
        if current_commit:
          save_current_commit()
          current_commit = {}
      else:
        try:
          key, value = line.split(':', 1)
          current_commit[key.lower()] = value.strip()
        except ValueError:
          pass
    else:
      current_commit.setdefault(
        'message', []
      ).append(LEADING_4_SPACES.sub('', line))
  if current_commit:
    save_current_commit()
  return commits
