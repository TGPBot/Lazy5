    # Credit @LazyDeveloper.
    # Please Don't remove credit.
    # Thank you LazyDeveloper for helping us in this Journey
import asyncio
import re
import ast
import math
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.lazy_utils import progress_for_pyrogram, convert, humanbytes
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os 
import humanize
from PIL import Image
import time
from utils import get_shortlink
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

req_channel = REQ_CHANNEL
BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
	user_id = update.message.chat.id
	date = update.message.date
	await update.message.delete()
	await update.message.reply_text("»»——— 𝙋𝙡𝙚𝙖𝙨𝙚 𝙀𝙣𝙩𝙚𝙧 𝙉𝙚𝙬 𝙁𝙞𝙡𝙚 𝙉𝙖𝙢𝙚...",	
	reply_to_message_id=update.message.reply_to_message.id,  
	reply_markup=ForceReply(True))  
# Born to make history @LazyDeveloper !
@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    type = update.data.split("_")[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file = update.message.reply_to_message
    file_path = f"downloads/{new_filename}"
    ms = await update.message.edit("\n༻☬ད 𝘽𝙪𝙞𝙡𝙙𝙞𝙣𝙜 𝙇𝙖𝙯𝙮 𝙈𝙚𝙩𝙖𝘿𝙖𝙩𝙖...")
    c_time = time.time()
    try:
        path = await bot.download_media(
                message=file,
                progress=progress_for_pyrogram,
                progress_args=("**\n  ღ♡ ꜰɪʟᴇ ᴜɴᴅᴇʀ ᴄᴏɴꜱᴛʀᴜᴄᴛɪᴏɴ... ♡♪**", ms, c_time))
    except Exception as e:
        await ms.edit(e)
        return 
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
    except:
        pass
    user_id = int(update.message.chat.id) 
    ph_path = None 
    media = getattr(file, file.media.value)
    filesize = humanize.naturalsize(media.file_size) 
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
    if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
         except Exception as e:
             await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
             return 
    else:
        caption = f"**{new_filename}** \n\n💽𝗗𝗮𝘁𝗮 𝗖𝗼𝘀𝘁: `{filesize}`"
    if (media.thumbs or c_thumb):
        if c_thumb:
           ph_path = await bot.download_media(c_thumb) 
        else:
           ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
    await ms.edit("**三 𝘗𝘳𝘦𝘱𝘢𝘳𝘪𝘯𝘨 𝘵𝘰 𝘳𝘦𝘤𝘦𝘪𝘷𝘦 𝘓𝘢𝘻𝘺 𝘧𝘪𝘭𝘦...︻デ═一**")
    c_time = time.time() 
    try:
       if type == "document":
          await bot.send_document(
	        update.message.chat.id,
                   document=file_path,
                   thumb=ph_path, 
                   caption=caption, 
                   progress=progress_for_pyrogram,
                   progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time))
       elif type == "video": 
           await bot.send_video(
	        update.message.chat.id,
	        video=file_path,
	        caption=caption,
	        thumb=ph_path,
	        duration=duration,
	        progress=progress_for_pyrogram,
	        progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time))
       elif type == "audio": 
           await bot.send_audio(
	        update.message.chat.id,
	        audio=file_path,
	        caption=caption,
	        thumb=ph_path,
	        duration=duration,
	        progress=progress_for_pyrogram,
	        progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time   )) 
    except Exception as e: 
        await ms.edit(f" Erro {e}") 
        os.remove(file_path)
        if ph_path:
          os.remove(ph_path)
        return 
    await ms.delete() 
    os.remove(file_path) 
    if ph_path:
       os.remove(ph_path) 

