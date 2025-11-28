from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create user for authentication tests
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # API client for authenticated user
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        # Create sample books
        self.book1 = Book.objects.create(
            title="Python Crash Course",
            author="Eric Matthes",
            publication_year=2016
        )
        self.book2 = Book.objects.create(
            title="Django for Beginners",
            author="William S. Vincent",
            publication_year=2018
        )
        self.list_url = reverse("book-list")      # /books/
        self.detail_url = reverse("book-detail", args=[self.book1.id])  # /books/<id>/

    # ----------------------------------------------------------------------
    # LIST VIEW TESTS
    # ----------------------------------------------------------------------

    def test_get_books_list(self):
        """Test retrieving all books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books(self):
        """Test searching by title"""
        response = self.client.get(self.list_url, {"search": "Python"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books(self):
        """Test filtering by publication_year"""
        response = self.client.get(self.list_url, {"publication_year": 2018})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        """Test ordering by title"""
        response = self.client.get(self.list_url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["Django for Beginners", "Python Crash Course"])

    # ----------------------------------------------------------------------
    # DETAIL VIEW TESTS
    # ----------------------------------------------------------------------

    def test_get_single_book(self):
        """Test retrieving a single book by ID"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # ----------------------------------------------------------------------
    # CREATE VIEW TESTS (requires authentication)
    # ----------------------------------------------------------------------

    def test_create_book_authenticated(self):
        """Authenticated user should be able to create a book"""
        data = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "publication_year": 2008
        }
        response = self.client_auth.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Unauthenticated user cannot create a book"""
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_year": 2020
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------------------------------------------------------------
    # UPDATE VIEW TESTS
    # ----------------------------------------------------------------------

    def test_update_book_authenticated(self):
        """Authenticated users can update a book"""
        data = {"title": "Updated Title"}
        response = self.client_auth.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_unauthenticated(self):
        """Unauthenticated users cannot update a book"""
        data = {"title": "Hacker Update"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------------------------------------------------------------
    # DELETE VIEW TESTS
    # ----------------------------------------------------------------------

    def test_delete_book_authenticated(self):
        """Authenticated users can delete a book"""
        response = self.client_auth.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_unauthenticated(self):
        """Unauthenticated users cannot delete books"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


