import psycopg2
import mysql.connector
from bottle import route, run, get, static_file, template, view, debug
import os, json


@route('/')
@view('index')
def index():
    db_type = None
    db_version = ''
    uptime = ''
    conn_count = ''

    # Pick up environment variables for PostgreSQL or MySQL
    if os.environ.get('MYSQL_DATABASE'):
        db_type = 'MYSQL'
        database = os.environ.get('MYSQL_DATABASE')
        user = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASSWORD')
        host = os.environ.get('MYSQL_HOST')
        port = os.environ.get('MYSQL_PORT') or 3306
    else:
        db_type = 'POSTGRES'
        database = os.environ.get('POSTGRESQL_DATABASE')
        user = os.environ.get('POSTGRESQL_USER')
        password = os.environ.get('POSTGRESQL_PASSWORD')
        host = os.environ.get('POSTGRESQL_HOST')
        port = os.environ.get('POSTGRES_PORT') or 5432

    if db_type is 'POSTGRES':
        try:
            conn = psycopg2.connect(database=database, user=user, host=host, password=password)
            cur = conn.cursor()
            # Get PostgreSQL version
            cur.execute("""select version()""")
            rows = cur.fetchall()
            db_version = str(rows[0][0])
            cur.close()
            conn.close()
        except:
            print(os.environ.get('POSTGRES_HOST'))
        return dict(database=database, user=user, host=host, db_version=db_version, uptime=uptime, conn_count=conn_count)

    elif db_type is 'MYSQL':
        try:
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
            cur = conn.cursor()
            # Get MySQL version
            cur.execute("""SELECT VERSION()""")
            rows = cur.fetchall()
            db_version = str(rows[0][0])
            # Get MySQL uptime
            cur.execute("""SHOW STATUS LIKE 'Uptime'""")
            rows = cur.fetchall()
            uptime = str(rows[0][1])
            # Get MySQL connection count
            cur.execute("""SHOW STATUS LIKE 'Connections'""")
            rows = cur.fetchall()
            conn_count = str(rows[0][1])
            # Close MySQL cursor and connection
            cur.close()
            conn.close()
        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        else:
          conn.close()

        return dict(database=database, user=user, host=host, db_version=db_version, uptime=uptime, conn_count=conn_count)


# For Static files
@get("/static/css/<filename:re:.*\.css>")
def css(filename):
    return static_file(filename, root="static/css")


@get("/static/font/<filename:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filename):
    return static_file(filename, root="static/font")


@get("/static/img/<filename:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filename):
    return static_file(filename, root="static/img")


@get("/static/js/<filename:re:.*\.js>")
def js(filename):
    return static_file(filename, root="static/js")


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
