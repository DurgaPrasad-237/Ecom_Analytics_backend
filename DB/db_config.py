from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DB_USER = "root"
DB_PASSWORD = "nani"
DB_HOST = "localhost"
DB_PORT = "3307"
DB_NAME = "indian_ecommerce_dw"

class Base(DeclarativeBase):
    pass

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)