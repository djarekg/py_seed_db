import psycopg2
from faker import Faker

from .customer import get_customers


class SeedCustomerContact:
    """Class to seed the CustomerContact table with data."""

    def __init__(
        self,
        conn: psycopg2.extensions.connection,
        faker: Faker,
        count: int = 100,
    ):
        self.conn = conn
        self.faker = faker
        self.count = count

    def _insert_data(
        self,
        cursor: psycopg2.extensions.cursor,
        id: str,
        customer_id: str,
        first_name: str,
        last_name: str,
        email: str,
        street_address: str,
        city: str,
        state_id: str,
        zip_code: str,
        phone: str,
        is_active: bool,
    ):
        """Insert a customer contact record into the CustomerContact table."""
        cursor.execute(
            """
            INSERT INTO "public"."CustomerContact" (
                "id", "customerId", "firstName", "lastName", "email", "streetAddress",
                "city", "stateId", "zip", "phone", "isActive"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                id,
                customer_id,
                first_name,
                last_name,
                email,
                street_address,
                city,
                state_id,
                zip_code,
                phone,
                is_active,
            ),
        )

    def seed(self) -> None:
        """Seed the CustomerContact table with data."""
        print(f'Seeding {self.count} customer contacts per customer...')

        cursor = self.conn.cursor()

        try:
            # Clear unique cache to avoid exhausting unique values
            self.faker.unique.clear()

            customers = get_customers(self.conn)

            first_name = self.faker.unique.first_name()
            last_name = self.faker.unique.last_name()
            email = f'{first_name.lower()}.{last_name.lower()}@idk.fu'

            for customer in customers:
                for _ in range(self.count):
                    self._insert_data(
                        cursor=cursor,
                        id=self.faker.unique.uuid4(),
                        customer_id=customer[0],
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        street_address=customer[1],
                        city=customer[2],
                        state_id=customer[3],
                        zip_code=customer[4],
                        phone=self.faker.phone_number(),
                        is_active=True,
                    )

            self.conn.commit()
            print(f'Successfully seeded {self.count * len(customers)} customer contacts')

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f'Error seeding customer contacts: {e}')

        finally:
            cursor.close()


def seed_customer_contacts(conn: psycopg2.extensions.connection, faker: Faker) -> None:
    """Convenience function that seeds the CustomerContact table."""
    seeder = SeedCustomerContact(conn, faker, 10)
    seeder.seed()