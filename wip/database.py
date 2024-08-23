import sqlite3
from sqlite3 import Connection
from models import ItemModel, Items
from datetime import datetime


def get_items(connection: Connection) -> Items:
    connection.row_factory = sqlite3.Row
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT id, name, expiry_date, image, category, notes
            FROM
            items
            '''
        )
        items_list = [ItemModel(**dict(row)) for row in cur.fetchall()]
        return Items(items=items_list)


def insert_item(connection: Connection, item: ItemModel):
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            INSERT INTO items(name, expiry_date, image, category, notes)
            VALUES
            (:name, :expiry_date, :image, :category, :notes)
            ''',
            item.model_dump()
        )


if __name__ == "__main__":
    connection = sqlite3.connect("./database/food.db")
    test_item = ItemModel(name="Pydantic", expiry_date=datetime.now(), image="test", category="test_tag", notes="Buy more"
                          )
    insert_item(connection, test_item)
    print(get_items(connection))
