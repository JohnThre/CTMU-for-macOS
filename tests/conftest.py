"""Pytest configuration and fixtures"""

import pytest
from PIL import Image
from unittest.mock import Mock

@pytest.fixture
def sample_qr_image():
    """Sample QR code image for testing"""
    return Image.new('RGB', (200, 200), 'white')

@pytest.fixture
def sample_favicon():
    """Sample favicon image for testing"""
    return Image.new('RGBA', (32, 32), (255, 0, 0, 255))

@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests module"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'fake_image_data'
    mock_response.raise_for_status.return_value = None
    
    mock_get = Mock(return_value=mock_response)
    mock_head = Mock(return_value=mock_response)
    
    monkeypatch.setattr('requests.get', mock_get)
    monkeypatch.setattr('requests.head', mock_head)
    
    return mock_get, mock_head