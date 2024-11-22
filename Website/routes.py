from flask import Flask, render_template, request
import sqlite3
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__, static_folder='static')


def get_db_conn():
    """
    Подключение к базе данных через SQlite3
    :return:
    """
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    return cursor


@app.route('/')
def index():
    """
    Функция создания главной странице, в частности:
    - получение списка книг из базы данных
    - изменения списка, в котором каждая книга представлена в виде словаря атрибутов книги
    - создания пагинации
    :return: Возвращает функцию рендеринга HTML-шаблона
    """
    connect = get_db_conn()
    books = connect.execute('SELECT * FROM books')
    books_dicts = []
    for book in books:
        books_dicts.append(dict(
            zip(['id', 'title', 'genre', 'author', 'publisher', 'year', 'description', 'isbn', 'price', 'photo'],
                book)))
    books_num = len(books_dicts)
    connect.close()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 13
    offset = (page - 1) * per_page
    pagination_data = books_dicts[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=len(books_dicts),
                            css_framework='bootstrap4')
    return render_template('index.html',
                           books_num=books_num,
                           data=pagination_data,
                           pagination=pagination)


attr = ['id', 'title', 'genre', 'author', 'publisher', 'year', 'description', 'isbn', 'price', 'photo']


@app.route('/book_list')
def book_list():
    """
    Функция создания страницы, состоящая из списка книг, в частности:
    - получение списка книг из базы данных
    - изменения списка, в котором каждая книга представлена в виде словаря атрибутов книги
    - создания пагинации
    :return: Возвращает функцию рендеринга HTML-шаблона
    """
    connect = get_db_conn()
    books = connect.execute('SELECT * FROM books')
    books_dicts = []
    for book in books:
        books_dicts.append(dict(
            zip(attr, book)))
    connect.close()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 5
    offset = (page - 1) * per_page
    pagination_data = books_dicts[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=len(books_dicts),
                            css_framework='bootstrap4')
    return render_template('book_list.html',
                           data=pagination_data,
                           pagination=pagination)


@app.route('/book_list/<book_id>')
def book_detail(book_id):
    """
    Функция создания страницы с выбранной книгой, в частности:
    - получение списка атрибутов книги;
    - изменения списка в словарь атрибутов книги;
    :return: Возвращает функцию рендеринга HTML-шаблона
    """
    connect = get_db_conn()
    book_ = connect.execute('SELECT * FROM books WHERE id = ?', (int(book_id),))
    book = dict(zip(attr, list(book_)[0]))
    connect.close()
    return render_template('book_detail.html', book=book)
