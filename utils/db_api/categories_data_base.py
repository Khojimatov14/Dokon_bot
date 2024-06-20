import sqlite3


class DatabaseCategories:
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

    def create_table_categories(self):
        sql = """
        CREATE TABLE Categories (
            category_id INTEGER NOT NULL UNIQUE,
            up_category TEXT,
            sub_category TEXT,
            category_name_uz TEXT,
            category_name_ru TEXT,
            PRIMARY KEY(category_id AUTOINCREMENT)
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

    def add_category(self,up_category: str, sub_category: str, category_name_uz: str, category_name_ru: str):
        sql = """
        INSERT INTO Categories(up_category, sub_category, category_name_uz, category_name_ru) 
        VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(up_category, sub_category, category_name_uz, category_name_ru), commit=True)

    def update_category_info(self, category_id, **kwargs):
        sql = "UPDATE Categories SET "
        sql, parameters = self.formatArgs(sql, kwargs)
        sql += " WHERE category_id = ?;"
        parameters += (category_id,)
        return self.execute(sql, parameters=parameters, commit=True)

    def select_category(self, **kwargs):
        sql = "SELECT * FROM Categories WHERE "
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_up_categories(self, **kwargs):
        sql = f"SELECT * FROM Categories WHERE up_category = 'True'"
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_sub_categories(self, up_category: str):
        sql = f"SELECT * FROM Categories WHERE up_category = '{up_category}'"
        return self.execute(sql, fetchall=True)

    def select_all_categories(self):
        sql = f"SELECT * FROM Categories"
        return self.execute(sql, fetchall=True)


# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)

# ALTER TABLE Users ADD user_wallet INT DEFAULT 0