# # Born to make history @LazyDeveloper !
@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):

    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("This Message is not for you dear. Don't worry you can send new one !", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
        # if query.from_user.id in download_counts and download_counts[query.from_user.id]['date'] == current_date:
        #     if download_counts[query.from_user.id]['count'] >= DOWNLOAD_LIMIT:
        #         # set URL_MODE to False to disable the URL shortener button
        #         URL_MODE = False
        #     else:
        #         # increment the download count for the user
        #         download_counts[query.from_user.id]['count'] += 1
        # else:
        #     # create a new entry for the user in the download counts dictionary
        #     download_counts[query.from_user.id] = {'date': current_date, 'count': 1}d
    if settings['button']:
            if URL_MODE is True:
                if query.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif query.from_user.id in LZURL_PRIME_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                        ]
                else:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", 
                                url=await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                            ),
                        ]
                        for file in files
                    ]
            else:
                btn = [
                    [
                        InlineKeyboardButton(
                            text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                        ),
                    ]
                    for file in files
                ]

    else:
        if URL_MODE is True:
            if query.from_user.id in ADMINS:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'files#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'files#{file.file_id}',),
                    ]
                    for file in files
                ]
            elif query.from_user.id in LZURL_PRIME_USERS:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'files#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'files#{file.file_id}',),
                    ]
                    for file in files
                ]
            else:
                btn = [
                    query[
                        InlineKeyboardButton(text=f"{file.file_name}", url=await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")),
                        InlineKeyboardButton(text=f"[{get_size(file.file_size)}]", url=await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")),
                    ]
                    for file in files
                ]
        else:
            if query.from_user.id in ADMINS:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'files#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'files#{file.file_id}',),
                    ]
                    for file in files
                ]
            else:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'files#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'files#{file.file_id}',),
                    ]
                    for file in files
                ]
    try:
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )
                
    except KeyError:
        grpid = await active_connection(str(message.from_user.id))
        await save_group_settings(grpid, 'auto_delete', True)
        settings = await get_settings(message.chat.id)
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )
    btn.insert(0,
        [ 
	    InlineKeyboardButton(text=DOWNLOAD_TEXT_NAME, url=DOWNLOAD_TEXT_URL)
        ] 
    )

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

