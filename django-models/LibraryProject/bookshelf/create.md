from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949,
    isbn="1234567890123",
    available=True
)

book 

# Expected output 
<Book: 1984>

# Comment: A Book instance titled “1984” by George Orwell was successfully created