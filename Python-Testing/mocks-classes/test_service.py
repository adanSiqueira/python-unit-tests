import pytest
from service import UserService, APIClient

def test_get_username(mocker):
    # Arrange
    mock_api_client = mocker.Mock(spec=APIClient) #Create a mock of APIClient
    user_service = UserService(mock_api_client) # Inject the mock into UserService

    mock_api_client.get_user_data.return_value = {'id': 1, 'name': 'John Doe'}

    # Act
    username = user_service.get_username(1) #Call the method under test that depends on the mock

    # Assert
    assert username == 'JOHN DOE'
    mock_api_client.get_user_data.assert_called_once_with(1)