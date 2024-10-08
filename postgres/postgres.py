import logging

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session, declarative_base

DB_URL = 'postgresql://postgres:password@localhost/postgres'

Base = declarative_base()
logger = logging.getLogger(__name__)


class Users(Base):
    __tablename__ = 'users'

    tg_id = Column(Integer, primary_key=True)
    username = Column(String)
    active_key = Column(String)


class UserFilters(Base):
    __tablename__ = 'user_filters'

    id_filter = Column(Integer, primary_key=True, autoincrement=True)
    id_owner = Column(Integer, ForeignKey('users.tg_id'))
    saved_filter_name = Column(String)


class FiltersMethods(Base):
    __tablename__ = 'filters_methods'

    id_method = Column(Integer, primary_key=True, autoincrement=True) # created solely for primary key
    id_filter = Column(Integer, ForeignKey('user_filters.id_filter')) 
    filter_method = Column(String)
    filter_method_readable = Column(String)
    argument = Column(String)
    arg_readable = Column(String)
    
    
class LicenseKey(Base):
    __tablename__ = 'keys'

    license_key = Column(String, primary_key=True)

    


class DatabaseManager:
    """Class to manage database operations for the bot. Uses SQLAlchemy ORM."""

    def __init__(self, db_url):
        """Connect to the database and create the necessary tables."""

        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))
        logger.info("Connected to DB")

    def add_user(self, username, tg_id, active_key):
        """Add a new user to the database."""

        session = self.session_factory()  
        try:
            new_user = Users(username=username, tg_id=tg_id, active_key=active_key)
            session.add(new_user)
            session.commit()
            logger.info("User added")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add user: {e}")
        finally:
            session.close()

    def get_all_users(self):
        """Fetch all users from the database."""
        session = self.session_factory()
        try:
            users = session.query(Users).all()
            return users
        except Exception as e:
            logger.error(f"Failed to fetch users: {e}")
            return []
        finally:
            session.close()

    def get_all_keys(self):
        """Fetch all license keys from the database"""
        session = self.session_factory()
        try:
            keys_list = session.query(LicenseKey).all()  
            keys = [key.license_key for key in keys_list]
            return keys
        except Exception as e:
            logger.error(f"Failed to fetch keys: {e}")
            return []  
        finally:
            session.close()

    def save_user_filter_to_db(self, tg_id, name_for_filter):
        """Save user filter to the database and return its newly created db ID."""
        session = self.session_factory()
        try:
            new_user_filter = UserFilters(id_owner=tg_id, saved_filter_name=name_for_filter)
            session.add(new_user_filter)
            session.commit()
            user_filter_id = new_user_filter.id_filter
            logger.info(f"UserFilter '{name_for_filter}' added with ID {user_filter_id}")
            # Return the ID of the newly created filter 
            return user_filter_id  
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add userfilter: {e}")
            return None  # Indicate failure
        finally:
            session.close()


    def save_filter_method_to_db(self, id, region_set, filter_list):
        """Save filter methods to the database."""
        session = self.session_factory()  
        try:
            if region_set:
                for region in region_set:
                    region_method = FiltersMethods(id_filter=id, filter_method='region', filter_method_readable='Регион', argument=region, arg_readable=region)
                    session.add(region_method)
            if filter_list:
                for filter in filter_list:
                    filter_method = FiltersMethods(id_filter=id, filter_method=filter.filter_method.__name__, filter_method_readable=filter.filter_method_readable, argument=str(filter.arg), arg_readable=filter.arg_readable)
                    session.add(filter_method)
            session.commit()
            logger.info(f"Filter methods for filter {id} added")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add filter methods: {e}")
        finally:
            session.close()

    def get_all_user_filters(self, user):
        """Fetch all filters for a user defined by their tg_id."""
        session = self.session_factory()
        try: 
            results = session.query(UserFilters).filter_by(id_owner=user.tg_id).with_entities(UserFilters.id_filter, UserFilters.saved_filter_name).all()
            user_filters = [[id_filter, saved_filter_name] for id_filter, saved_filter_name in results]
            return user_filters
        except Exception as e:
            logger.error(f"Failed to fetch user filters: {e}")
            return []
        finally:
            session.close()

    def get_user_filters_by_name(self, user, str_req):
        """Fetch all filters for a user defined by their tg_id and filters name."""
        session = self.session_factory()
        try: 
            results = session.query(UserFilters).filter_by(id_owner=user.tg_id).with_entities(UserFilters.id_filter, UserFilters.saved_filter_name).all()
            user_filters = [[id_filter, saved_filter_name] for id_filter, saved_filter_name in results if saved_filter_name.find(str_req) != -1]
            return user_filters
        except Exception as e:
            logger.error(f"Failed to fetch user filters: {e}")
            return []

    def load_user_filters(self, filters_id):
        """Fetch filter methods for a given filter ID."""
        session = self.session_factory()
        try:
            results = session.query(FiltersMethods).filter_by(id_filter=filters_id).all()
            filter_methods = [[result.filter_method, result.filter_method_readable, 
                               result.argument, result.arg_readable] for result in results]
            return filter_methods
        except Exception as e:
            logger.error(f"Failed to fetch filter methods: {e}")
            return []
        finally:
            session.close()

    def delete_user_filter(self, filter_id):
        """Delete a user filter and all the realted filter methods"""
        session = self.session_factory()
        try:
            session.query(FiltersMethods).filter_by(id_filter=filter_id).delete()
            session.query(UserFilters).filter_by(id_filter=filter_id).delete()
            session.commit()
            logger.info(f"Filter {filter_id} deleted")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete filter: {e}")
        finally:
            session.close()






