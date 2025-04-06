import os.path

from dotenv import load_dotenv

root_path = os.path.abspath(os.path.dirname(__file__))
flask_env_path = os.path.join(root_path, '.env')


def init_dotenv():
    if os.path.exists(flask_env_path):
        load_dotenv(flask_env_path)