from src.db.session import Base, engine
from src.models.expense import Expense

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
