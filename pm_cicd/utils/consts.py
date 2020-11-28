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
  BLUE = '\033[94m'
  CYAN = '\033[96m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
