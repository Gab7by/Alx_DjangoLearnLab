import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# --- Sample Data Creation ---
author = Author.objects.create(name="Gabriel Garcia Marquez")
book1 = Book.objects.create(title="One Hundred Years of Solitude", author=author)
book2 = Book.objects.create(title="Love in the Time of Cholera", author=author)

library = Library.objects.create(name="Central City Library")
library.books.add(book1, book2)

librarian = Librarian.objects.create(name="Mary Johnson", library=library)

# --- Queries ---

# 1️⃣ Retrieve author instance
author_instance = Author.objects.get(name="Gabriel Garcia Marquez")
print(f"Author retrieved: {author_instance.name}")

# 2️⃣ Query all books by the author using the author instance
books_by_author = Book.objects.filter(author=author_instance)  # <--- Correct usage
print(f"\nBooks by {author_instance.name}:")
for book in books_by_author:
    print("-", book.title)

# 3️⃣ List all books in a library
library_instance = Library.objects.get(name="Central City Library")
library_books = library_instance.books.all()
print(f"\nBooks in {library_instance.name}:")
for book in library_books:
    print("-", book.title)

# 4️⃣ Retrieve the librarian for a library
library_librarian = library_instance.librarian
print(f"\nLibrarian of {library_instance.name}: {library_librarian.name}")