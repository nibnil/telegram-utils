from datetime import datetime

# domain
DOMAIN_DEFAULT = 0

# account status
ACCOUNT_STATUS_DEFAULT = 0

# group status
GROUP_STATUS_DEFAULT = 0
GROUP_STATUS_WATCH = 1

# file type
FILE_TYPE_DEFAULT = 0
FILE_TYPE_PHOTO = 1
FILE_TYPE_VIDEO = 2
FILE_TYPE_WEB = 3

# mime type
MIME_TYPE_VIDEO = ['video/mp4']
MIME_TYPE_IMAGE = ['image/webp']


class BaseEntity:

    def to_dict(self):
        item = dict()
        for key, value in vars(self).items():
            item[key] = value
        return item

    async def from_dict(self, item: dict):
        self.__dict__.update(item)
        return self


class TgAccountEntity(BaseEntity, ):

    TABLE = 'tg_account'

    def __init__(self,
                 account_id: str = None,
                 domain: int = DOMAIN_DEFAULT,
                 phone_number: str = None,
                 username: str = None,
                 token: str = None,
                 account_status: int = ACCOUNT_STATUS_DEFAULT,
                 create_time: datetime = None,
                 update_time: datetime = None):
        self.account_id = account_id
        self.domain = domain
        self.phone_number = phone_number
        self.username = username
        self.token = token
        self.account_status = account_status
        self.create_time = create_time
        self.update_time = update_time


class TgGroupEntity(BaseEntity, ):

    TABLE = 'tg_group'

    def __init__(self,
                 group_id: str = None,
                 group_name: str = None,
                 username: str = None,
                 group_create_time: datetime = None,
                 create_time: datetime = None,
                 update_time: datetime = None):
        self.group_id = group_id
        self.group_name = group_name
        self.username = username
        self.group_create_time = group_create_time
        self.create_time = create_time
        self.update_time = update_time


class TgGroupStatusEntity(BaseEntity, ):

    TABLE = 'tg_group_status'

    def __init__(self,
                 group_id: str = None,
                 group_status: int = GROUP_STATUS_DEFAULT,
                 last_datetime: datetime = None,
                 last_msg_id: int = None,
                 last_archived_id: int = 0,
                 create_time: datetime = None,
                 update_time: datetime = None):
        self.group_id = group_id
        self.group_status = group_status
        self.last_datetime = last_datetime
        self.last_msg_id = last_msg_id
        self.last_archived_id = last_archived_id
        self.create_time = create_time
        self.update_time = update_time


class TgMsgEntity(BaseEntity, ):

    TABLE = 'tg_msg'

    def __init__(self,
                 group_id: str = None,
                 msg_id: int = None,
                 from_id: str = None,
                 to_id: str = None,
                 file_type: int = FILE_TYPE_DEFAULT,
                 content: str = None,
                 filename: str = None,
                 file_path: str = None,
                 msg_datetime: datetime = None,
                 create_time: datetime = None,
                 update_time: datetime = None):
        self.group_id = group_id
        self.msg_id = msg_id
        self.from_id = from_id
        self.to_id = to_id
        self.file_type = file_type
        self.content = content
        self.filename = filename
        self.file_path = file_path
        self.msg_datetime = msg_datetime
        self.create_time = create_time
        self.update_time = update_time
