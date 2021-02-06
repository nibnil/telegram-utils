import asyncio
import logging
import os
from datetime import datetime

from src.entity import TgAccountEntity, TgGroupEntity, GROUP_STATUS_DEFAULT, TgGroupStatusEntity, GROUP_STATUS_WATCH, \
    FILE_TYPE_DEFAULT, FILE_TYPE_PHOTO, MIME_TYPE_VIDEO, FILE_TYPE_VIDEO, MIME_TYPE_IMAGE, FILE_TYPE_WEB, TgMsgEntity
from src.mongodb_helper import MongodbHelper
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, BadRequestError
from telethon.sessions import StringSession
from telethon.tl.types import Channel, PeerChannel, MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage


async def msg_handler(event):
    pass


def callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))


async def download_media(msg, abs_file_path):
    try:
        await asyncio.sleep(1)
        await msg.download_media(file=abs_file_path, progress_callback=callback)
    except FloodWaitError as ex:
        logging.exception(ex)
        await asyncio.sleep(ex.seconds)
    except BadRequestError as ex:
        logging.exception(ex)


async def update_groups(client, mongodb):
    tg_groups = list()
    tg_groups_status = list()
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, Channel):
            group_id = str(dialog.entity.id)
            group_name = dialog.entity.title
            username = dialog.entity.username
            group_create_time = dialog.entity.date
            create_time = datetime.now()
            update_time = datetime.now()
            tg_group = TgGroupEntity(group_id=group_id,
                                     group_name=group_name,
                                     username=username,
                                     group_create_time=group_create_time,
                                     create_time=create_time,
                                     update_time=update_time)
            tg_groups.append(tg_group.to_dict())
            group_status = GROUP_STATUS_DEFAULT
            last_datetime = dialog.message.date
            last_msg_id = dialog.message.id
            tg_group_status = TgGroupStatusEntity(group_id=group_id,
                                                  group_status=group_status,
                                                  last_datetime=last_datetime,
                                                  last_msg_id=last_msg_id,
                                                  create_time=create_time,
                                                  update_time=update_time)
            tg_groups_status.append(tg_group_status.to_dict())
    if tg_groups:
        result = await mongodb.do_bulk_upsert(col=TgGroupEntity.TABLE,
                                              data=tg_groups,
                                              filter_key=['group_id'],
                                              set_key=['update_time', 'group_name', 'username', 'group_create_time'],
                                              set_on_insert_key=['group_id', 'create_time'])
    if tg_groups_status:
        result = await mongodb.do_bulk_upsert(col=TgGroupStatusEntity.TABLE,
                                              data=tg_groups_status,
                                              filter_key=['group_id'],
                                              set_key=['last_datetime', 'last_msg_id', 'update_time'],
                                              set_on_insert_key=['create_time', 'last_archive_id', 'group_status'])


