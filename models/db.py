from sqlalchemy import create_engine, MetaData, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from .user import Base, User


class DB:
    """ This class will setup the database
    """
    def __init__(self):
        """ Database initalization
        """
        self._engine = create_engine("mysql+mysqlconnector://root:root/root@localhost:3306/logs")
        self._auth_engine = create_engine('sqlite:///auth.db')
        Base.metadata.create_all(self._auth_engine)
        self.metadata = MetaData()
        self.__session = None
        self.__auth_session = None
    # Following are definations for Logging functionality

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
        self.metadata.clear()
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
        Base.metadata.remove(table)

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

    # Following are definations for auth service

    @property
    def _authsession(self):
        """ Creates authentication session
        """
        if self.__auth_session is None:
            DBSession = sessionmaker(bind=self._auth_engine)
            self.__auth_session = DBSession()
        return self.__auth_session

    def find_user_by(self, **kwargs):
        """ Finds a user from the database based on kwargs """
        try:
            records = self._authsession.query(User).filter_by(**kwargs).first()
            if records is None:
                raise NoResultFound
            return records
        except InvalidRequestError as e:
            raise e

    def add_user(self, email, hashed_password):
        """ Saves user to database and returns the user object
        """
        user = User(
            email=email,
            hashed_password=hashed_password
        )
        self._authsession.add(user)
        self._authsession.commit()
        return user

    def update_user(self, user_id, **kwargs):
        """ Updates user records
        """
        user_recods = self.find_user_by(id=user_id)

        for key, new_value in kwargs.items():
            if hasattr(user_recods, key):
                setattr(user_recods, key, new_value)
                self._authsession.commit()
            else:
                raise ValueError
