import psycopg2
from psycopg2.extras import DictCursor

from config import setting

db = psycopg2.connect(
    dbname = setting.DB_NAME,
    user = setting.DB_USER,
    password = setting.DB_PASSWORD,
    host = setting.DB_HOST,
    port = setting.DB_PORT
)

class QueryUsers:
    def __init__(self):
        self.result = None
        self.description = None
        self.list_params = []
        self.values = []

    def filter_dict(self, incoming_dict: dict):
        print(f"This is incoming dict: {incoming_dict}")
        filter_methods = {
            "id": self.filter_by_id,
            "name": self.filter_by_name,
            "email": self.filter_by_email
        }
        for key, value in incoming_dict.items():
            if key in filter_methods:
                filter_methods[key](value)
        return self

    def filter_by_id(self, user_id):
        if user_id is not None:
            self.list_params.append("id = %s")
            self.values.append(user_id)
            return self

    def filter_by_name(self, user_name):
        if user_name is not None:
            self.list_params.append("name = %s")
            self.values.append(user_name)
            return self

    def filter_by_email(self, user_email):
        if user_email is not None:
            self.list_params.append("email = %s")
            self.values.append(user_email)
            return self

    def constructor_query(self):
        if self.list_params:
            part_of_query = "SELECT * FROM postgres.public.user WHERE " + " AND ".join(self.list_params)
        else: part_of_query = "SELECT * FROM postgres.public.user"

        with (db.cursor(cursor_factory=DictCursor) as cursor):
            cursor.execute(part_of_query,self.values)
            column_descript = [col.name for col in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(column_descript, row)) for row in rows]
            return result

    def reset_query(self):
        self.list_params = []
        self.values = []
        return self


