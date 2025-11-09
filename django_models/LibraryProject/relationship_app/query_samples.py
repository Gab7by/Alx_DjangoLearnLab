import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Sample data creation
author = Author.objects.create(name="Gabriel Garcia Marquez")
book1 = Book.objects.create(title="One Hundred Years of Solitude", author=author)
book2 = Book.objects.create(title="Love in the Time of Cholera", author=author)

library = Library.objects.create(name="Central City Library")
library.books.add(book1, book2)

librarian = Librarian.objects.create(name="Mary Johnson", library=library)

# --- Queries ---

# 1️⃣ Query all books by a specific author
author_books = Book.objects.filter(author__name="Gabriel Garcia Marquez")
print("Books by Gabriel Garcia Marquez:")
for book in author_books:
    print("-", book.title)

# 2️⃣ List all books in a library
library_books = library.books.all()
print(f"\nBooks in {library.name}:")
for book in library_books:
    print("-", book.title)

# 3️⃣ Retrieve the librarian for a library
library_librarian = library.librarian
print(f"\nLibrarian of {library.name}: {library_librarian.name}")