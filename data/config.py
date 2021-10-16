from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Taking Bot token
ADMINS = env.list("ADMINS")  # Taking Bot token

DB_USER = env.str("DB_USER")  # Taking database username
DB_PASS = env.str("DB_PASS")  # Taking database password
DB_NAME = env.str("DB_NAME")  # Taking database host
DB_HOST = env.str("DB_HOST")  # Taking database host

