import os
import tempfile
import pytest
from flask import Flask
from main import getPrediction

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

# Add more test cases as needed

if __name__ == '__main__':
    pytest.main()
