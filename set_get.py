
def dict_to_constraints(dic):
    query = ""
    for _ in dic.keys():
        query += "("
        for _c in dic[_]:
            if type(_c) == str:
                query += "" + _ + "='" + _c + "' OR "
            else:
                query += "" + _ + "=" + str(_c) + " OR "
        query = query[:-4]
        query += ")"
        query += " AND "

    query = query[:-5]
    return query

def list_to_columns(list_of_columns):
    cols = ""
    for _ in list_of_columns:
        cols += _ + ", "
    cols = cols[:-2]
    return cols

def get_engine_and_conn():
    import psycopg2
    import pandas as pd
    from sqlalchemy import create_engine
    user, password, host, port, database = 'postgres', '4664', 'localhost', 5432, 'Labaratuar'

    try:
        # get the connection object (engine) for the database
        engine = create_engine(url="postgresql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
        print(f"Connection to the {host} for user {user} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
    
    return engine, engine.connect()

def delete_from_table(table_name, constraints):
    import psycopg2
    try:
        # Bağlantı kuruluyor
        conn = psycopg2.connect(host="localhost",
                                    database="Labaratuar",
                                    user="postgres",
                                    password="4664")
        cur = conn.cursor()

        # DELETE sorgusu oluşturuluyor
        query = f"DELETE FROM {table_name} WHERE {constraints}"

        # Sorgu çalıştırılıyor ve kayıtlar siliniyor
        cur.execute(query)
        conn.commit()

        # Bağlantı kapatılıyor
        cur.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while deleting records from PostgreSQL", error)

def get_table(table_name, column_names = "*", constraints={}):
    import pandas as pd
    query_c = ""
    if constraints != {}:
        query_c = dict_to_constraints(constraints)

    """
    tablo adı ve gerekli constraint'ler string şeklinde sağlanmalıdır:
    get_table("calisan")
    get_table("calisan", column_names="adi, soyadi" constraints="calisanadı='jack' AND maaş=6")
    get_table("virüs", column_names="ipliksayisi as İS", constraints="virüstipi='rna' AND ipliksayisi>200 OR genomsayisi<130 AND virüsadı!='vty-4'")
    """
    engine, conn = get_engine_and_conn()
    where = "" if query_c=="" else ' WHERE '
    column_names = "*" if column_names == "*" else list_to_columns(column_names)    
    table = pd.read_sql('SELECT ' + column_names + ' FROM ' + table_name + where + query_c, conn)
    return table


def update_table(table_name, constraints, values):
    import psycopg2
    conn = None
    try:
        # Veritabanına bağlanın
        conn = psycopg2.connect(host="localhost",
                                database="Labaratuar",
                                user="postgres",
                                password="4664")
        cursor = conn.cursor()

        # UPDATE sorgusu oluşturun
        query = f"UPDATE {table_name} SET {values} WHERE {constraints}"

        # Sorguyu çalıştırın ve değişiklikleri kaydedin
        cursor.execute(query)
        conn.commit()
        
        # Bağlantıyı kapatın
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



