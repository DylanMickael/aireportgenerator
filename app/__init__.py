from flask import Flask
import jaydebeapi
import configparser
import cohere
import os

config = configparser.ConfigParser()
config.read('config.ini')

def get_db_connection():
    h2_jar_path = os.path.join(os.getcwd(), 'lib', 'h2-2.2.224.jar')
    db_url = config['DATABASE']['url']
    db_user = config['DATABASE']['user']
    db_password = config['DATABASE']['password']
    
    conn = jaydebeapi.connect(
        'org.h2.Driver',
        db_url,
        [db_user, db_password],
        h2_jar_path
    )
    
    return conn

def get_db_schema():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    schema = {}

    for table in tables:
        table_name = table[0]
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table_name}'
        """)
        columns = cursor.fetchall()
        
        column_definitions = []
        for column in columns:
            column_name = column[0]
            column_type = column[1]
            column_definitions.append(f"{column_name} {column_type}")
        
        schema[table_name] = ", ".join(column_definitions)

    cursor.close()
    conn.close()

    return schema

def get_api_connection():
    api_key = config['API']['cohere_api_key']
    conn = cohere.ClientV2(api_key)
    return conn

def create_app():
    from app.routes import api as routes_api
    app = Flask(__name__)
    app.register_blueprint(routes_api)

    return app
