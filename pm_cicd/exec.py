'''The driver script to bump the dev version and generate chnagelog'''
import os
from subprocess import run, PIPE, STDOUT

from pm_cicd.bump_version import bump_version
from pm_cicd.generate_changelog import gen_changelog
from pm_cicd.utils.consts import BRANCHES, COLORS
from pm_cicd.utils.version_tools import (
  verify_version_with_master,
  get_current_version,
  is_release_branch,
  is_develop_version
)
from pm_cicd.utils.helpers import (
  get_commit_message,
  exec_subprocess,
  find_version_path
)

def exec_deploy():
  ''' automate the bumping of the version and creation of a new entry in the CHANGELOG
  '''
  # travis environment variables
  branch = os.environ['CIRCLE_BRANCH']
  repo_name = os.environ['CIRCLE_PROJECT_REPONAME']
  repo_user_name = os.environ['CIRCLE_PROJECT_USERNAME']
  is_open_pr = False # TODO: disable for now

  update_develop = False

  if (branch == BRANCHES.MASTER.value or
      branch == BRANCHES.DEVELOP.value or
      is_release_branch(branch)):
    # if it is an open pr that we are merging to dev, we only run this
    if branch == BRANCHES.DEVELOP.value and is_open_pr:
      return verify_version_with_master()

    path = find_version_path()
    current_version = get_current_version(path)
    # if on master branch & merging develop -> master, we should update develop as well
    if branch == BRANCHES.MASTER.value and is_develop_version(current_version):
      update_develop = True

    # bump version number
    new_version = bump_version(path, current_version, branch)

    # generate a new entry in the CHANGELOG
    if branch == BRANCHES.MASTER.value and new_version is not None:
      gen_changelog(path, new_version)

    try:
      # we first configure git author
      # git add any modified files
      # also add some specific files in case they aren't already commited (requirements.txt & changelog)
      # reset any files we don't want autobump to commit (e.g. package-lock.json)
      cmd = '''
        git config credential.helper 'cache --timeout=120'
        git config user.email "pmbot@policyme.com"
        git config user.name "bot-pm"
        git add -u
        git reset -- package-lock.json
        git commit --message "{}"
      '''.format(get_commit_message(branch))

      exec_subprocess(cmd)

      # git push logic
      github_token = os.environ['GITHUB_TOKEN']
      cmd = '''
        git push -v "https://policyme:{}@github.com/{}/{}.git" HEAD:{}
      '''.format(github_token, repo_user_name, repo_name, branch)

      exec_subprocess(cmd)

      # if develop -> master merge then we should also update develop
      if update_develop:
        cmd = '''
          echo "------ Automerging master -> develop ------"
          git fetch origin {}
          git checkout {}
          git merge origin/{}
          git push -v "https://policyme:{}@github.com/{}/{}.git" HEAD:{}
        '''.format(BRANCHES.MASTER.value, BRANCHES.DEVELOP.value, BRANCHES.MASTER.value,
                  github_token, repo_user_name, repo_name, BRANCHES.DEVELOP.value)

        exec_subprocess(cmd)
    except Exception as e:
      print(COLORS.RED + "Something went wrong. Exiting autobump...."+ COLORS.ENDC)
      exit(e)
  else:
    print("Not in {} nor {} branch, skipping version bump and changelog"\
      .format(BRANCHES.DEVELOP.value, BRANCHES.MASTER.value))
