from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection string matching our docker-compose credentials
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Madhan%2307@localhost:5432/customer_approval_db"
# DATABASE_URL=postgresql://postgres:Madhan%2307@localhost:5432/customer_approval_db

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()