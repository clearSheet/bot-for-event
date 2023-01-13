TOKEN = '<YOU BOT TOKEN>'

admins = [225726820, 601638704, 185974961, 362589424]

groups = []


async def check_admin(id):
    for id_ad in admins:
        if id_ad == id:
            return True
