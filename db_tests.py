import psycopg2
import db_params

db = psycopg2.connect(
    dbname = db_params.dbname,
    user = db_params.user,
    password = db_params.password,
    host = db_params.host,
    port = db_params.port
)

def db_query(param_1 = None, param_2 = None, param_3 = None):
    cursor = db.cursor()
    list_params = []
    values = []
    if param_1 is not None:
        list_params.append("id = %s")
        values.append(param_1)
    if param_2 is not None:
        list_params.append("name = %s")
        values.append(param_2)
    if param_3 is not None:
        list_params.append("email = %s")
        values.append(param_3)

    if list_params:
        part_of_query = "SELECT * FROM postgres.public.user WHERE " + " AND ".join(list_params)
    else: part_of_query = "SELECT * FROM postgres.public.user"
    cursor.execute(part_of_query,values)
    print(cursor.fetchall())
    db.close()



db_query(9,None, None)

