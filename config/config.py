from os import getenv

from dotenv import load_dotenv
load_dotenv(override=True)


class Config:
    admin_id = int(getenv("ADMIN_ID"))
    


config = Config


print(type(config.admin_id))