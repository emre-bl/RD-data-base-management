def list_tables():
    import psycopg2
    # Veritabanına bağlanmak için psycopg2 kütüphanesini kullanıyoruz
    conn = psycopg2.connect(host="localhost",
                                database="Labaratuar",
                                user="postgres",
                                password="4664")
    cur = conn.cursor()

    # Veritabanında bulunan tüm tabloları listeleyen SQL sorgusunu çalıştırıyoruz
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

    # Sorgunun sonucunu liste olarak alıyoruz
    tables = [table[0] for table in cur.fetchall() if len(table[0]) > 0]

    # İşlemler bittikten sonra veritabanı bağlantısını kapatıyoruz
    cur.close()
    conn.close()

    return tables


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

def dict_to_values(dic):
    values = ""
    for _ in dic.keys():
        values += _ + " = "
        if type(dic[_]) == str:
            values += "'" + dic[_] + "', "
        else:
            values += str(dic[_]) + ", "
    print("values: ", values)
    return values[:-2]

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
        constraints = dict_to_constraints(constraints)
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

        constraints = dict_to_constraints(constraints)
        values = dict_to_values(values)

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

def run_sql(file):
    from io import StringIO
    import psycopg2

    if file is not None:
        conn = psycopg2.connect(host="localhost",
                                database="Labaratuar",                        
                                user="postgres",
                                password="4664")
        cur = conn.cursor()
                        
                        
        stringio = StringIO(file.getvalue().decode("utf-8"))
        string_query = stringio.read()


        # Dosyadaki sorguları ayrıştır
        sql_commands = string_query.split(';')
        print("sql commands",sql_commands)
        # Sorguları tek tek çalıştır
        for command in sql_commands:
            if command != "\n":
                print("COMMAND ", command)
                cur.execute(command + ";")
        conn.commit()