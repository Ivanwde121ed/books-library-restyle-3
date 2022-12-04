import json
from livereload import Server

from jinja2 import Environment, FileSystemLoader, select_autoescape

BOOKS_FILENAME = 'books.json'
def fetch_books_from_json(filename) -> list[dict]:
    with open(filename, 'r', encoding='utf-8') as file:
        books = json.loads(file.read())

    for book in books:
        book['image_src'] = book['image_src'].replace('\\', '/')
        book['book_path'] = book['book_path'].replace('\\', '/')

    return books

def on_reload():

    books = fetch_books_from_json(BOOKS_FILENAME)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)



if __name__ == '__main__':

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

