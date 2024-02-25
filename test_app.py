import os
import tempfile
import pytest
from flask import Flask
from main import getPrediction
from unittest.mock import patch
from io import BytesIO

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'static/image/'

    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert b'Welcome to the Image Upload and Prediction App' in response.data

def test_submit_file(client):
    # Assuming you have a test image in the 'tests' folder
    test_image_path = 'tests/your_test_image.jpg'
    
    with open(test_image_path, 'rb') as file:
        response = client.post('/', data={'file': (file, 'test_image.jpg')}, follow_redirects=True)

    assert b'Prediction Result' in response.data
    assert b'Image' in response.data
    assert b'Test Result' in response.data  # Adjust this based on your actual test result

def test_submit_file_no_file(client):
    response = client.post('/', follow_redirects=True)
    assert b'No file selected for uploading' in response.data

def test_submit_file_empty_file(client):
    # Test handling an empty file
    response = client.post('/', data={'file': (BytesIO(b''), 'empty.txt')}, follow_redirects=True)
    assert b'No file selected for uploading' in response.data

def test_submit_file_invalid_file_type(client):
    # Test handling an invalid file type
    response = client.post('/', data={'file': (BytesIO(b'Invalid content'), 'invalid.exe')}, follow_redirects=True)
    assert b'Invalid file type' in response.data

@patch('app.process_uploaded_file', side_effect=Exception('Simulated error'))
def test_submit_file_exception_handling(mocked_process_uploaded_file, client):
    # Simulate an exception during file processing
    response = client.post('/', data={'file': (BytesIO(b'Some content'), 'valid.jpg')}, follow_redirects=True)
    assert b'Error processing file' in response.data

def test_submit_file_large_file(client):
    # Test handling a large file
    # ...

def test_submit_file_small_file(client):
    # Test handling a small file
    # ...

def test_submit_file_no_file_flash_message(client):
    response = client.post('/', follow_redirects=True)
    assert b'No file selected for uploading' in response.data
    assert b'No file selected for uploading' in client.get('/').data  # Ensure flash message persists

def test_submit_file_response_contains_elements(client):
    response = client.post('/', data={'file': (BytesIO(b'Some content'), 'valid.jpg')}, follow_redirects=True)
    assert b'Prediction Result' in response.data
    assert b'Image' in response.data
    assert b'Test Result' in response.data  # Adjust this based on your actual test result

if __name__ == '__main__':
    pytest.main()
