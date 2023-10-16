from sqlalchemy import create_engine
#
DATABASE_URL = "postgresql://same_base_db:same_password@localhost/same_user"
#
engine = create_engine(DATABASE_URL)