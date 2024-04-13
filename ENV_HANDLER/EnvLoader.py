import dotenv
from dotenv import dotenv_values

dotenv.load_dotenv()


config = dotenv_values(".env")

# Env variables
CLIENT_ID = config.get("CLIENT_ID", None)
SECRET_KEY = config.get("SECRET_KEY", None)
REDIRECT_URI = config.get("REDIRECT_URI", None)
STATE = config.get("STATE", None)