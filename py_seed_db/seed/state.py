import psycopg2
from faker import Faker

STATE_COUNT = 50


def seed_state(conn: psycopg2.extensions.connection, fake: Faker) -> None:
    """Seed the state table with data (default: 50 US states)."""
    cursor = conn.cursor()

    try:
        print(f'Seeding {STATE_COUNT} states...')

        # Clear unique cache to avoid exhausting unique values
        fake.unique.clear()

        for _ in range(STATE_COUNT):
            cursor.execute(
                """
                INSERT INTO "public"."State" ("id", "name", "code")
                VALUES (%s, %s, %s)
                """,
                (
                    fake.unique.uuid4(),
                    fake.unique.state(),
                    fake.unique.state_abbr(),
                ),
            )

        conn.commit()
        print(f'Successfully seeded {STATE_COUNT} states')

    except psycopg2.Error as e:
        conn.rollback()
        print(f'Error seeding states: {e}')
    finally:
        cursor.close()


def get_states(conn: psycopg2.extensions.connection) -> list[tuple[str, str, str]]:
    """Retrieve all states from the state table."""
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT "id", "name", "code" FROM "public"."State"')
        states = cursor.fetchall()
        return states
    except psycopg2.Error as e:
        print(f'Error retrieving states: {e}')
        return []
    finally:
        cursor.close()
