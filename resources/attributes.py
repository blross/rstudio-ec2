import os

PROJECT_NAME = 'rstudio'
RESOURCE_FOLDER_NAME = 'resources/'

USERNAME = 'ubuntu'
PASSWORD = 'password'

GROUP_NAME = PROJECT_NAME
GROUP_DESCRIPTION = "Security group for rstudio server"
KEY_PAIR_NAME = PROJECT_NAME
PEM_FILE_NAME = os.path.join(
    os.path.dirname(__file__),
    PROJECT_NAME + '.pem'
)
CONFIG_PICKLE_FILE_NAME = os.path.join(
    os.path.dirname(__file__),
    PROJECT_NAME + '_config.p'
)
USER_DATA_FILE_NAME = os.path.join(
    os.path.dirname(__file__),
    'user_data.sh'
)

INSTANCE_TYPE = 'm5.large'
IMAGE_ID = 'ami-aa2ea6d0'
MIN_COUNT = 1
MAX_COUNT = 1
MAX_PRICE = '0.05'

with open(USER_DATA_FILE_NAME, 'r') as sh:
    USER_DATA_SCRIPT = sh.read().format(username=USERNAME,
                                        password=PASSWORD)
