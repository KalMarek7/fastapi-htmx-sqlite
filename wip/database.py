from models import ItemModel, Items, UploadItem, Images
import sqlite3
from sqlite3 import Connection
from datetime import timedelta, datetime


def get_items(connection: Connection) -> Items:
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT items.id AS item_id, items.name, items.expiry_date, items.created_date, pictures.src AS image, items.category, items.notes, pictures.id AS picture_id
            FROM items
            JOIN pictures ON items.picture_id = pictures.id;
            '''
        )
        items_list = [ItemModel(**dict(row)) for row in cur.fetchall()]
        items_list.sort(key=lambda x: x.expiry_date)
        # print(items_list)
        return Items(items=items_list)


def insert_item(connection: Connection, item: ItemModel):
    with connection:
        cur = connection.cursor()
        # print(item)
        cur.execute(
            '''
            INSERT INTO items(name, expiry_date, created_date, picture_id, category, notes)
            VALUES
            (:name, :expiry_date, :created_date, :picture_id, :category, :notes)
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


def get_image(connection: Connection, id: int) -> Images:
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT id, src, filename, filesize, initial
            FROM
            pictures
            WHERE id = :id
            ''',
            {'id': id}
        )
        image = UploadItem(**dict(cur.fetchone()))
        # It needs to be returned as a list to work with the rest of the app
        return Images(images=[image])


def update_image(connection: Connection, id: int):
    with connection:
        cur = connection.cursor()
        cur.execute(
            f'''
            UPDATE pictures
            SET initial = False
            WHERE id = :id;
            ''',
            {'id': id}
        )


def date_filtered_items(connection: Connection) -> Items:
    with connection:
        cur = connection.cursor()
        today = datetime.now().date()
        print(today)
        delta = today + timedelta(days=3)
        print(delta)

        query = '''
            SELECT items.id AS item_id, items.name, items.expiry_date, items.created_date, pictures.src AS image, items.category, items.notes, pictures.id AS picture_id
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


def search_items(connection: Connection, query: str) -> Items:
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT items.id AS item_id, items.name, items.expiry_date, items.created_date, pictures.src AS image, items.category, items.notes, pictures.id AS picture_id
            FROM items
            JOIN pictures ON items.picture_id = pictures.id
            WHERE items.name LIKE :query OR items.notes LIKE :query OR items.category LIKE :query
            ''',
            {'query': f'%{query}%'}
        )
        items_list = [ItemModel(**dict(row)) for row in cur.fetchall()]
        return Items(items=items_list)


def clear_table(connection: Connection, table: str):
    with connection:
        cur = connection.cursor()
        cur.execute(
            f'''
            DELETE FROM {table}
            '''
        )


def get_item(connection: Connection, id: int) -> Items:
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            SELECT items.id AS item_id, items.name, items.expiry_date, items.created_date, pictures.src AS image, items.category, items.notes, pictures.id AS picture_id
            FROM items
            JOIN pictures ON items.picture_id = pictures.id
            WHERE items.id = :id
            ''',
            {'id': id}
        )
        item = ItemModel(**dict(cur.fetchone()))
        # It needs to be returned as a list to work with the rest of the app
        return Items(items=[item])


def update_item(connection: Connection, id: int, name: str, expiry_date: str, category: str, notes: str):
    expiry_date_fmt = datetime.strptime(expiry_date, '%Y-%m-%d').date()
    existing_item = get_item(connection, id).model_dump()
    # print(existing_item)
    # If category or notes None then take the values from existing_item
    if category is None:
        category = existing_item["items"][0]["category"]
    if notes is None:
        notes = existing_item["items"][0]["notes"]
    updated_item = ItemModel(
        name=name,
        expiry_date=expiry_date_fmt,
        category=category,
        notes=notes,
        item_id=id,
        created_date=existing_item["items"][0]["created_date"],
        picture_id=existing_item["items"][0]["picture_id"]

    )
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            UPDATE items
            SET name = :name, expiry_date = :expiry_date, category = :category, notes = :notes
            WHERE id = :item_id
            ''',
            updated_item.model_dump()
        )


def delete_item(connection: Connection, id: int):
    with connection:
        cur = connection.cursor()
        cur.execute(
            f'''
            DELETE FROM items
            WHERE id = :id
            ''',
            {'id': id}
        )


""" if __name__ == "__main__":
    connection = sqlite3.connect("./database/food.db")
    # test_item = ItemModel(name="Pydantic", expiry_date=datetime.now(), image="test", category="test_tag", notes="Buy more"
    #                      )
    # insert_item(connection, test_item)
    # print(get_items(connection))
 """
