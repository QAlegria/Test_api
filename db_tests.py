import psycopg2
from psycopg2.extras import DictCursor

import db_params

db = psycopg2.connect(
    dbname = db_params.dbname,
    user = db_params.user,
    password = db_params.password,
    host = db_params.host,
    port = db_params.port
)

class QueryUsers:
    def __init__(self):
        self.list_params = []
        self.values = []

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

        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(part_of_query,self.values)
            return cursor.fetchall()

query = QueryUsers()
result = (query.filter_by_name('1')
          .filter_by_email('test@test.test')
          .constructor_query())
