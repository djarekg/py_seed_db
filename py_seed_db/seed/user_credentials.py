
import psycopg2
from constants.job_title import JobTitle
from constants.role import Role
from faker import Faker
from utils.hash import hash_password

from .user import get_users_id_by_job_title


class SeedUserCredentials:
    """Class to seed UserCredential table."""

    def __init__(self, conn: psycopg2.extensions.connection, faker: Faker):
        self.conn = conn
        self.faker = faker

    def _insert_data(self, cursor: psycopg2.extensions.cursor, id: str, user_id: str, password: str, role: str):
        """Seed the UserCredential table with data."""

        cursor.execute(
            """
            INSERT INTO "public"."UserCredential" (
                "id", "userId", "password", "role"
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                id,
                user_id,
                password,
                role,
            ),
        )

    def seed(self):
        """Seed the UserCredential table with data."""
        cursor = self.conn.cursor()

        try:
            self._seed_user_credentials(
                cursor=cursor,
                job_title=JobTitle.ADMIN_USER.value,
                role=Role.ADMIN.value,
                default_password='admin',
            )

            self._seed_user_credentials(
                cursor=cursor,
                job_title=JobTitle.BASIC_USER.value,
                role=Role.USER.value,
                default_password='password123',
            )

            self._seed_user_credentials(
                cursor=cursor,
                job_title=JobTitle.SALES_REP.value,
                role=Role.SALES.value,
                default_password='password123',
            )

            self._seed_user_credentials(
                cursor=cursor,
                job_title=JobTitle.ACCOUNTING_SPEC.value,
                role=Role.ACCOUNTING.value,
                default_password='password123',
            )
 
            self.conn.commit()
        
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e
        
        finally:
            cursor.close()
            
    def _seed_user_credentials(self, cursor: psycopg2.extensions.cursor, job_title: str, role: str, default_password: str):
        """Seed default user credentials into the UserCredential table."""
        print(f'Seeding user credentials for `{role}`')

        try:
            user_ids = get_users_id_by_job_title(self.conn, job_title)

            for user_id in user_ids:
                self._insert_data(
                    cursor=cursor,
                    id=self.faker.unique.uuid4(),
                    user_id=user_id,
                    password=hash_password(default_password),
                    role=role,
                )

        except Exception as e:
            print(f'Error seeding user credentials for `{role}`: {e}')
            raise e

def seed_user_credentials(conn: psycopg2.extensions.connection, faker: Faker) -> None:
    """Convenience function that seeds the UserCredential table."""
    seeder = SeedUserCredentials(conn, faker)
    seeder.seed()