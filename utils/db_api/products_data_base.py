import sqlite3


class DatabaseProducts:
    def __init__(self, path_to_db="allData.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        try:
            with sqlite3.connect(self.path_to_db) as connection:
                # connection.set_trace_callback(logger)
                cursor = connection.cursor()
                data = None
                cursor.execute(sql, parameters)
                if commit:
                    connection.commit()
                if fetchall:
                    data = cursor.fetchall()
                if fetchone:
                    data = cursor.fetchone()
        except sqlite3.OperationalError:
            with sqlite3.connect("/Users/khojimatov14/Documents/Documents/Botlar/Shop_bot/data/allData.db") as connection:
                # connection.set_trace_callback(logger)
                cursor = connection.cursor()
                data = None
                cursor.execute(sql, parameters)
                if commit:
                    connection.commit()
                if fetchall:
                    data = cursor.fetchall()
                if fetchone:
                    data = cursor.fetchone()
        return data

    def create_table_products(self):
        sql = """
        CREATE TABLE Products (
            product_id INTEGER NOT NULL UNIQUE,
            up_category TEXT,
            sub_category TEXT,
            product_name_uz TEXT,
            product_name_ru TEXT,
            product_name_en TEXT,
            price INT,
            product_photos TEXT,
            description_uz TEXT,
            description_ru TEXT,
            description_en TEXT,
            brand_name TEXT,
            PRIMARY KEY(product_id AUTOINCREMENT)
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def formatArgs(sql, parameters: dict):
        if len(parameters) == 1:
            bat = " AND "
        else:
            bat = ", "
        sql += bat.join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_product(self, up_category: str, sub_category: str, product_name_uz: str, product_name_ru: str,
                    product_name_en: str, price: int, product_photos: str, description_uz: str, description_ru: str,
                    description_en: str, brand_name: str):
        sql = """
        INSERT INTO Products(up_category, sub_category, product_name_uz, product_name_ru, product_name_en, price,
         product_photos, description_uz, description_ru, description_en, brand_name) 
         VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(up_category, sub_category, product_name_uz, product_name_ru, product_name_en,
                                      price, product_photos, description_uz, description_ru, description_en, brand_name),
                     commit=True)

    def select_product(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_last_product(self, **kwargs):
        sql = "SELECT * FROM Products ORDER BY product_id DESC LIMIT 1"
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_products(self):
        sql = f"SELECT * FROM Products"
        return self.execute(sql, fetchall=True)

    def select_products(self, up_category, sub_category):
        sql = f"SELECT * FROM Products WHERE up_category = '{up_category}' AND sub_category = '{sub_category}'"
        return self.execute(sql, fetchall=True)

    def select_all_products_one_category(self, up_category):
        sql = f"SELECT * FROM Products WHERE up_category = '{up_category}'"
        return self.execute(sql, fetchall=True)

    def update_product_info(self, product_id, **kwargs):
        sql = "UPDATE Products SET "
        sql, parameters = self.formatArgs(sql, kwargs)
        sql += " WHERE product_id = ?;"
        parameters += (product_id,)
        return self.execute(sql, parameters=parameters, commit=True)

    def search_products(self, product_name):
        words = product_name.split()
        conditions = [f"product_name LIKE '%{word}%'" for word in words]
        sql = f"SELECT * FROM Products WHERE {' OR '.join(conditions)}"
        return self.execute(sql, fetchall=True)

    def delete_product(self, product_id):
        self.execute(sql=f"DELETE FROM Products WHERE product_id = '{product_id}'", commit=True)


# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)
