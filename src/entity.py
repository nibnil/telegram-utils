from datetime import datetime

DOMAIN_DEFAULT = 0
ACCOUNT_STATUS_DEFAULT = 0
GROUP_STATUS_DEFAULT = 0
FIle_TYPE_DEFAULT = 0


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
                 target: str = None,
                 username: str = None,
                 token: str = None,
                 account_status: int = ACCOUNT_STATUS_DEFAULT,
                 create_time: datetime = None,
                 update_time: datetime = None):
        self.account_id = account_id
        self.domain = domain
        self.target = target
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
                 last_archived_id: int = None,
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
                 file_type: int = FIle_TYPE_DEFAULT,
                 content: str = None,
                 file_name: str = None,
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
        self.file_name = file_name
        self.file_path = file_path
        self.msg_datetime = msg_datetime
        self.create_time = create_time
        self.update_time = update_time
