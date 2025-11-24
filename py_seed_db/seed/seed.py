from db.connection import get_db_connection
from db.reset import reset_tables
from faker import Faker

from .customer import seed_customer
from .customer_contact import seed_customer_contacts
from .state import seed_state
from .user import seed_users
from .user_credentials import seed_user_credentials

faker = Faker()
Faker.seed(4321)

def seed_db():
    conn = get_db_connection()

    if reset_tables():
        seed_state(conn, faker)
        seed_users(conn, faker)
        seed_user_credentials(conn, faker)
        seed_customer(conn, faker)
        seed_customer_contacts(conn, faker)
    
    conn.close()