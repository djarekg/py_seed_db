from typing import Any

import psycopg2
from faker import Faker

from .state import get_states


class SeedCustomer:
    """Class responsible for seeding the Customer table."""

    def __init__(
        self, conn: psycopg2.extensions.connection, faker: Faker, count: int
    ):
        self.conn = conn
        self.faker = faker
        self.count = count

    def _insert_data(
        self,
        cursor: psycopg2.extensions.cursor,
        id: str,
        name: str,
        street_address: str,
        city: str,
        state_id: str,
        zip_code: str,
        phone: str,
        is_active: bool,
    ):
        """Insert a customer record into the Customer table."""
        cursor.execute(
            """
            INSERT INTO "public"."Customer" (
                "id", "name", "streetAddress", "city", "stateId", "zip", "phone", "isActive"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                id,
                name,
                street_address,
                city,
                state_id,
                zip_code,
                phone,
                is_active,
            ),
        )

    def seed(self) -> None:
        """Seed the Customer table with data."""
        print(f'Seeding {self.count} customers...')

        cursor = self.conn.cursor()

        try:
            # Clear unique cache to avoid exhausting unique values
            self.faker.unique.clear()

            states = get_states(self.conn)

            for _ in range(self.count):
                state = self.faker.random_element(states)

                self._insert_data(
                    cursor=cursor,
                    id=self.faker.unique.uuid4(),
                    name=self.faker.company(),
                    street_address=self.faker.street_address(),
                    city=self.faker.city(),
                    state_id=state[0],
                    zip_code=self.faker.zipcode_in_state(state_abbr=state[2]),
                    phone=self.faker.phone_number(),
                    is_active=True,
                )

            self.conn.commit()
            print(f'Successfully seeded {self.count} customers')

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f'Error seeding customers: {e}')
            raise e

        finally:
            cursor.close()


def seed_customer(conn: psycopg2.extensions.connection, faker: Faker) -> None:
    """Convenience function that seeds the Customer table."""
    seeder = SeedCustomer(conn, faker, 200)
    seeder.seed()


def get_customers(conn: psycopg2.extensions.connection) -> list[tuple[Any, ...]]:
    """Retrieve all customers from the Customer table."""
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT "id", "streetAddress", "city", "stateId", "zip"
            FROM "public"."Customer"
            """
        )
        customers = cursor.fetchall()
        return customers

    except psycopg2.Error as e:
        print(f'Error retrieving customers: {e}')
        return []

    finally:
        cursor.close()