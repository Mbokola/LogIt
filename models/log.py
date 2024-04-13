from .db import DB, Base
from sqlalchemy import Column, Text, Integer


class Log:
    """ Class defination for user logs
    """
    def __init__(self):
        """ Log initialization
        """
        self._database = DB()

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
        self._database.create_table(log)

    def all_logs(self):
        """ Retrieves all logs
        """
        all_logs = [log for log in self._database.get_tables()]
        return all_logs

    def get_log_field(self, log_name):
        """ Retrieves fields for a particular log
        """
        all_logs = self._database.get_tables()
        log_fields = []
        for log, fields in all_logs.items():
            if log == log_name:
                log_fields = [field.name for field in fields.columns]
        return log_fields

    def make_log_entry(self, log_name, data):
        """ This will make entries into our log
        """
        table = self._database.get_tables().get(log_name)

        log_entry = table.insert().values(data)
        self._database.log_entry(log_entry)

    def retrieve_log(self, log_name):
        """ Retrieves entries from log
        """
        table = self._database.get_tables().get(log_name)
        logs = self._database.get(table)
        return logs

    def get_log(self, log_name, criteria):
        """ Retieves specific log entry
        """
        table = self._database.get_tables().get(log_name)
        log = self._database.get_row(table, criteria)
        return log

    def del_log(self, log_name):
        """ Deletes a log from database
        """
        self._database.del_log(log_name)
        self._database._session.commit()
