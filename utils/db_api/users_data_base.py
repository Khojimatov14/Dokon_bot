import sqlite3


class DatabaseUsers:
    def __init__(self, path_to_db="allData.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
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
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            user_id INT UNIQUE,
            user_name TEXT,
            user_full_name TEXT NOT NULL,
            user_first_name TEXT(20),
            user_last_name TEXT(20),
            user_phone_number TEXT(20),
            user_registration_date TEXT,
            user_all_money_spent INT,
            user_registration TEXT,
            user_language TEXT,
            user_wallet INT,
            user_last_message_id TEXT,
            user_up_category TEXT,
            user_sub_category TEXT,
            user_last_page INT,
            user_sub_category_last_page INT
            user_last_state TEXT
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

    def add_user(self, user_id: int, user_name: str, user_full_name: str, user_first_name: str, user_last_name: str,
                 user_phone_number: str, user_registration_date: str, user_all_money_spent: int, user_registration: str,
                 user_language: str, user_wallet: int, user_last_message_id: str, user_up_category: str,
                 user_sub_category: str, user_last_page: int, user_sub_category_last_page: int, user_last_state: str):
        sql = """
        INSERT INTO Users(user_id, user_name, user_full_name, user_first_name, user_last_name, user_phone_number,
        user_registration_date, user_all_money_spent, user_registration, user_language, user_wallet, 
        user_last_message_id, user_up_category, user_sub_category, user_last_page, user_sub_category_last_page, user_last_state) 
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, user_name, user_full_name, user_first_name, user_last_name,
                                      user_phone_number, user_registration_date, user_all_money_spent,
                                      user_registration, user_language, user_wallet, user_last_message_id,
                                      user_up_category, user_sub_category, user_last_page,
                                      user_sub_category_last_page, user_last_state), commit=True)

    def update_user_info(self, user_id, **kwargs):
        sql = "UPDATE Users SET "
        sql, parameters = self.formatArgs(sql, kwargs)
        sql += " WHERE user_id = ?;"
        parameters += (user_id,)
        return self.execute(sql, parameters=parameters, commit=True)

    def select_user(self, user_id, **kwargs):
        sql = f"SELECT * FROM Users WHERE user_id = '{user_id}'"
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_users(self):
        sql = f"SELECT * FROM Users"
        return self.execute(sql, fetchall=True)


# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)

# ALTER TABLE Users ADD user_wallet INT DEFAULT 0
