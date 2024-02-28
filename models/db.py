from sqlalchemy import create_engine, MetaData, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DB:
    """ This class will setup the database
    """
    def __init__(self):
        """ Database initalization
        """
        self._engine = create_engine("sqlite:///logs.db")
        self.metadata = MetaData()
        self.__session = None

    @property
    def _session(self):
        """ Creates database session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def log_entry(self, log_entry):
        """ Will add a log to the database
        """
        self._session.execute(log_entry)
        self._session.commit()

    def get_tables(self):
        """ Retrieves all user logs
        """
        self.metadata.reflect(bind=self._engine)
        tables = self.metadata.tables
        return tables

    def find_by(self, log_name, keyword, column):
        """ Find logs based on keyword
        """
        query = self._session.query(log_name).filter(
            or_(log_name.column.ilike(f"%{keyword}%")))

        result = query.all()

        return result

    def del_log(self, log_name):
        """ Deletes a log
        """
        table = self.metadata.tables[log_name]
        table.drop(self._engine)

    def del_entry(self, log_name):
        """ Deletes log entry
        """
        query = self._session.query(log_name).all()
        return query

    def create_table(self, log):
        """ Creates a table based on obj
        """
        log.metadata.create_all(self._engine)

    def get(self, log_name):
        """ Retrieves table entries
        """
        query = self._session.query(log_name).all()
        return query

    def get_row(self, log_name, criteria):
        """ Retrieve a row based on id
        """
        query = self._session.query(log_name).filter_by(**criteria)
        results = query.all()

        return results
