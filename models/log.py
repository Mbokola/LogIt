from db import DB, Base
from sqlalchemy import Column, Text, Integer


class Log:
    """ Class defination for user logs
    """
    def __init__(self):
        """ Log initialization
        """
        self.database = DB()

    def create_log(self, log_name, fields):
        """ Creates user log
        """
        attrs = {'__tablename__': log_name}
        attrs['id'] = Column(Integer, primary_key=True)
        for field in fields:
            field_type = Text
            length = None
            attrs[field] = Column(field_type(length=length))

        log = type(log_name, (Base,), attrs)
        self.database.create_table(log)

    def all_logs(self):
        """ Retrieves all logs
        """
        all_logs = [log for log in self.database.get_tables()]
        return all_logs

    def get_log_field(self, log_name):
        """ Retrieves fields for a particular log
        """
        all_logs = self.database.get_tables()
        for log, fields in all_logs.items():
            if log == log_name:
                log_fields = [field.name for field in fields.columns]
        return log_fields

    def make_log_entry(self, log_name, data):
        """ This will make entries into our log
        """
        table = self.database.get_tables().get(log_name)

        log_entry = table.insert().values(data)
        self.database.log_entry(log_entry)
