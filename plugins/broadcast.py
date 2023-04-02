
from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages
import asyncio
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# https://t.me/LazyDeveoper
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩𝙞𝙣𝙜 𝙮𝙤𝙪𝙧 𝙈𝙚𝙨𝙨𝙖𝙜𝙚...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"𝙇𝙖𝙯𝙮 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙞𝙨 𝙞𝙣 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨...\n\n𝙏𝙤𝙩𝙖𝙡 𝙐𝙨𝙚𝙧𝙨: {total_users}\n𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙: {done} / {total_users}\n𝙎𝙪𝙘𝙘𝙚𝙨𝙨: {success}\n𝘽𝙡𝙤𝙘𝙠𝙚𝙙: {blocked}\n𝘿𝙚𝙡𝙚𝙩𝙚𝙙: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"𝙇𝙖𝙯𝙮 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙞𝙨 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙:\n𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙 𝙞𝙣 {time_taken} 𝙎𝙚𝙘𝙤𝙣𝙙𝙨.\n\n𝙏𝙤𝙩𝙖𝙡 𝙐𝙨𝙚𝙧𝙨: {total_users}\n𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙: {done} / {total_users}\n𝙎𝙪𝙘𝙘𝙚𝙨𝙨: {success}\n𝘽𝙡𝙤𝙘𝙠𝙚𝙙: {blocked}\n𝘿𝙚𝙡𝙚𝙩𝙚𝙙: {deleted}")

@Client.on_message(filters.command("group_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩𝙞𝙣𝙜 𝙮𝙤𝙪𝙧 𝙈𝙚𝙨𝙨𝙖𝙜𝙚 𝙩𝙤 𝙂𝙧𝙤𝙪𝙥𝙨...'
    )
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for group in groups:
        pti, sh = await broadcast_messages_group(int(group['id']), b_msg)
        if pti:
            success += 1
        elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"𝙇𝙖𝙯𝙮 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙞𝙨 𝙞𝙣 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨...\n\n𝙏𝙤𝙩𝙖𝙡 𝙂𝙧𝙤𝙪𝙥𝙨: {total_groups}\n𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙: {done} / {total_groups}\n𝙎𝙪𝙘𝙘𝙚𝙨𝙨: {success}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"𝙇𝙖𝙯𝙮 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙞𝙨 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙:\n𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙 𝙞𝙣 {time_taken} 𝙎𝙚𝙘𝙤𝙣𝙙𝙨.\n\n𝙏𝙤𝙩𝙖𝙡 𝙂𝙧𝙤𝙪𝙥𝙨: {total_groups}\n𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙: {done} / {total_groups}\n𝙎𝙪𝙘𝙘𝙚𝙨𝙨: {success}")
