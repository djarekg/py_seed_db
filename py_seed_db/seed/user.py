import psycopg2
from constants.job_title import JobTitle
from faker import Faker

from .state import get_states

ADMIN_EMAIL = 'dustin.griffith@djarekg.com'

class SeedUser:
    """Seed the user table with data."""

    def __init__(
        self,
        conn: psycopg2.extensions.connection,
        faker: Faker,
        basicUserCount: int,
        salesUserCount: int,
        accountingUserCount: int,
    ):
        """Initialize the SeedUser class."""
        self.conn = conn
        self.faker = faker
        self.basicUserCount = basicUserCount
        self.salesUserCount = salesUserCount
        self.accountingUserCount = accountingUserCount
        self.states = get_states(conn)

    def _insert_data(
        self,
        cursor: psycopg2.extensions.cursor,
        id: str,
        first_name: str,
        last_name: str,
        gender: str,
        email: str,
        phone: str,
        street_address: str,
        city: str,
        state_id: str,
        zip_code: str,
        job_title: str,
        is_active: bool,
    ):
        cursor.execute(
            """
            INSERT INTO "public"."User" (
                "id", "firstName", "lastName", "gender", "email", "phone",
                "streetAddress", "city", "stateId", "zip", "jobTitle", "isActive"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                id,
                first_name,
                last_name,
                gender,
                email,
                phone,
                street_address,
                city,
                state_id,
                zip_code,
                job_title,
                is_active,
            ),
        )

    def seed(self):
        """Seed the user table with data."""
        cursor = self.conn.cursor()

        try:
            self.seed_admin(cursor)
            self.seed_basic_user(cursor)
            self.seed_sales_user(cursor)
            self.seed_accounting_user(cursor)
            self.conn.commit()

        except psycopg2.Error as e:
            self.conn.rollback()
            raise e
        
        finally:
            cursor.close()

    def seed_admin(self, cursor: psycopg2.extensions.cursor):
        """Seed an admin user into the user table."""
        try:
            print('Seeding admin user...')

            state = self.faker.random_element(self.states)

            # Avoid unique exhaustion
            self.faker.unique.clear()

            self._insert_data(
                cursor=cursor,
                id=self.faker.unique.uuid4(),
                first_name='Dustin',
                last_name='Griffith',
                gender='MALE',
                email='dustin.griffith@djarekg.com',
                phone=self.faker.phone_number(),
                street_address=self.faker.street_address(),
                city=self.faker.city(),
                state_id=state[0],
                zip_code=self.faker.zipcode_in_state(state_abbr=state[2]),
                job_title=JobTitle.ADMIN_USER.value,
                is_active=True,
            )

        except psycopg2.Error as e:
            print(f'Error seeding admin user: {e}')
            raise e

    def seed_basic_user(self, cursor: psycopg2.extensions.cursor):
        """Seed a basic user into the user table."""
        try:
            print(f'Seeding {self.basicUserCount} basic users...')

            # Avoid unique exhaustion
            self.faker.unique.clear()

            for _ in range(self.basicUserCount):
                first_name, last_name, gender, email = _generateName(self.faker)

                self._insert_data(
                    cursor=cursor,
                    id=self.faker.unique.uuid4(),
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    email=email,
                    phone=self.faker.phone_number(),
                    street_address=self.faker.street_address(),
                    city=self.faker.city(),
                    state_id=self.faker.random_element(self.states)[0],
                    zip_code=self.faker.postcode(),
                    job_title=JobTitle.BASIC_USER.value,
                    is_active=True,
                )

        except psycopg2.Error as e:
            print(f'Error seeding basic users: {e}')
            raise e

    def seed_sales_user(self, cursor: psycopg2.extensions.cursor):
        """Seed a sales user into the user table."""
        try:
            print(f'Seeding {self.salesUserCount} sales users...')

            # Avoid unique exhaustion
            self.faker.unique.clear()

            for _ in range(self.salesUserCount):
                first_name, last_name, gender, email = _generateName(self.faker)

                self._insert_data(
                    cursor=cursor,
                    id=self.faker.unique.uuid4(),
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    email=email,
                    phone=self.faker.phone_number(),
                    street_address=self.faker.street_address(),
                    city=self.faker.city(),
                    state_id=self.faker.random_element(self.states)[0],
                    zip_code=self.faker.postcode(),
                    job_title=JobTitle.SALES_REP.value,
                    is_active=True,
                )

        except psycopg2.Error as e:
            print(f'Error seeding sales users: {e}')
            raise e

    def seed_accounting_user(self, cursor: psycopg2.extensions.cursor):
        """Seed an accounting user into the user table."""
        try:
            print(f'Seeding {self.accountingUserCount} accounting users...')

            # Avoid unique exhaustion
            self.faker.unique.clear()

            for _ in range(self.accountingUserCount):
                first_name, last_name, gender, email = _generateName(self.faker)

                self._insert_data(
                    cursor=cursor,
                    id=self.faker.unique.uuid4(),
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    email=email,
                    phone=self.faker.phone_number(),
                    street_address=self.faker.street_address(),
                    city=self.faker.city(),
                    state_id=self.faker.random_element(self.states)[0],
                    zip_code=self.faker.postcode(),
                    job_title=JobTitle.ACCOUNTING_SPEC.value,
                    is_active=True,
                )

        except psycopg2.Error as e:
            print(f'Error seeding accounting users: {e}')
            raise e


def seed_users(conn:  psycopg2.extensions.connection, faker: Faker) -> None:
    """Convenience function to seed users."""
    seeder = SeedUser(conn, faker, 50, 20, 10)
    seeder.seed()


def _generateName(fake: Faker) -> tuple[str, str, str, str]:
    """Generate a name and email address based on gender."""
    gender = fake.random_element(['MALE', 'FEMALE'])

    # Generate first name based on gender
    first_name = (
        fake.first_name_male()
        if gender == 'MALE'
        else fake.first_name_female()
    )

    # Generate last name based on gender
    last_name = (
        fake.last_name_male()
        if gender == 'MALE'
        else fake.last_name_female()
    )

    email = f"{first_name.lower()}.{last_name.lower()}@djarekg.com"

    return (first_name, last_name, gender, email)


def get_users_id_by_job_title(
    conn: psycopg2.extensions.connection,
    job_title: str
) -> list[str]:
    """Get user IDs from the user table by job title."""
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT "id" FROM "public"."User"
            WHERE "jobTitle" = %s
            """,
            (job_title,)
        )

        user_ids: list[str] = []
        users: list[tuple[str, ...]] = cursor.fetchall()
        for user in users:
            user_ids.append(user[0])

        return user_ids

    except psycopg2.Error as e:
        print(f"Error fetching user IDs by job title: {e}")
        return []

    finally:
        cursor.close()