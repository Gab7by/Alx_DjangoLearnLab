from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the change
book.title
# Expected Output:
'Nineteen Eighty-Four'

# Comment: Title successfully updated from “1984” to “Nineteen Eighty-Four.”


