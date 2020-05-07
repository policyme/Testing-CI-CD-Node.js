'''The driver script to bump the dev version and generate chnagelog'''
import subprocess
import os
from pm_cicd.bump_version import bump_version_py, bump_version_js
from pm_cicd.generate_changelog import gen_changelog

def exec_deploy():

  travis_branch = os.environ['TRAVIS_BRANCH']

  if travis_branch == "develop":

    if os.environ["LANG"] == "py":
      bump_version_py(travis_branch)

    elif os.environ["LANG"] == "js":
      bump_version_js(travis_branch)

    gen_changelog()

  subprocess.run('''
  if [ "$TRAVIS_BRANCH" == "develop" ]; then

      commit_file() {
        git add *
        git commit --message "Updating the CHANGELOG.md and the _version file"
      }

      upload_files() {
        git remote add develop  https://${TOKEN}@github.com/policyme/${REPO_NAME}.git > /dev/null 2>&1
        git push develop HEAD:develop
      }
      commit_file
      upload_files

  fi
  ''', shell=True, check=True, executable='/bin/bash')
