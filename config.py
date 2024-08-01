import os
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

BOT_TOKEN = os.getenv("BOT_TOKEN", config.get("bot", "token", fallback=None))
if not BOT_TOKEN:
    exit('Please provide BOT_TOKEN env variable')

WOLF_photo = 'https://masterpiecer-images.s3.yandex.net/76e21c5c75d011eebac46a0259d7362a:upscaled'

SUNRISE_PIC_FILE_ID = 'AgACAgIAAxkDAAIBFmaj7V1jVzuhIKD4oZIhDqZlKIRoAAIe4DEbeGkhSbFRuL6jKPdyAQADAgADeQADNQQ'

OPENWEATHER_API_KEY = '0d9b27dd7edbdcd0a7ae9601cf69f334'

admin_ids = config.get("admin", 'admin_id', fallback='')
admin_ids = [admin_id.strip() for admin_id in admin_ids.split(",")]
admin_ids = [int(admin_id) for admin_id in admin_ids if admin_id]
BOT_ADMIN_USER_IDS = [admin_ids]

