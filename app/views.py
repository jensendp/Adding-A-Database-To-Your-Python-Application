from app import app
from app.helpers import get_page_url_name, get_page_display_name
from app.page_repository import get_all_pages, create_page, get_page, update_page, delete_page_record
from flask import render_template, request, redirect, url_for, abort
import markdown
import os

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pages')
def pages():
    pages = get_all_pages()
    return render_template("pages.html", pages=pages)

@app.route('/pages/<page_name>')
def page(page_name):
    contents = get_page(page_name)
    if contents is None:
        abort(404)

    html = markdown.markdown(contents)
    return render_template('page.html', page_name=page_name, contents=html)

@app.route('/new_page', methods=['GET', 'POST'])
def new_page():
    if request.method == 'GET':
        return render_template('new_page.html')

    title = request.form['title']
    contents = request.form['contents']

    create_page(get_page_url_name(title), contents)
    # Save new page with provided title and contents (get_page_url_name(title) helper method)

    return redirect(url_for('pages'))

@app.route('/edit_page/<page_name>', methods=['GET', 'POST'])
def edit_page(page_name):
    if request.method == 'GET':
        contents = get_page(page_name)
        if contents is None:
            abort(404)

        title = get_page_display_name(page_name)

        return render_template('edit_page.html', page_name=title, contents=contents)

    title = request.form['title']
    contents = request.form['contents']

    update_page(get_page_url_name(title), contents)
    # Save updated page with provided contents (get_page_url_name(title) helper method)

    return redirect(url_for('page', page_name=get_page_url_name(title)))

@app.route('/delete_page/<page_name>', methods=['GET', 'POST'])
def delete_page(page_name):
    if request.method == 'GET':
        return render_template('delete_page.html')

    delete_page_record(page_name)
    # Delete information associated with the provided page_name

    return redirect(url_for('pages'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404