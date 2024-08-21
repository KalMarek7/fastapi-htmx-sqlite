import sqlite3
from sqlite3 import Connection
from models import Recipie, Recipies


def get_pies(connection: Connection) -> Recipies:
    connection.row_factory = sqlite3.Row
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT rpie_id, rpie_title, rpie_text
            FROM
            recipies
            '''
        )
        recipies_list = [Recipie(**dict(row)) for row in cur.fetchall()]
        return Recipies(recipies=recipies_list)


def insert_pies(connection: Connection, pie: Recipie):
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            INSERT INTO recipies(rpie_title, rpie_text)
            VALUES
            ( :rpie_title, :rpie_text)
            ''',
            pie.model_dump()
        )


if __name__ == "__main__":
    connection = sqlite3.connect("pie.db")
    test_rpie = Recipie(rpie_title="Pydantic", rpie_text="Sweet"
                        )
    # insert_pies(connection, test_rpie)
    print(get_pies(connection))
