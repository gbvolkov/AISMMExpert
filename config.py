OPENAI_API_KEY = "sk-proj-8W2FTjxabTBZIUZLJyzvT3BlbkFJx1M9dlgvEV7iVLU76xNz"

vk_api_key = "vk1.a.APCGeuOM7uLro89R1NZOp8fmyh-7swmfRZiGoXFny1UFa9RdTCimnrWbdalBr_Ql_A8Lh92xZmP_dmi6l8oQb5k_8OGbe4KG-AUPaHHcLp1PvxP2BC4QOiTSC09R7jY20iQkcWestsgi-tAN0EaqnaUAms_xjA0R-hztrmXFDHBw4cCh27ZYAr-udcdj1pQXShrsfTWdKWm1qES2ap-z6w"
vk_group_id = -226143353

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
