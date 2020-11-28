''' Constants
'''

import enum

CHANGELOG_FILE = "CHANGELOG.md"

SKIP_BUMP = "[skip autobump]"

class BRANCHES(enum.Enum):
  DEVELOP = 'develop'
  RELEASE = 'release'
  MASTER = 'master'

class BRANCH_TYPE(enum.Enum):
  FEATURE = 'feature'
  BUGFIX = 'bugfix'
  HOTFIX = 'hotfix'

  @staticmethod
  def list():
    return list(map(lambda branch_type: branch_type.value, BRANCH_TYPE))

class VERSION_SEMANTIC(enum.Enum):
  PATCH = 'PATCH'
  MINOR = 'MINOR'
  MAJOR = 'MAJOR'

class COLORS:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
