from models import ItemModel, Items, UploadItem, Images
import sqlite3
from sqlite3 import Connection
from datetime import timedelta, datetime


def get_items(connection: Connection) -> Items:
    connection.row_factory = sqlite3.Row
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT items.id AS item_id, items.name, items.expiry_date, pictures.src AS image, items.category, items.notes, pictures.id AS picture_id
            FROM items
            JOIN pictures ON items.picture_id = pictures.id;
            '''
        )
        items_list = [ItemModel(**dict(row)) for row in cur.fetchall()]
        # print(items_list)
        return Items(items=items_list)


def insert_item(connection: Connection, item: ItemModel):
    with connection:
        cur = connection.cursor()
        # print(item)
        cur.execute(
            '''
            INSERT INTO items(name, expiry_date, picture_id, category, notes)
            VALUES
            (:name, :expiry_date, :picture_id, :category, :notes)
            ''',
            item.model_dump()
        )


def insert_image(connection: Connection, item: UploadItem):
    with connection:
        cur = connection.cursor()
        # print(item.image)
        cur.execute(
            '''
            INSERT INTO pictures(src, filename, filesize, initial)
            VALUES
            (:src, :filename, :filesize, :initial)
            ''',
            item.model_dump()
        )


def get_images(connection: Connection) -> Images:
    connection.row_factory = sqlite3.Row
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT id, src, filename, filesize, initial
            FROM
            pictures
            '''
        )
        images_list = [UploadItem(**dict(row)) for row in cur.fetchall()]
        # print(images_list)
        return Images(images=images_list)


def update_image(connection: Connection, id: int):
    connection.row_factory = sqlite3.Row
    with connection:
        cur = connection.cursor()
        cur.execute(
            f'''
            UPDATE pictures
            SET initial = False
            WHERE id = {id};
            '''
        )


def date_filtered_items(connection: Connection) -> Items:
    connection.row_factory = sqlite3.Row
    with connection:
        cur = connection.cursor()
        today = datetime.now().date()
        print(today)
        delta = today + timedelta(days=3)
        print(delta)
        """ query = '''
            SELECT items.id AS item_id, items.name, items.expiry_date, pictures.src AS image, items.category, items.notes, pictures.id AS picture_id
            FROM items
            JOIN pictures ON items.picture_id = pictures.id
            WHERE items.expiry_date BETWEEN ? AND ?
        ''' """

        query = '''
            SELECT items.id AS item_id, items.name, items.expiry_date, pictures.src AS image, items.category, items.notes, pictures.id AS picture_id
            FROM items
            JOIN pictures ON items.picture_id = pictures.id
            WHERE items.expiry_date BETWEEN ? AND ?
            ORDER BY items.expiry_date DESC
        '''

        cur.execute(query, (today, delta))
        items_list = [ItemModel(**dict(row)) for row in cur.fetchall()]
        items_list.sort(key=lambda x: x.expiry_date, reverse=True)
        # print(items_list)
        return Items(items=items_list)


if __name__ == "__main__":
    connection = sqlite3.connect("./database/food.db")
    # test_item = ItemModel(name="Pydantic", expiry_date=datetime.now(), image="test", category="test_tag", notes="Buy more"
    #                      )
    # insert_item(connection, test_item)
    # print(get_items(connection))
