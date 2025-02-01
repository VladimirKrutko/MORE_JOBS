import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)



engine = create_engine(DATABASE_URL,
                       pool_size=20,
                       max_overflow=30,
                       pool_timeout=30 )

Session = sessionmaker(bind=engine)
Base = declarative_base()
