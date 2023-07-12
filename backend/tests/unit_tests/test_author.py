import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import backend_app
from src.models.db.author import Author


class AuthorTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client for the FastAPI application
        self.test_client = TestClient(backend_app)

    @patch("src.repository.crud.author.AuthorCRUDRepository.read_authors")
    def test_get_authors(self, mock_read_authors):
        # Define the mocked data
        mocked_authors = [Author(id=1, name="Author 1"), Author(id=2, name="Author 2")]

        # Configure the mock to return the mocked data
        mock_read_authors.return_value = mocked_authors

        # Send a GET request to the read endpoint
        response = self.test_client.get("/api/authors")

        # Perform assertions on the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"id": 1, "name": "Author 1"}, {"id": 2, "name": "Author 2"}],
        )

    @patch("src.repository.crud.author.AuthorCRUDRepository.create_author")
    def test_create_author(self, mock_create_author):
        # Define the request payload
        payload = {"name": "John Doe"}

        # Configure the mock to return the created author
        created_author = Author(id=1, name="John Doe")
        mock_create_author.return_value = created_author

        # Send a POST request to the create endpoint
        response = self.test_client.post("/api/authors", json=payload)

        # Perform assertions on the response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "name": "John Doe"})

    @patch("src.repository.crud.author.AuthorCRUDRepository.read_author_by_id")
    def test_get_author_by_id(self, mock_read_author_by_id):
        # Define the mocked author ID
        author_id = 1

        # Configure the mock to return the author
        author = Author(id=author_id, name="John Doe")
        mock_read_author_by_id.return_value = author

        # Send a GET request to the read endpoint with the author ID
        response = self.test_client.get(f"/api/authors/{author_id}")

        # Perform assertions on the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "John Doe"})

    @patch("src.repository.crud.author.AuthorCRUDRepository.update_author_by_id")
    def test_update_author(self, mock_update_author):
        # Define the request payload
        payload = {"name": "Updated Name"}

        # Define the mocked author ID
        author_id = 1

        # Configure the mock to return the updated author
        updated_author = Author(id=author_id, name="Updated Name")
        mock_update_author.return_value = updated_author

        # Send a PATCH request to the update endpoint with the author ID
        response = self.test_client.patch(f"/api/authors/{author_id}", json=payload)

        # Perform assertions on the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "Updated Name"})

    @patch("src.repository.crud.author.AuthorCRUDRepository.delete_author_by_id")
    def test_delete_author(self, mock_delete_author):
        # Define the mocked author ID
        author_id = 1

        # Configure the mock to return a success message
        success_message = f"Author with id '{author_id}' is successfully deleted!"
        mock_delete_author.return_value = success_message

        # Send a DELETE request to the delete endpoint with the author ID
        response = self.test_client.delete(f"/api/authors/{author_id}")

        # Perform assertions on the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"notification": success_message})


if __name__ == "__main__":
    unittest.main()
