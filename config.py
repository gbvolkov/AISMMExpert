import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.expanduser("~/Documents"), 'gv.env'))
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
vk_api_key = os.environ.get('VK_API_KEY')

vk_group_id = -226143353

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
