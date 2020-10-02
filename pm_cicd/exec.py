'''The driver script to bump the dev version and generate chnagelog'''
import os
from pm_cicd.bump_version import bump_version_py, bump_version_js
from pm_cicd.generate_changelog import gen_changelog
from pm_cicd.helpers import COMMIT_MESSAGE, exec_subprocess

def exec_deploy():
  ''' automate the bumping of the version and creation of a new entry in the CHANGELOG
  '''
  travis_branch = os.environ['TRAVIS_BRANCH']
  github_token = os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']
  repo_name = os.environ['TRAVIS_REPO_SLUG']

  if travis_branch == "gabe-test":
    # check the language of the project, and bump associated version file
    if os.environ["LANG"] == "py":
      bump_version_py(travis_branch)
    elif os.environ["LANG"] == "js":
      bump_version_js(travis_branch)

    # generate a new entry in the CHANGELOG
    gen_changelog(os.environ["LANG"])

    try:
      cmd = '''
        git add *
        git commit --message "{}"
      '''.format(COMMIT_MESSAGE)

      exec_subprocess(cmd)

      cmd = '''
        echo "token={}"
        git push "https://policyme:{}@github.com/{}.git" HEAD:{}
      '''.format(github_token, github_token, repo_name, travis_branch)

      exec_subprocess(cmd)
    except Exception as e:
      print(e)
      print("No changes to commit")
