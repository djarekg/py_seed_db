import psycopg2
from faker import Faker

from .state import get_states


def seed_user(
    conn: psycopg2.extensions.connection, fake: Faker, count: int = 100
) -> None:
    """Seed the user table with data."""
    states = get_states(conn)

    cursor = conn.cursor()

    try:
        print(f'Seeding {count} users...')

        # Clear unique cache to avoid exhausting unique values
        fake.unique.clear()

        for _ in range(count):
            cursor.execute(
                """
                INSERT INTO "public"."User" (
                    "id", "firstName", "lastName", "gender", "email", "phone",
                    "streetAddress", "city", "stateId", "zip", "jobTitle", "isActive"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    fake.unique.uuid4(),
                    fake.first_name(),
                    fake.last_name(),
                    'MALE' if fake.boolean(chance_of_getting_true=50) else 'FEMALE',
                    fake.unique.email(),
                    fake.phone_number(),
                    fake.street_address(),
                    fake.city(),
                    # pick a random state id from the states table
                    fake.random_element(states)[0],
                    fake.zipcode(),
                    fake.job(),
                    fake.boolean(chance_of_getting_true=80),
                ),
            )

        conn.commit()
        print(f'Successfully seeded {count} users')

    except psycopg2.Error as e:
        conn.rollback()
        print(f'Error seeding users: {e}')
    finally:
        cursor.close()
