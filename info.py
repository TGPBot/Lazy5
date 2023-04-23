import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
PICS = (environ.get('PICS', 'https://telegra.ph/file/3aecb4f98d11d57d7aa07.jpg https://telegra.ph/file/ecc416d9a2165c46d752a.jpg https://telegra.ph/file/a498ac569cb045fa47f51.jpg https://telegra.ph/file/d457bb99aff9684d95d86.jpg https://telegra.ph/file/46ab00b66746d6b8433c1.jpg')).split()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '978408962').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001877173739').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '978408962').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL', '-1001866867338')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://LazyPrince:LazyPrince@cluster0.wyvwivd.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "LazyDeveloper")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001961381696'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'LazyDeveloper')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), False)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>📂Fɪʟᴇ :</b> <code> {file_name} </code>\n\n<b>💾Sɪᴢᴇ : {file_size}</b>\n<b>⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽</b>\n<b><a href='https://t.me/+AJCnlql9y4o4MjJl'>Sᴇᴀʀᴄʜ Gʀᴏᴜᴘ​</a>│<a href='https://t.me/+5M64kC0935k0MTFl'>Mᴏᴠɪᴇ Cʜᴀɴɴᴇʟ</a></b>\n<b>⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺</b>\n<b>Pʟᴇᴀꜱᴇ Fᴏʀᴡᴀʀᴅ Yᴏᴜʀ Fɪʟᴇs Tᴏ\nSᴀᴠᴇᴅ Mᴇꜱꜱᴀɢᴇ & Cʟɪᴄᴋ Oɴ Tʜᴇ\nCʟᴏꜱᴇ Bᴜᴛᴛᴏɴ.</b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Your Query: {query}</b> \n‌‌‌‌IMDb Data by: @LazyDeveloper \n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10 \n\n♥️ we are nothing without you ♥️ \n\n💛 Please Share Us 💛\n\n⚠️Click on the button 👇 below to get your query privately")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), False)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '-1001965178287')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "True")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), False)

#LazyRenamer Configs
FLOOD = int(environ.get("FLOOD", "10"))
LAZY_MODE = bool(environ.get("LAZY_MODE"))
#Add user id of the user in this field those who you want to be Authentic user for file renaming features
lazy_renamers = [int(lazrenamers) if id_pattern.search(lazrenamers) else lazrenamers for lazrenamers in environ.get('LAZY_RENAMERS', '978408962').split()]
LAZY_RENAMERS = (lazy_renamers + ADMINS) if lazy_renamers else []
REQ_CHANNEL = int(environ.get('REQ_CHANNEL', '-1001962699032'))

#ai
AI = is_enabled((environ.get("AI","False")), False)
OPENAI_API = environ.get("OPENAI_API","")
LAZY_AI_LOGS = int(environ.get("LAZY_AI_LOGS","-1001924121462")) #GIVE YOUR NEW LOG CHANNEL ID TO STORE MESSAGES THAT THEY SEARCH IN BOT PM.... [ i have added this to keep an eye on the users message, to avoid misuse of LazyPrincess ]
# Requested Content template variables ---
ADMIN_USRNM = environ.get('ADMIN_USRNM','XKunalBot') # WITHOUT @
MAIN_CHANNEL_USRNM = environ.get('MAIN_CHANNEL_USRNM','LazYHuB') # WITHOUT @
DEV_CHANNEL_USRNM = environ.get('DEV_CHANNEL_USRNM','LazYHuB') # WITHOUT @
LAZY_YT_HANDLE = environ.get('LAZY_YT_HANDLE','LazYHuB')  # WITHOUT @ [  add only handle - don't add full url  ] 
MOVIE_GROUP_USERNAME = environ.get('MOVIE_GROUP_USERNAME', "+AJCnlql9y4o4MjJl") #[ without @ ]
MOVIE_CHANNEL_USERNAME = environ.get('MOVIE_CHANNEL_USERNAME', "+5M64kC0935k0MTFl") #[ without @ ]

# Url Shortner
URL_MODE = is_enabled((environ.get("URL_MODE","True")), False)
URL_SHORTENR_WEBSITE = environ.get('URL_SHORTENR_WEBSITE', 'omegalinks.in') #Always use website url from api section 
URL_SHORTNER_WEBSITE_API = environ.get('URL_SHORTNER_WEBSITE_API', '')
LZURL_PRIME_USERS = [int(lazyurlers) if id_pattern.search(lazyurlers) else lazyurlers for lazyurlers in environ.get('LZURL_PRIME_USERS', '978408962').split()]

# Auto Delete For Group Message (Self Delete) #
SELF_DELETE_SECONDS = int(environ.get('SELF_DELETE_SECONDS', 300))
SELF_DELETE = is_enabled((environ.get('SELF_DELETE','True')), False)

# Download Tutorial Button #
DOWNLOAD_TEXT_NAME = "📥Hᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ꜰʀᴏᴍ Lɪɴᴋ📥"
DOWNLOAD_TEXT_URL = "https://t.me/LazYHuB"

# Direct File Button #
DIRECT_FILE_TEXT_NAME = "📁Gᴇᴛ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇ ᴡɪᴛʜᴏᴜᴛ Lɪɴᴋ📁"
DIRECT_FILE_TEXT_URL = "https://t.me/LazYHuB"

# Custom Caption Under Button #
CAPTION_BUTTON = "🔔 Gᴇᴛ Uᴘᴅᴀᴛᴇ 🔔"
CAPTION_BUTTON_URL = "https://t.me/LazYHuB"

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