async def update_msgs(client, mongodb, file_path, limit=100):
    doc = await mongodb.do_find_one(TgGroupStatusEntity.TABLE,
                                    filter_={'group_status': GROUP_STATUS_WATCH},
                                    sort=[('update_time', 1)])
    if not doc:
        return False
    tg_group_status = TgGroupStatusEntity()
    await tg_group_status.from_dict(doc)
    if tg_group_status.last_msg_id > tg_group_status.last_archived_id:
        tg_msgs = list()
        msg_id = None
        min_id = tg_group_status.last_archived_id
        group_id = tg_group_status.group_id
        abs_dir_path = os.path.join(file_path, group_id)
        if not os.path.exists(abs_dir_path):
            os.mkdir(abs_dir_path)
        async for msg in client.iter_messages(int(group_id), reverse=True, min_id=min_id, limit=limit):
            msg_id = msg.id
            from_id = msg.from_id
            to_id = msg.to_id
            if isinstance(to_id, PeerChannel):
                to_id = to_id.channel_id
            else:
                logging.info(type(to_id))
                to_id = None
            media = msg.media
            file_type = FILE_TYPE_DEFAULT
            filename = None
            rel_file_path = None
            if media:
                if isinstance(media, MessageMediaPhoto):
                    file_type = FILE_TYPE_PHOTO
                    filename = f'{msg_id}.jpg'
                    rel_file_path = os.path.join(group_id, filename)
                    abs_file_path = os.path.join(abs_dir_path, filename)
                    await download_media(msg, abs_file_path=abs_file_path)
                elif isinstance(media, MessageMediaDocument):
                    mime_type = media.document.mime_type
                    if mime_type in MIME_TYPE_VIDEO:
                        file_type = FILE_TYPE_VIDEO
                        filename = f'{msg_id}.mp4'
                        rel_file_path = os.path.join(group_id, filename)
                        abs_file_path = os.path.join(abs_dir_path, filename)
                        await download_media(msg=msg, abs_file_path=abs_file_path)
                    elif mime_type in MIME_TYPE_IMAGE:
                        file_type = FILE_TYPE_PHOTO
                        filename = f'{msg_id}.jpg'
                        rel_file_path = os.path.join(group_id, filename)
                        abs_file_path = os.path.join(abs_dir_path, filename)
                    else:
                        logging.info(f'UpdateMsgs, unresolved mime type({mime_type})')
                elif isinstance(media, MessageMediaWebPage):
                    file_type = FILE_TYPE_WEB
                else:
                    logging.info(f'UpdateMsgs, media ({media})')
            else:
                logging.info(f'UpdateMsgs, media is None')
            content = msg.text
            msg_datetime = msg.date
            create_time = datetime.utcnow()
            update_time = datetime.utcnow()
            tg_msg = TgMsgEntity(group_id=group_id,
                                 msg_id=msg_id,
                                 from_id=from_id,
                                 to_id=to_id,
                                 file_type=file_type,
                                 content=content,
                                 filename=filename,
                                 file_path=rel_file_path,
                                 msg_datetime=msg_datetime,
                                 create_time=create_time,
                                 update_time=update_time)
            tg_msgs.append(tg_msg.to_dict())
            if msg_id == tg_group_status.last_archived_id:
                break
        await mongodb.do_bulk_upsert(col=TgMsgEntity.TABLE,
                                     data=tg_msgs,
                                     filter_key=['group_id', 'msg_id'],
                                     set_key=['from_id', 'to_id', 'file_type', 'content', 'filename',
                                              'file_path', 'update_time', 'msg_datetime'],
                                     set_on_insert_key=['group_id', 'msg_id', 'create_time'])

        await mongodb.do_bulk_upsert(col=TgGroupStatusEntity.TABLE,
                                     data=[{'_id': doc.get('_id'),
                                            'last_archive_id': msg_id,
                                            'update_time': datetime.utcnow()}],
                                     filter_key=['_id'],
                                     set_key=['last_archived_id', 'update_time'])
    else:
        await mongodb.do_bulk_upsert(col=TgGroupStatusEntity.TABLE,
                                     data=[{'_id': doc.get('_id'),
                                            'update_time': datetime.utcnow()}])
    return True


async def get_tg_data(aio_loop, url, db, config):
    mongodb = MongodbHelper(url=url, db=db)
    phone_number = config.get('PHONE_NUMBER')
    doc = await mongodb.do_find_one(col=TgAccountEntity.TABLE, filter_={'phone_number': phone_number})
    tg_account = TgAccountEntity()
    await tg_account.from_dict(doc)
    session = StringSession(tg_account.token)
    api_id = config.get('API_ID')
    api_hash = config.get('API_HASH')
    proxy = config.get('PROXY')
    client = TelegramClient(session=session, api_id=api_id, api_hash=api_hash, loop=aio_loop, proxy=proxy)
    client.add_event_handler(callback=msg_handler, event=events.NewMessage)
    try:
        await client.connect()
    except Exception as ex:
        logging.error(f'GetTgData', ex)
        return
    me = await client.get_me()
    logging.info(f'GetTgData, current user({me.id}), username({me.username}), phone number({me.phone})')
    await update_groups(client=client, mongodb=mongodb)
    try:
        interval = config.get('INTERVAL')
        msg_limit = config.get('MSG_LIMIT')
        while True:
            res = await update_msgs(client=client, mongodb=mongodb, limit=msg_limit)
            print(res)
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        logging.exception(ex)
    await client.disconnect()


def get_data(config):
    aio_loop = asyncio.get_event_loop()
    try:
        url = config.get('mongodb_url')
        db = config.get('mongodb_db')
        aio_loop.run_until_complete(get_tg_data(aio_loop, url=url, db=db, config=config))
    finally:
        if not aio_loop.is_closed():
            aio_loop.close()
