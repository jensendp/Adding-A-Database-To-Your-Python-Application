import sqlite3

sqlite_file = 'wiki.sqlite'
table_name = 'page'
title_field = 'title'
title_field_type = 'TEXT'
content_field = 'content'
content_field_type = 'TEXT'

def ensure_page_table_exists():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '%s';" % table_name)

    data = c.fetchone()

    if data is None:
        c.execute("CREATE TABLE {tn} ({fc} {fct} PRIMARY KEY, {sc} {sct})".format(tn=table_name, fc=title_field, fct=title_field_type, sc=content_field, sct=content_field_type))
        conn.commit()
    
    conn.close()

def get_all_pages():
    ensure_page_table_exists()

    pages = []
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT title FROM page")

    pages = c.fetchall()

    conn.close()

    return [page[0] for page in pages]

def create_page(title, content):
    ensure_page_table_exists()

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("INSERT INTO page (title, content) VALUES ('%s', '%s')" % (title, content))
    conn.commit()

    c.close()

def get_page(page_name):
    ensure_page_table_exists()

    content = None
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT content FROM page WHERE title = '%s'" % page_name)

    content = c.fetchone()
    conn.close()

    if content is None:
        return content

    return content[0]

def update_page(title, content):
    ensure_page_table_exists()

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("UPDATE page SET content = '%s' WHERE title = '%s'" % (content, title))

    conn.commit()

    c.close()

def delete_page_record(title):
    ensure_page_table_exists()

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("DELETE FROM page WHERE title = '%s'" % title)

    conn.commit()

    c.close()
