from .db_info import DbInfo
import pymssql


class MSSqlInfo(DbInfo):
    db_type_label = 'MSSql'

    def __init__(self, host, port, admin_user, admin_password):
        super().__init__()
        self.host = host
        self.port = port or 1433
        self.user = admin_user
        self.password = admin_password
        self.connector = pymssql

    def query_version(self):
        return self.query("""SELECT @@VERSION""", 0, 0)

    def query_uptime(self):
        return self.query("""SELECT login_time AS START_TIME_INSTANCE FROM sys.sysprocesses WHERE spid = 1""", 0, 0)

    def query_connection_count(self):
        return self.query("""SELECT @@Connections""", 0, 0)
