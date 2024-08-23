import sqlite3
from sqlite3 import Connection
from models import ItemModel, Items, UploadItem, Images
from datetime import datetime


""" def get_items(connection: Connection) -> Items:
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
        print(item.image)
        cur.execute(
            '''
            INSERT INTO items(name, expiry_date, image, category, notes)
            VALUES
            (:name, :expiry_date, :image, :category, :notes)
            ''',
            item.model_dump()
        ) """


def insert_image(connection: Connection, item: UploadItem):
    with connection:
        cur = connection.cursor()
        # print(item.image)
        cur.execute(
            '''
            INSERT INTO pictures(src, filename, filesize)
            VALUES
            (:src, :filename, :filesize)
            ''',
            item.model_dump()
        )


def get_images(connection: Connection) -> Images:
    connection.row_factory = sqlite3.Row
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT id, src, filename, filesize
            FROM
            pictures
            '''
        )
        images_list = [UploadItem(**dict(row)) for row in cur.fetchall()]
        print(images_list)
        return Images(images=images_list)


if __name__ == "__main__":
    connection = sqlite3.connect("./database/food.db")
    test_item = ItemModel(name="Pydantic", expiry_date=datetime.now(), image="test", category="test_tag", notes="Buy more"
                          )
    # insert_item(connection, test_item)
    # print(get_items(connection))