# Born to make history @LazyDeveloper !
@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("This Message is not for you dear. Don't worry you can send new one !", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit('😒 currently unavailable ! we are really sorry for inconvenience !\n Have patience ! our great admins will upload it as soon as possible !')
            await asyncio.sleep(10)
            await k.delete()

# Born to make history @LazyDeveloper !
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('♥️ Love @LazY_PrinceBot ♥️')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you sona!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "filep" else False,
                    reply_markup=InlineKeyboardMarkup(
                        [
                         [
                          InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://telegram.me/{MOVIE_GROUP_USERNAME}'),
                          InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=f'https://telegram.me/{MAIN_CHANNEL_USRNM}')
                       ],[
                          InlineKeyboardButton('❌Cʟᴏꜱᴇ❌', callback_data='close_data')
                         ]
                        ]
                    )
                )
                await query.answer('Check PM, I have sent files in pm', show_alert=True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("Hᴇʏ Bᴜᴅᴅʏ Dᴏɴ'ᴛ Bᴇ Oᴠᴇʀꜱᴍᴀʀᴛ..😏\n\nFɪʀꜱᴛ J̲ᴏ̲ɪ̲ɴ̲ ̲U̲ᴘ̲ᴅ̲ᴀ̲ᴛ̲ᴇ̲ꜱ̲ C̲ʜ̲ᴀ̲ɴ̲ɴ̲ᴇ̲ʟ̲ Tʜᴇɴ Cʟɪᴄᴋ ᴏɴ T̲ʀ̲ʏ̲ ̲A̲ɢ̲ᴀ̲ɪ̲ɴ̲", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                  InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://telegram.me/{MOVIE_GROUP_USERNAME}'),
                  InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=f'https://telegram.me/{MAIN_CHANNEL_USRNM}')
               ],[
                  InlineKeyboardButton('❌Cʟᴏꜱᴇ❌', callback_data='close_data')
                 ]
                ]
            )
        )
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('➕ Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ], [
            InlineKeyboardButton('ℹ️ Hᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('🧑🏻‍💻 Aʙᴏᴜᴛ', callback_data='about')
        ], [
            InlineKeyboardButton('🔄 Mᴏʀᴇ', callback_data='morchl'),
            InlineKeyboardButton('🔐 Cʟᴏꜱᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ', callback_data='autofilter')
        ], [
            InlineKeyboardButton('Sᴛᴏʀᴇ ʏᴏᴜʀ Fɪʟᴇꜱ', callback_data='lazy_filstr')
        ], [
            InlineKeyboardButton('Cᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct'),
            InlineKeyboardButton('Exᴛʀᴀ Mᴏᴅᴇ', callback_data='extra')
        ], [
            InlineKeyboardButton('Rᴇɴᴀᴍᴇ ʏᴏᴜʀ Fɪʟᴇꜱ', callback_data='lazy_rnm')
        ], [
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔐 Cʟᴏꜱᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('🧑🏻‍💻 Oᴡɴᴇʀ', callback_data='owner_info'),
            InlineKeyboardButton('🪩 Sᴛᴀᴛᴜꜱ', callback_data='stats')
        ], [
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔐 Cʟᴏꜱᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "morchl":
        buttons = [[
            InlineKeyboardButton('Mᴀɪɴ Cʜᴀɴɴᴇʟ', url=CAPTION_BUTTON_URL),
            InlineKeyboardButton('Mᴏᴠɪᴇ Cʜᴀɴɴᴇʟ', url=f'https://telegram.me/{MOVIE_CHANNEL_USERNAME}')
        ],[
            InlineKeyboardButton('Mᴏᴠɪᴇ Sᴇᴀʀᴄʜ Gʀᴏᴜᴘ', url=f'https://telegram.me/{MOVIE_GROUP_USERNAME}')
        ],[
            InlineKeyboardButton('🚪Gᴏ Bᴀᴄᴋ', callback_data='start'),
            InlineKeyboardButton('🔐 Cʟᴏꜱᴇ', callback_data='close_data')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MORCHL_TXT.format(temp.B_LINK),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⏹️ Bᴜᴛᴛᴏɴꜱ', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif data.startswith("notify_user_not_avail"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"💬Rᴇǫᴜᴇsᴛ Aɢᴀɪɴ💬", url=f"https://telegram.me/{MOVIE_GROUP_USERNAME}")
            ],[
                InlineKeyboardButton(text=f"🧑🏻‍💻Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ🧑🏻‍💻", url=f"https://telegram.me/{ADMIN_USRNM}")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"❌ Dᴇʟᴇᴛᴇ Lᴏɢ ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv)
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"**Yᴏᴜʀ Rᴇǫᴜᴇsᴛ ɪꜱ Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ..😌**\n\n**Rᴇǫᴜᴇsᴛ Nᴀᴍᴇ:** `{movie}` \n\n**Pʟzz... Pʀᴏᴠɪᴅᴇ Sᴏᴍᴇ Mᴏʀᴇ Dᴇᴛᴀɪʟꜱ ᴛᴏ <a href='https://telegram.me/{ADMIN_USRNM}'>Aᴅᴍɪɴ</a>.**\n\n**Kɪɴᴅʟʏ Rᴇǫᴜᴇsᴛ Aɢᴀɪɴ  ᴏʀ Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ Fᴏʀ Hᴇʟᴘ.**", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**✅Uꜱᴇʀ Nᴏᴛɪꜰɪᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ...!!**__\n\n**🌐Sᴛᴀᴛᴜꜱ :** Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ 😒\n**🪪Uꜱᴇʀ ID :** `{user_id}`\n**📨Cᴏɴᴛᴇɴᴛ :** `{movie}`",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer("something went wrong", show_alert=True)
            return
        
    elif data.startswith("notify_user_alrupl"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔎Sᴇᴀʀᴄʜ Aɢᴀɪɴ🔎", url=f"https://telegram.me/{MOVIE_GROUP_USERNAME}")
            ],[
                InlineKeyboardButton(text=f"🧑🏻‍💻Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ🧑🏻‍💻", url=f"https://telegram.me/{ADMIN_USRNM}")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"❌ Dᴇʟᴇᴛᴇ Lᴏɢ ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv)            
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"**Hᴇʏ..!! Yᴏᴜʀ Rᴇǫᴜᴇsᴛᴇᴅ Cᴏɴᴛᴇɴᴛ ɪꜱ Aʟʀᴇᴀᴅʏ Uᴘʟᴏᴀᴅᴇᴅ✅**\n\n**Rᴇǫᴜᴇsᴛ Nᴀᴍᴇ:** `{movie}` \n\n**Pʟz..Sᴇᴀʀᴄʜ Aɢᴀɪɴ ɪɴ Oᴜʀ Oꜰꜰɪᴄɪᴀʟ Gʀᴏᴜᴘ🙃**", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**✅Uꜱᴇʀ Nᴏᴛɪꜰɪᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ...!!**__\n\n**🌐Sᴛᴀᴛᴜꜱ :** Aʟʀᴇᴀᴅʏ Uᴘʟᴏᴀᴅᴇᴅ ✅\n**🪪Uꜱᴇʀ ID :** `{user_id}`\n**📨Cᴏɴᴛᴇɴᴛ :** `{movie}`",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except:
            await query.answer("something went wrong", show_alert = True)
            return
        
    elif data.startswith("notify_userupl"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔎Sᴇᴀʀᴄʜ Aɢᴀɪɴ🔎", url=f"https://telegram.me/{MOVIE_GROUP_USERNAME}")
            ],[
                InlineKeyboardButton(text=f"🧑🏻‍💻Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ🧑🏻‍💻", url=f"https://telegram.me/{ADMIN_USRNM}")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"❌ Dᴇʟᴇᴛᴇ Lᴏɢ ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"**Yᴏᴜʀ Rᴇǫᴜᴇsᴛ Hᴀꜱ Bᴇᴇɴ Uᴘʟᴏᴀᴅᴇᴅ Sᴜᴄᴇssғᴜʟʟʏ✅**\n\n**Rᴇǫᴜᴇsᴛ Nᴀᴍᴇ:** `{movie}` \n\n**Pʟz..Sᴇᴀʀᴄʜ Aɢᴀɪɴ ɪɴ Oᴜʀ Oꜰꜰɪᴄɪᴀʟ Gʀᴏᴜᴘ🙃**", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**✅Uꜱᴇʀ Nᴏᴛɪꜰɪᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ...!!**__\n\n**🌐Sᴛᴀᴛᴜꜱ :** Uᴘʟᴏᴀᴅᴇᴅ ✅\n**🪪Uꜱᴇʀ ID :** `{user_id}`\n**📨Cᴏɴᴛᴇɴᴛ :** `{movie}`", reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except:
            await query.answer("something went wrong", show_alert = True)
            return
        
    elif data.startswith("notify_user_req_rejected"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"💬Rᴇǫᴜᴇsᴛ Aɢᴀɪɴ💬", url=f"https://telegram.me/{MOVIE_GROUP_USERNAME}")
            ],[
                InlineKeyboardButton(text=f"🧑🏻‍💻Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ🧑🏻‍💻", url=f"https://telegram.me/{ADMIN_USRNM}")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"❌ Dᴇʟᴇᴛᴇ Lᴏɢ ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"**Sᴏʀʀʏ!!!😔 Yᴏᴜʀ Rᴇǫᴜᴇsᴛ Hᴀꜱ Bᴇᴇɴ Rᴇᴊᴇᴄᴛᴇᴅ Bʏ Aᴅᴍɪɴ❌**\n\n**Rᴇǫᴜᴇsᴛ Nᴀᴍᴇ:** `{movie}` \n\n**Rᴇᴀꜱᴏɴ: Aʟʀᴇᴀᴅʏ Aᴅᴅᴇᴅ ɪɴ Rᴇǫᴜᴇsᴛ Lɪꜱᴛ ᴏʀ Rᴇǫᴜᴇsᴛ ɪꜱ Mᴀʟғᴏʀᴍᴀᴛᴛᴇᴅ.**\n\n**Kɪɴᴅʟʏ Rᴇǫᴜᴇsᴛ Aɢᴀɪɴ  ᴏʀ  Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ Fᴏʀ Hᴇʟᴘ.**", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**✅Uꜱᴇʀ Nᴏᴛɪꜰɪᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ...!!**__\n\n**🌐Sᴛᴀᴛᴜꜱ :** Rᴇǫᴜᴇsᴛ Rᴇᴊᴇᴄᴛᴇᴅ ❌\n**🪪Uꜱᴇʀ ID :** `{user_id}`\n**📨Cᴏɴᴛᴇɴᴛ :** `{movie}`",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except:
            await query.answer("something went wrong", show_alert = True)
            return
        
    elif data.startswith("notify_user_spelling_error"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔎Sᴇᴀʀᴄʜ Aɢᴀɪɴ🔎", url=f"https://telegram.me/{MOVIE_GROUP_USERNAME}")
            ],[
                InlineKeyboardButton(text=f"🧑🏻‍💻Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ🧑🏻‍💻", url=f"https://telegram.me/{ADMIN_USRNM}")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"❌ Dᴇʟᴇᴛᴇ Lᴏɢ ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"**Yᴏᴜʀ Rᴇǫᴜᴇsᴛᴇᴅ Cᴏɴᴛᴇɴᴛ Cᴏᴜʟᴅɴ'ᴛ ʙᴇ Fᴏᴜɴᴅ Bᴇᴄᴀᴜꜱᴇ ɪᴛ'ꜱ Nᴏᴛ Sᴘᴇʟʟᴇᴅ Cᴏʀʀᴇᴄᴛʟʏ💬**\n\n**Rᴇǫᴜᴇsᴛ Nᴀᴍᴇ:** `{movie}` \n\n**Pʟz.. Cʜᴇᴄᴋ Sᴘᴇʟʟɪɴɢ ɪɴ  <a href='https://google.com/search'>🔎Gᴏᴏɢʟᴇ</a>. Aɴᴅ Sᴇᴀʀᴄʜ Aɢᴀɪɴ ɪɴ Oᴜʀ Oꜰꜰɪᴄɪᴀʟ Gʀᴏᴜᴘ🙃**", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**✅Uꜱᴇʀ Nᴏᴛɪꜰɪᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ...!!**__\n\n**🌐Sᴛᴀᴛᴜꜱ :** Sᴘᴇʟʟɪɴɢ Eʀʀᴏʀ 🖊\n**🪪Uꜱᴇʀ ID :** `{user_id}`\n**📨Cᴏɴᴛᴇɴᴛ :** `{movie}`",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except:
            await query.answer("something went wrong", show_alert = True)
            return
        
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='owner_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        if query.from_user.id in ADMINS:
            await query.message.edit_text(
                text=script.ADMIN_TXT,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.answer("Sᴏʀʀʏ!! ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴏɴʟʏ ꜰᴏʀ ᴍʏ Aᴅᴍɪɴꜱ⚠️", show_alert = True)
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='about'),
            InlineKeyboardButton('♻️ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ],[
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    # elif query.data == "getlazythumbnail":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="thdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="lazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZTHMB_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    # elif query.data == "thdonatelazydev":
    #     buttons = [
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="getlazythumbnail") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.DNT_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    # elif query.data == "getlazylink":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="linkdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="lazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZLINK_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    elif query.data == "donatelazydev":
        buttons = [
            [ InlineKeyboardButton("⨳   Close   ⨳", callback_data="close_data") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DNT_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "lazyhome":
        text = f"""\n⨳ *•.¸♡ L҉ΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\n**Please tell, what should i do with this file.?**\n"""
        buttons = [[ InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="rename") ],
                           [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="cancel") ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )    
    elif query.data == "requireauth":
        buttons = [
            [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="cancel") ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.REQ_AUTH_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    # elif query.data == "reqauthgetlazythumbnail":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="thdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="reqauthlazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZTHMB_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    # elif query.data == "reqauthlazyhome":
    #     text = f"""\n⨳ *•.¸♡ L҉ΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\n**Please tell, what should i do with this file.?**\n"""
    #     buttons = [[ InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="requireauth") ],
    #                        [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="cancel") ]]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #                 text=text,
    #                 reply_markup=reply_markup,
    #                 parse_mode=enums.ParseMode.HTML
    #             )
    # elif query.data == "reqauthgetlazylink":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="linkdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="reqauthlazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZLINK_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    elif query.data == "exit":
        await query.answer("Sorry Darling! You can't make any changes...\n\nOnly my Admin can change this setting...", show_alert = True)
        return
    elif query.data == "invalid_index_process":
        await query.answer("Hey sweetie, please send me the last media with quote from your group.\nAnd also make sure that i am admin in your beloved group...")
        return
    # elif query.data == "already_uploaded":
    #     if query.from_user.id not in ADMINS:
    #         await query.answer("Sorry Darling! You can't make any changes...\n\nOnly my Admin can change this setting...", show_alert = True)
    #         return
    #     else:
    #         message = message.text
    #         chat_id = message.chat_id
    #         extracted_line = re.search(pattern, message, re.MULTILINE)
    #         if extracted_line:
    #           # Send the extracted line to the other group chat
    #             buttons = [
    #             [ InlineKeyboardButton("⨳ ok ⨳", callback_data="cancel") ]
    #             ]
    #             reply_markup = InlineKeyboardMarkup(buttons)
    #             await client.send_message(MOVIE_GROUP_ID, text=extracted_line.group(1))
    elif query.data == "cancel":
        try:
            await query.message.delete()
        except:
            return
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='about'),
            InlineKeyboardButton('♻️ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ],[
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "owner_info":
            btn = [[
                    InlineKeyboardButton('Sᴜᴅᴏ Mᴀꜱᴛᴇʀ', callback_data='admin'),
                    InlineKeyboardButton('Sᴏᴜʀᴄᴇ Cᴏᴅᴇ', callback_data='source')
                  ],[
                    InlineKeyboardButton("🚪 Bᴀᴄᴋ", callback_data="about")
                  ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.OWNER_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "lazy_filstr":
            filbtn = [[
                       InlineKeyboardButton("🚪 Bᴀᴄᴋ", callback_data="help")
                     ]]
            reply_markup = InlineKeyboardMarkup(filbtn)
            await query.message.edit_text(
                text=(script.LAZY_FILSTR),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "lazy_rnm":
            filbtn = [[
                       InlineKeyboardButton("🚪 Bᴀᴄᴋ", callback_data="help")
                     ]]
            reply_markup = InlineKeyboardMarkup(filbtn)
            await query.message.edit_text(
                text=(script.LAZY_RNM),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            if query.from_user.id in ADMINS:
                buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Cʟᴏsᴇ Sᴇᴛᴛɪɴɢs', callback_data='close_data')
                ]
            ]
            else:
                buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'exit'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'exit')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Cʟᴏsᴇ Sᴇᴛᴛɪɴɢs', callback_data='close_data')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer('♥️ Thank You @LazY_PrinceBot ♥️')

async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            requested_movie = search.strip()
            user_id = message.from_user.id
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                await client.send_message(req_channel,f"**📟 Rᴇǫᴜᴇsᴛ Dᴇᴛᴀɪʟs :**\n\n**📨 Cᴏɴᴛᴇɴᴛ :** `{search}`\n**🧑🏻‍💻 Rᴇǫᴜᴇsᴛᴇᴅ Bʏ : {message.from_user.mention}**\n**🪪 Uꜱᴇʀ ID :** {user_id}",
                                                                                                       reply_markup=InlineKeyboardMarkup([
                                                                                                                                        [InlineKeyboardButton(text=f"✅Aʟʀᴇᴀᴅʏ Uᴘʟᴏᴀᴅᴇᴅ", callback_data=f"notify_user_alrupl:{user_id}:{requested_movie}")],
                                                                                                                                        [InlineKeyboardButton(text=f"✔️Uᴘʟᴏᴀᴅᴇᴅ", callback_data=f"notify_userupl:{user_id}:{requested_movie}"),InlineKeyboardButton("🖋Sᴘᴇʟʟ Eʀʀᴏʀ", callback_data=f"notify_user_spelling_error:{user_id}:{requested_movie}")],
                                                                                                                                        [InlineKeyboardButton(text=f"😒Nᴏᴛ Aᴠᴀɪʟ", callback_data=f"notify_user_not_avail:{user_id}:{requested_movie}"),InlineKeyboardButton("❌Rᴇᴊᴇᴄᴛ Rᴇǫ", callback_data=f"notify_user_req_rejected:{user_id}:{requested_movie}")],
                                                                                                                                        ]))
                
                l = await message.reply_text(text=f"**Sᴏʀʀʏ ɴᴏ Rᴇꜱᴜʟᴛ ꜰᴏᴜɴᴅ Fᴏʀ**\n`{search}`\n\n**ɪᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴛ ᴛᴏ...Aᴅᴍɪɴ**\n\n**Pʟᴇᴀᴇꜱᴇ ᴡᴀɪᴛ,..ɪ ᴡɪʟʟ ɴᴏᴛɪꜰʏ**\n**ʏᴏᴜ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ...**\n\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ: {message.from_user.mention}**",
                                                                                                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ Gʀᴏᴜᴘ ➕", url=f'http://t.me/{temp.U_NAME}?startgroup=true')],[InlineKeyboardButton("🔔 Bᴀᴄᴋᴜᴘ Cʜᴀɴɴᴇʟ 🔔", url=f"https://t.me/{DEV_CHANNEL_USRNM}")],[InlineKeyboardButton("🔎Gᴏᴏɢʟᴇ ꜱᴘᴇʟʟɪɴɢ Cʜᴇᴄᴋ🔎", url=f"https://google.com/search")],[InlineKeyboardButton("»♥️ Tʜᴀɴᴋ-Yᴏᴜ ♥️«", callback_data="close_data")]]))
                await asyncio.sleep(60)
                await l.delete()    
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else: 
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
            if URL_MODE is True:
                if message.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif message.from_user.id in LZURL_PRIME_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                            ),
                        ]
                        for file in files
                        ]
                else:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", 
                                url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}")
                            ),
                        ]
                        for file in files
                    ]
            else    :
                btn = [
                    [
                        InlineKeyboardButton(
                            text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                        ),
                    ]
                    for file in files
                ]

    else:
        if URL_MODE is True:
            if message.from_user.id in ADMINS:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'files#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'files#{file.file_id}',),
                    ]
                    for file in files
                ]
            elif message.from_user.id in LZURL_PRIME_USERS:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'{pre}#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'{pre}#{file.file_id}',),
                    ]
                    for file in files
                ]
            else:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}")),
                        InlineKeyboardButton(text=f"[{get_size(file.file_size)}]", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}")),
                    ]
                    for file in files
                ]
        else:
            if message.from_user.id in ADMINS:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'files#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'files#{file.file_id}',),
                    ]
                    for file in files
                ]
            else:
                btn = [
                    [
                        InlineKeyboardButton(text=f"{file.file_name}",callback_data=f'{pre}#{file.file_id}',),
                        InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f'{pre}#{file.file_id}',),
                    ]
                    for file in files
                ]

    try:
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )
                
    except KeyError:
        grpid = await active_connection(str(message.from_user.id))
        await save_group_settings(grpid, 'auto_delete', True)
        settings = await get_settings(message.chat.id)
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(text=DIRECT_FILE_TEXT_NAME, url=DIRECT_FILE_TEXT_URL),
                ]
            )

    btn.insert(0,
        [ 
	    InlineKeyboardButton(text=DOWNLOAD_TEXT_NAME, url=DOWNLOAD_TEXT_URL),
        ] 
    )
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"🗓 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="NEXT ⏩", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓 1/1", callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"**Hᴇʀᴇ ɪꜱ Tʜᴇ Rᴇꜱᴜʟᴛ ꜰᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ:** {search} \n\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ: {mention}** \n\n**Pᴏᴡᴇʀᴇᴅ Bʏ: {message.chat.title}** \n\n**Tʜɪs Mᴇssᴀɢᴇ Wɪʟʟ Bᴇ Aᴜᴛᴏ Dᴇʟᴇᴛᴇᴅ Aꜰᴛᴇʀ 5 Mɪɴᴜᴛᴇs.**"
    if imdb and imdb.get('poster'):
        try:
            z = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
            if SELF_DELETE is True:
                await asyncio.sleep(SELF_DELETE_SECONDS)
                await z.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            m = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
            if SELF_DELETE is True:
                await asyncio.sleep(SELF_DELETE_SECONDS)
                await m.delete()
            
        except Exception as e:
            logger.exception(e)
            n = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
            if SELF_DELETE is True:
                await asyncio.sleep(SELF_DELETE_SECONDS)
                await n.delete()         
    else:
        p = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
        if SELF_DELETE is True:
            await asyncio.sleep(SELF_DELETE_SECONDS)
            await p.delete()
    if spoll:
        await msg.message.delete()

# Born to make history @LazyDeveloper !
async def advantage_spell_chok(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(10)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        k = await msg.reply("Hey Sona! The requested content is currently unavailable in our database, have some patience 🙂 - our great admin will upload it as soon as possible \n             **or**\nDiscuss issue with admin here 👉  <a href='https://telegram.me/{ADMIN_USRNM}'>Discuss Here</a> ♥️ ")
        await asyncio.sleep(10)
        await k.delete()
        return
    SPELL_CHECK[msg.id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    await msg.reply("Hey Sona! The requested content is currently unavailable in our database, have some patience 🙂 - our great admin will upload it as soon as possible \n              **or**\nDiscuss issue with admin here 👉 <a href='https://telegram.me/{ADMIN_USRNM}'>Discuss Here</a> ♥️ ",
                    reply_markup=InlineKeyboardMarkup(btn))


async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
