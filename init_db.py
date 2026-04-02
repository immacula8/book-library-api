# init_db.py - Creates database tables

from database import engine
from models import Base

# Create all tables defined in models
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")