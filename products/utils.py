import requests
from urllib.parse import quote

def search_wikimedia_cover(book_title, author_name=None):
    """Поиск обложки книги на Wikimedia Commons"""
    search_query = f"{book_title} {author_name} book cover" if author_name else f"{book_title} book cover"
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': search_query,
        'srnamespace': 6,
        'srlimit': 5
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        if 'query' in data and 'search' in data['query']:
            for result in data['query']['search']:
                title = result['title']
                file_url = get_wikimedia_file_url(title)
                if file_url:
                    return file_url
    except Exception:
        pass
    return None

def get_wikimedia_file_url(file_title):
    """Получает прямую ссылку на файл из Wikimedia Commons"""
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'titles': file_title,
        'prop': 'imageinfo',
        'iiprop': 'url',
        'iiurlwidth': 300
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        pages = data['query']['pages']
        for page_id, page_data in pages.items():
            if 'imageinfo' in page_data:
                return page_data['imageinfo'][0]['thumburl']
    except Exception:
        pass
    return None

def get_openlibrary_cover(isbn):
    """Получает обложку с OpenLibrary по ISBN"""
    clean_isbn = isbn.replace('-', '').replace(' ', '')
    return f"https://covers.openlibrary.org/b/isbn/{clean_isbn}-L.jpg"

def update_book_covers():
    """Обновляет обложки для всех книг в базе данных"""
    from .models import Book
    for book in Book.objects.all():
        if not book.cover_url:
            openlibrary_url = get_openlibrary_cover(book.isbn)
            book.cover_url = openlibrary_url
            wikimedia_url = search_wikimedia_cover(book.title)
            if wikimedia_url:
                book.cover_url = wikimedia_url
            book.save()
            print(f"Обновлена книга: {book.title}")
