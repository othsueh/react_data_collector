from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

"""
- Creates a SQLAlchemy engine object that manages the database connection pool
- The engine handles the actual connection to your database
- It doesn't establish a connection yet - that happens when you first use it
"""
engine = create_engine(DB_URL)

"""
- Creates a session factory that will generate database sessions
- autocommit=False: Changes aren't automatically committed to the database
- autoflush=False: Changes aren't automatically flushed to the database
- bind=engine: Associates this session factory with the engine
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
- Creates a base class for your database models
- You'll inherit from this class when defining your database tables/models
"""
Base = declarative_base()

def test_connection():
    """Test if we can connect to the database"""
    try:
        # Try to connect
        connection = engine.connect()
        print("✅ Successfully connected to the database!")
        
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
