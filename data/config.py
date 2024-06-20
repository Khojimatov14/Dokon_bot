from environs import Env

env = Env()
env.read_env()

admins = []
for i in env.list("ADMINS"):
    admins.append(int(i))

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = admins
IP = env.str("ip")
