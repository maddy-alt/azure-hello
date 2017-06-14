import psycopg2
from bottle import route, run, get, static_file, template, view, debug
import os, json


@route('/')
@view('index')
def index():
    database = os.environ.get('POSTGRESQL_DB')
    user = os.environ.get('POSTGRESQL_USER')
    password = os.environ.get('POSTGRESQL_PASSWORD')
    host = os.environ.get('POSTGRESQL_HOST')
    # port=os.environ.get('POSTGRES_PORT') | 5432
    db_version = ''

    try:
        conn = psycopg2.connect(database=database, user=user, host=host, password=password)
        cur = conn.cursor()
        cur.execute("""select version()""")

        rows = cur.fetchall()
        db_version = str(rows[0][0])
        cur.close()
        conn.close()
    except:
        print(os.environ.get('POSTGRES_HOST'))

    return dict(database=database, user=user, host=host, db_version=db_version)


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
    run(host='0.0.0.0', port=80, debug=True, reloader=True)
