from bookshelf.models import Book

# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
Book.objects.all()
# Expected Output:


(1, {'bookshelf.Book': 1})
<QuerySet []>
Comment: The book instance was successfully deleted; no books remain in the database.
