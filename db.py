import sqlite3


def initiate_db() -> None:
    database_connection = sqlite3.connect("settings.db")
    cursor = database_connection.cursor()
    cursor.execute(
        """CREATE TABLE if not exists settings (
            file_name text,
            file_extension text,
            prompt text,
            file_number text,
            priority text,
            priority_value real
        )"""
    )
    database_connection.commit()
    database_connection.close()


def save_db(data: list) -> None:
    database_connection = sqlite3.connect("settings.db")
    cursor = database_connection.cursor()
    cursor.execute(
        "DELETE FROM settings;",
    )

    for item in data:
        cursor.execute("INSERT INTO settings VALUES (?,?,?,?,?,?)", item)

    database_connection.commit()
    database_connection.close()


def extract_db() -> list:
    database_connection = sqlite3.connect("settings.db")
    cursor = database_connection.cursor()
    cursor.execute("SELECT * FROM settings")
    data = cursor.fetchall()
    database_connection.commit()
    database_connection.close()
    return data


if __name__ == "__main__":
    initiate_db()
