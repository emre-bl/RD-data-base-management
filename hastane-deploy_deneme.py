# %% [markdown]
# https://github.com/emre-bl/RD-data-base-management/blob/main/sql_connection.ipynb
# %%
import streamlit as st
import hashlib


#def get_table(table_name, column_names="*", col_constraint_dict={}):
from set_get import get_engine_and_conn, delete_from_table, get_table, update_table, run_sql, list_tables

database_tables = list_tables()

def greet_user(calisanlar, user_ssn):
    user = calisanlar[calisanlar["ssn"] == user_ssn][["ad", "soyad", "ekipadı"]]
    ekipler = get_table("ekip")

    if user_ssn in list(ekipler["yöneticissn"]):
        st.sidebar.write("Welcome,", user["ad"].iloc[0], user["soyad"].iloc[0] , "(menager of", ekipler[ekipler["yöneticissn"] == user_ssn]["ekipadı"].iloc[0],")")  
        st.sidebar.write("Your team are working on", ekipler[ekipler["yöneticissn"] == user_ssn]["virüsadı"].iloc[0], "virus.")
        st.sidebar.write("Your team are working in build: ", ekipler["binano"].iloc[0], "in lab:", ekipler["labno"].iloc[0])
        
        # ekip başkanı ekibini kontrol ediyor
        if st.button('check my team', on_click=None):
            ekip_calisanları = calisanlar[calisanlar["ekipadı"] == ekipler[ekipler["yöneticissn"] == user_ssn]["ekipadı"].iloc[0]]
            st.table(ekip_calisanları[["ad","soyad","yaş","cinsiyet","calisantipi"]])
            if st.button('go back', on_click=None):
                pass        
        else:
            pass
    else:
        st.sidebar.write("Welcome,", user["ad"].iloc[0], user["soyad"].iloc[0],  "(employee at", user["ekipadı"].iloc[0] ,")")
        st.sidebar.write("Your team are working on", ekipler[ekipler["ekipadı"] == user["ekipadı"].iloc[0]]["virüsadı"].iloc[0], "virus.")
        st.sidebar.write("Your team are working in build: ", ekipler["binano"].iloc[0], "in lab:", ekipler["labno"].iloc[0])
        

def select_table():
    global database_tables
    table_name = st.selectbox(" ", database_tables)
    return table_name

def select_columns(table_name):
    if table_name != "Select a table":
        table = get_table(table_name)
        table_columns = list(table.columns)

        if table_name == "calisan":
            table_columns.remove("ssn")
            table_columns.remove("maas")

        st.write("## Select Columns")
        column_names = st.multiselect("Requested columns", options=table_columns, key=str)
        if column_names == []:
            column_names = table_columns
        else:
            column_names = (",".join(column_names)).split(",")
    return table, column_names

def select_columns_mudur(table_name):
    if table_name != "Select a table":
        table = get_table(table_name)
        table_columns = list(table.columns)

        st.write("## Select Columns")
        column_names = st.multiselect("Requested columns", options=table_columns, key=str)
        if column_names == []:
            column_names = table_columns
        else:
            column_names = (",".join(column_names)).split(",")
    return table, column_names

def select_constraints(table, column_names):
    #constraints = st.text_input("constraints(if there is any):")
    #st.write(constraints)

    st.write("## Selected Columns Constraints")
    col_constraint_dict = {}
    if len(table) != 0:# and len(constraints) != "":
        for col in column_names:
            if type(table[col][0]) == str:
                col_constraint_dict[col] = st.multiselect(col, options=list(table[col].unique()),)
                if len(col_constraint_dict[col]) == 0:
                    col_constraint_dict[col] = list(table[col].unique())
            else:
                start_cons, end_cons = st.select_slider(label=col, options=list(range(table[col].min(),table[col].max()+1)), value=(table[col].min(),table[col].max()))
                col_constraint_dict[col] = list(range(start_cons, end_cons + 1))
    return col_constraint_dict







st.write("# Simple Hospital virus research web service")


# taking input
def run():
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    st.sidebar.image("logo.png", width=250,use_column_width=True)
    st.sidebar.write("# Login")
    user_ssn = st.sidebar.text_input("User ssn")
    user_pass = st.sidebar.text_input("User password")
    if user_ssn == "" or user_pass == "":
        st.sidebar.write("Please log in with your ssn and password.")
    else:
        calisanlar = get_table("calisan")
        ssn_list = list(calisanlar["ssn"])

        if user_ssn == "hastane müdürü":
            if user_pass == "123456":
                database_tables = list_tables()
                import psycopg2
                import pandas as pd
                st.sidebar.write("Welcome, hospital manager")
                müdür = ["run .sql file", "table setter","table show","table deleter"]
                option = st.selectbox("Select an option", müdür)

                if option == "table show":
                    st.write("# -Select Table")
                    table_name = select_table()
                    table, column_names = select_columns_mudur(table_name)
                    col_constraint_dict = select_constraints(table, column_names)
                    data = get_table(table_name, column_names, col_constraint_dict)
                    st.write("#", table_name)
                    st.table(data)

                elif option == "run .sql file":
                    uploaded_file = st.file_uploader("Upload new tables .sql file", type=["sql"])
                    if st.button('run .sql file', on_click=None):
                        run_sql(uploaded_file)
                        # bruada tabloyu sil       
                    else:
                        pass


                elif option == "table setter":

                    st.write("# -Update Table")
                    table_name = select_table()
                    table, column_names = select_columns_mudur(table_name)
                    col_constraint_dict = select_constraints(table, column_names)

                    st.write("## Selected New Columns Values")
                    new_col_values = {}
                    dFrame = {}
                    
                    #burayı düzelt. constraints aldıktan sonra değiştirilcek columnları seç
                    for col in column_names:
                        new_value = st.text_input("**New value for**", col)
                        new_col_values[col] = new_value
                        dFrame[col] = [new_value]

                    st.write("# Old ", table_name)
                    data = get_table(table_name, constraints = col_constraint_dict)
                    st.table(data)
                    st.write("# New ", table_name)
                    new_table = pd.DataFrame(dFrame)   
                    st.table(new_table)

                    

                    if st.button('update table'):
                        update_table(table_name, col_constraint_dict, new_col_values)
                        # bruada tabloyu sil      
                    else:
                        pass
                #table deleterı düzelt
                elif option == "table deleter":

                    st.write("# -Delete Table")
                    table_name = select_table()
                    
                    if table_name != "Select a table":
                        table = get_table(table_name)
                        column_names = list(table.columns)
                    col_constraint_dict = select_constraints(table, column_names)

                    data = get_table(table_name, column_names, col_constraint_dict)
                    st.write("#", table_name)
                    st.write(data)

                    if st.button('delete table', on_click=None):
                        delete_from_table(table_name, col_constraint_dict)
                        
                        # bruada tabloyu sil       
                    else:
                        pass
                    
                database_tables = list_tables()

            else:
                st.sidebar.write("Non-granted login")
    
    
        elif user_ssn not in ssn_list:
            st.sidebar.write("Non-granted login")


        elif user_ssn in ssn_list and user_pass == hashlib.md5(user_ssn.encode('utf8')).hexdigest():
            greet_user(calisanlar, user_ssn)
            table_name = select_table()
            table, column_names = select_columns(table_name)
            col_constraint_dict = select_constraints(table, column_names)

            data = get_table(table_name, column_names, col_constraint_dict)
            st.write("#", table_name)
            st.write(data)




try:
    run()
except Exception as e:
    print(e)
# %%
