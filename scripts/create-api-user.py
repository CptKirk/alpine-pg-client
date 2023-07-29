import datetime
import json
import os
import psycopg


PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_DBNAME = os.getenv("PG_DBNAME")

API_EMAIL = os.getenv("API_EMAIL")
API_PASSWORD = os.getenv("API_PASSWORD")
API_ROLE = os.getenv("API_ROLE")


def main():
    try:
        with psycopg.Connection.connect(
            f"user={PG_USER} password={PG_PASSWORD} host={PG_HOST} dbname={PG_DBNAME}"
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT 1 FROM basic_auth.users WHERE email = '{API_EMAIL}';",
                )
                if cursor.fetchone() is not None:
                    cursor.execute(
                        f"DELETE FROM basic_auth.users WHERE email = '{API_EMAIL}';",
                    )
                cursor.execute(
                    "INSERT INTO basic_auth.users (email, pass, role) "
                    f"VALUES ('{API_EMAIL}', '{API_PASSWORD}', '{API_ROLE}');"
                )
    except Exception as e:
        print(
            json.dumps(
                {
                    "timestamp": datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat(),
                    "level": "ERROR",
                    "message": (
                        f"failed to create api user {e.__class__.__name__}: {e}"
                    ),
                    "database": PG_DBNAME,
                }
            )
        )
        exit(1)

    print(
        json.dumps(
            {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "level": "INFO",
                "message": "successfully created api user",
                "database": PG_DBNAME,
            }
        )
    )


main()
