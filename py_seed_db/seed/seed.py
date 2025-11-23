from faker import Faker

fake = Faker()
Faker.seed(4321)

def seed_db():
    from db.connection import get_db_connection
    from db.reset import reset_tables

    from .state import seed_state
    from .user import seed_user

    conn = get_db_connection()

    if reset_tables():
        seed_state(conn, fake)
        seed_user(conn, fake)
        
    conn.close()