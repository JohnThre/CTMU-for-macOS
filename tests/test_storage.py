"""Tests for storage utilities"""

import pytest
from unittest.mock import Mock, patch, mock_open
from ctmu.storage import (
    s3_upload, s3_download, s3_list, s3_delete,
    nextcloud_upload, nextcloud_download, nextcloud_list, 
    nextcloud_delete, nextcloud_mkdir
)

class TestS3Functions:
    
    @patch('ctmu.storage.boto3')
    def test_s3_upload_success(self, mock_boto3):
        mock_s3 = Mock()
        mock_boto3.Session.return_value.client.return_value = mock_s3
        
        result = s3_upload('test.txt', 'bucket', 'key')
        
        mock_s3.upload_file.assert_called_once_with('test.txt', 'bucket', 'key')
        assert "Uploaded test.txt to s3://bucket/key" in result
    
    @patch('ctmu.storage.boto3')
    def test_s3_download_success(self, mock_boto3):
        mock_s3 = Mock()
        mock_boto3.Session.return_value.client.return_value = mock_s3
        
        result = s3_download('bucket', 'key', 'local.txt')
        
        mock_s3.download_file.assert_called_once_with('bucket', 'key', 'local.txt')
        assert "Downloaded s3://bucket/key to local.txt" in result
    
    @patch('ctmu.storage.boto3')
    def test_s3_list_success(self, mock_boto3):
        mock_s3 = Mock()
        mock_response = {
            'Contents': [
                {'Key': 'file1.txt', 'Size': 100, 'LastModified': Mock()},
                {'Key': 'file2.txt', 'Size': 200, 'LastModified': Mock()}
            ]
        }
        mock_s3.list_objects_v2.return_value = mock_response
        mock_boto3.Session.return_value.client.return_value = mock_s3
        
        result = s3_list('bucket')
        
        assert len(result) == 2
        assert result[0]['Key'] == 'file1.txt'
    
    def test_s3_upload_no_boto3(self):
        with patch('ctmu.storage.boto3', side_effect=ImportError):
            result = s3_upload('test.txt', 'bucket')
            assert "boto3 not installed" in result

class TestNextcloudFunctions:
    
    @patch('ctmu.storage.Client')
    @patch('builtins.open', mock_open(read_data=b'test data'))
    def test_nextcloud_upload_success(self, mock_client):
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        result = nextcloud_upload('test.txt', '/remote/test.txt', 'url', 'user', 'pass')
        
        mock_client_instance.upload_fileobj.assert_called_once()
        assert "Uploaded test.txt to /remote/test.txt" in result
    
    @patch('ctmu.storage.Client')
    @patch('builtins.open', mock_open())
    def test_nextcloud_download_success(self, mock_client):
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        result = nextcloud_download('/remote/test.txt', 'local.txt', 'url', 'user', 'pass')
        
        mock_client_instance.download_fileobj.assert_called_once()
        assert "Downloaded /remote/test.txt to local.txt" in result
    
    @patch('ctmu.storage.Client')
    def test_nextcloud_list_success(self, mock_client):
        mock_client_instance = Mock()
        mock_item1 = Mock()
        mock_item1.name = 'file1.txt'
        mock_item1.is_dir = False
        mock_item1.content_length = 100
        
        mock_item2 = Mock()
        mock_item2.name = 'folder1'
        mock_item2.is_dir = True
        
        mock_client_instance.ls.return_value = [mock_item1, mock_item2]
        mock_client.return_value = mock_client_instance
        
        result = nextcloud_list('/remote/', 'url', 'user', 'pass')
        
        assert len(result) == 2
        assert result[0]['Name'] == 'file1.txt'
        assert result[0]['Type'] == 'File'
        assert result[1]['Type'] == 'Directory'
    
    def test_nextcloud_upload_no_webdav4(self):
        with patch('ctmu.storage.Client', side_effect=ImportError):
            result = nextcloud_upload('test.txt', '/remote/', 'url', 'user', 'pass')
            assert "webdav4 not installed" in result