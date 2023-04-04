import datetime
import json
import os
import sys
import psycopg

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
TIMESCALEDB_VERSION = os.getenv("TIMESCALEDB_VERSION")
TIMESCALEDB_TOOLKIT_VERSION = os.getenv("TIMESCALEDB_TOOLKIT_VERSION")
TIMESCALE = {
    "timescaledb": TIMESCALEDB_VERSION,
    "timescaledb_toolkit": TIMESCALEDB_TOOLKIT_VERSION,
}


def _update_extension(db_name: str, extension_name: str, extension_version: str):
    query = f"ALTER EXTENSION {extension_name} UPDATE TO '{extension_version}'"
    command = 'PGPASSWORD={} psql -X -h {} -d {} -U {} -c "{}"'.format(
        PG_PASSWORD, PG_HOST, db_name, PG_USER, query
    )
    return os.system(command)


def _get_extension_versions(db_name: str):
    with psycopg.Connection.connect(
        f"user={PG_USER} password={PG_PASSWORD} host={PG_HOST} dbname={db_name}"
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT extname, extversion FROM pg_extension "
                "WHERE extname = 'timescaledb' OR extname = 'timescaledb_toolkit'"
            )
            return cursor.fetchall()


def main():
    db_name = sys.argv[1]
    try:
        loaded_extensions = _get_extension_versions(db_name)
    except Exception as e:
        print(
            json.dumps(
                {
                    "timestamp": datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat(),
                    "level": "ERROR",
                    "message": (
                        "failed to get versions of extensions with error "
                        f"{e.__class__.__name__}: {e}"
                    ),
                    "database": db_name,
                }
            )
        )
        exit(1)

    for extension in loaded_extensions:
        if TIMESCALE[extension[0]] == extension[1]:
            continue
        return_code = _update_extension(db_name, extension[0], TIMESCALE[extension[0]])
        if return_code != 0:
            print(
                json.dumps(
                    {
                        "timestamp": datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat(),
                        "level": "ERROR",
                        "message": (f"failed to update version of {extension[0]}"),
                        "database": db_name,
                    }
                )
            )
            exit(1)

        print(
            json.dumps(
                {
                    "timestamp": datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat(),
                    "level": "INFO",
                    "message": f"successfully updated {extension[0]}",
                    "database": db_name,
                }
            )
        )


main()
