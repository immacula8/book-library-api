import requests

# Your Render URL - NO extra /books here
API_URL = "https://book-library-api-bep0.onrender.com"

# Your 20 books
books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"title": "1984", "author": "George Orwell", "year": 1949},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813},
    {"title": "Moby Dick", "author": "Herman Melville", "year": 1851},
    {"title": "War and Peace", "author": "Leo Tolstoy", "year": 1869},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953},
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "year": 1847},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932},
    {"title": "The Odyssey", "author": "Homer", "year": -800},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "year": 1866},
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "year": 1890},
    {"title": "Wuthering Heights", "author": "Emily Brontë", "year": 1847},
    {"title": "The Alchemist", "author": "Paulo Coelho", "year": 1988},
    {"title": "Frankenstein", "author": "Mary Shelley", "year": 1818},
    {"title": "Dracula", "author": "Bram Stoker", "year": 1897},
    {"title": "The Chronicles of Narnia", "author": "C.S. Lewis", "year": 1950},
    {"title": "The Kite Runner", "author": "Khaled Hosseini", "year": 2003},
]

print(f"Adding {len(books)} books to {API_URL}...")
print("-" * 50)

success_count = 0
fail_count = 0

for book in books:
    # The correct endpoint is API_URL + /books
    url = f"{API_URL}/books"
    
    try:
        response = requests.post(url, json=book)
        if response.status_code == 200:
            success_count += 1
            print(f"✅ Added: {book['title']}")
        else:
            fail_count += 1
            print(f"❌ Failed: {book['title']} - Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        fail_count += 1
        print(f"❌ Error: {book['title']} - {e}")

print("-" * 50)
print(f"Complete! ✅ {success_count} added | ❌ {fail_count} failed")