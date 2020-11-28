'''Module having the logic for bumping the dev version'''
import os
import sys
import json
import git

from pm_cicd.utils.consts import (
  BRANCHES,
  BRANCH_TYPE,
  VERSION_SEMANTIC
)
from pm_cicd.utils.version_tools import (
  increase_version_num,
  get_version_diff_to_master,
  is_release_branch,
  is_develop_version,
  is_release_version,
  is_hotfix_version
)
from pm_cicd.utils.helpers import (
  is_merge_pull_request,
  is_python_project,
  get_forked_branch_type
)

sys.path.insert(0, os.getcwd())

def update_version(branch, version):
  if version is None:
    return None
  repo = git.Repo(search_parent_directories=True)
  commit_message = repo.head.object.message

  # if it isn't a merge pr, we don't do anything
  if not is_merge_pull_request(commit_message):
    return None

  new_version = None
  parse_version = version.split('-')
  version_num = parse_version[0]
  dev_incr_num = 1
  rel_incr_num = 1
  if is_develop_version(version):
    dev_num = parse_version[2]
    dev_incr_num = str(int(dev_num) + 1)
  elif is_release_version(version):
    rel_num = parse_version[-1]
    rel_incr_num = str(int(rel_num) + 1)

  if branch == BRANCHES.DEVELOP.value:
    version_differences_dict = get_version_diff_to_master(version_num)
    if get_forked_branch_type(commit_message) == BRANCH_TYPE.FEATURE.value:
      # if the version is already higher than the master, than we increment the number instead
      if version_differences_dict[VERSION_SEMANTIC.MINOR.value] > 0:
        new_version = version_num + '-dev-' + dev_incr_num
      else:
        new_version = increase_version_num(version_num, VERSION_SEMANTIC.MINOR.value) + '-dev-1'
    elif get_forked_branch_type(commit_message) == BRANCH_TYPE.BUGFIX.value:
      # if the version is already higher than the master, than we increment the number instead
      if version_differences_dict[VERSION_SEMANTIC.PATCH.value] > 0:
        new_version = version_num + '-dev-' + dev_incr_num
      else:
        new_version = increase_version_num(version_num, VERSION_SEMANTIC.PATCH.value) + '-dev-1'
    elif BRANCHES.MASTER.value in commit_message: # if it is master -> develop, it must be a hotfix
      new_version = version_num + '-dev-1'
  elif branch == BRANCHES.MASTER.value:
    if is_develop_version(version):
      new_version = version_num
    elif is_hotfix_version(version) or\
    get_forked_branch_type(commit_message) == BRANCH_TYPE.HOTFIX.value or\
    get_forked_branch_type(commit_message) == BRANCH_TYPE.BUGFIX.value:
      new_version = increase_version_num(version_num, VERSION_SEMANTIC.PATCH.value)
    elif get_forked_branch_type(commit_message) == BRANCH_TYPE.FEATURE.value:
      new_version = increase_version_num(version_num, VERSION_SEMANTIC.MINOR.value)
  elif is_release_branch(branch):
    if rel_incr_num == 1: # indicates that the version doesn't already include '-rel-'
      version_suffix = branch.replace('release/', 'rel-')
      new_version = version_num + '-' + version_suffix + '-1'
    else:
      new_version = '-'.join(parse_version[0:-1]) + '-' + rel_incr_num
  return new_version

def save_version_py(path, version):
  # Writing contents to the changelog file
  f = open(path, "a+")
  # Erasing the contents of the file
  f.truncate(0)
  # Adding the version number and the version ticket number
  contents = "''' module for version '''" + '\n'
  contents += 'VERSION = ' + "'" +  version + "'" + '\n'
  # Bumping the version
  f.write(contents)
  # Closing the file
  f.close()

def save_version_js(path, version):
  # Updating the version
  f = open(path)
  # Loading the contents of the file
  parsed_json = json.load(f)
  parsed_json['version'] = version

  # Dumping the updated json into the package.json file
  with open(path, 'w') as fp:
    json.dump(parsed_json, fp, indent=2)
    fp.write('\n') # appends newline at the end

def bump_version(path, current_version, branch):
  new_version = update_version(branch, current_version)

  if new_version is not None:
    if is_python_project():
      save_version_py(path, new_version)
    else:
      save_version_js(path, new_version)

  return new_version
