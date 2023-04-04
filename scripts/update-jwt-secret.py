import datetime
import json
import os
import psycopg


PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_DBNAME = os.getenv("PG_DBNAME")
JWT_SECRET = os.getenv("JWT_SECRET")


def main():
    try:
        with psycopg.Connection.connect(
            f"user={PG_USER} password={PG_PASSWORD} host={PG_HOST} dbname={PG_DBNAME}"
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"ALTER DATABASE {PG_DBNAME} "
                    f"SET \"app.jwt_secret\" TO '{JWT_SECRET}'"
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
                        f"failed to set jwt secret {e.__class__.__name__}: {e}"
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
                "message": "successfully updated jwt secret",
                "database": PG_DBNAME,
            }
        )
    )


main()
