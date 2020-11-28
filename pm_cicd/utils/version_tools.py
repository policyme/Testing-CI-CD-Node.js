''' verify branch versions '''
import git
import json
import re

from pm_cicd.utils.consts import BRANCHES, VERSION_SEMANTIC
from pm_cicd.utils.helpers import (
  find_version_relative_path,
  find_version_path,
  is_python_project,
  get_version_py,
  get_version_js
)

# increases number depending on the semantic
def increase_version_num(version_num_str, semantic):
  version_digits = version_num_str.split('.')
  if len(version_digits) != 3:
    return None
  major = version_digits[0]
  minor = version_digits[1]
  patch = version_digits[2]
  if semantic == VERSION_SEMANTIC.PATCH.value:
    patch = str(int(patch) + 1)
  elif semantic == VERSION_SEMANTIC.MINOR.value:
    patch = str(0)
    minor = str(int(minor) + 1)
  elif semantic == VERSION_SEMANTIC.MAJOR.value:
    patch = str(0)
    minor = str(0)
    major = str(int(major) + 1)
  else:
    return None
  return major + '.' + minor + '.' + patch

# gets the sementic numbers & returns them in a dict
def get_version_dict(version_str):
  version_digits = version_str.split('.')
  if len(version_digits) != 3:
    return {}
  return {
    VERSION_SEMANTIC.MAJOR.value: version_digits[0],
    VERSION_SEMANTIC.MINOR.value: version_digits[1],
    VERSION_SEMANTIC.PATCH.value: version_digits[2]
  }

# gets the version on a different branch
def get_branch_version(branch):
  repo = git.Repo(search_parent_directories=True)
  version = None
  relative_path = find_version_relative_path()
  contents = repo.git.show('origin/{}:{}'.format(branch, relative_path))
  if is_python_project():
    contents = contents.strip().replace('\'', '')
    version = contents.split("=")[1]
  else:
    parsed_json = json.loads(contents)
    version = parsed_json['version']
  version = version.strip()
  return version

# gets the version from master branch & returns the version
def get_master_version():
  # get master branch's version
  master_version = get_branch_version(BRANCHES.MASTER.value)
  if master_version is None:
    raise Exception("failed to find a version from branch: {}".format(BRANCHES.MASTER.value))
  return master_version

# gets the version from current branch & returns the version
def get_current_version(specified_path = None):
  # we get the version for this branch/pr
  current_version = None
  path = specified_path
  if specified_path is None:
    path = find_version_path()
  if is_python_project():
    current_version = get_version_py(path)
  else:
    current_version = get_version_js(path)

  if current_version is None:
    raise Exception("failed to find a version in this branch/pr")
  current_version = current_version.strip()
  return current_version

# returns a version string without the description after the semantic
# e.g. 1.1.0-dev-1 -> 1.1.0
def strip_descriptions_from_version(version):
  parse_version = version.split('-')
  version_semantic = parse_version[0]
  return version_semantic

# determines how many versions is the current branch/pr ahead from master
def get_version_diff_to_master(current_version):
  master_version = strip_descriptions_from_version(get_master_version())
  master_version_dict = get_version_dict(master_version)
  current_version_dict = get_version_dict(current_version)
  version_differences_dict = {
    VERSION_SEMANTIC.MAJOR.value:
      int(current_version_dict[VERSION_SEMANTIC.MAJOR.value]) -
      int(master_version_dict[VERSION_SEMANTIC.MAJOR.value]),
    VERSION_SEMANTIC.MINOR.value:
      int(current_version_dict[VERSION_SEMANTIC.MINOR.value]) -
      int(master_version_dict[VERSION_SEMANTIC.MINOR.value]),
    VERSION_SEMANTIC.PATCH.value:
      int(current_version_dict[VERSION_SEMANTIC.PATCH.value]) -
      int(master_version_dict[VERSION_SEMANTIC.PATCH.value]),
  }
  return version_differences_dict

# returns true if the current branch's version is ahead of the master's version
def is_version_ahead_of_master(current_version):
  version_differences_dict = get_version_diff_to_master(current_version)
  return (
    int(version_differences_dict[VERSION_SEMANTIC.MAJOR.value]) > 0 or
    int(version_differences_dict[VERSION_SEMANTIC.MINOR.value]) > 0 or
    int(version_differences_dict[VERSION_SEMANTIC.PATCH.value]) > 0
  )

# used to determine what the version diff is between master & feature/bugfix/hotfix branch pr
# if the current branch version & master version is a missmatch we will show an error
def verify_version_with_master():
  master_version = strip_descriptions_from_version(get_master_version())
  current_version = strip_descriptions_from_version(get_current_version())
  if master_version != current_version:
    raise Exception('there is a version missmatch.\nPR/current version: {}\nMaster version: {}'\
      .format(current_version, master_version))
  print('{} is the correct version!'.format(current_version))

# determine if the current branch is a release branch
def is_release_branch(branch):
  if re.match('^release\/[A-Z]{2}[0-9]?-[0-9]+(-[a-z0-9]+)+$', branch):
    return True
  return False

def is_develop_version(version):
  if '-dev-' in version:
    return True
  return False

def is_release_version(version):
  if '-rel-' in version:
    return True
  return False

def is_hotfix_version(version):
  if '-hotf-' in version:
    return True
  return False
