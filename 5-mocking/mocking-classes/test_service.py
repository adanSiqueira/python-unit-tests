from service import UserService, APIClient

def test_get_username(mocker):
    """Test UserService.get_username with a mocked APIClient."""
    mock_api_client = mocker.Mock(spec=APIClient)
    user_service = UserService(mock_api_client)

    mock_api_client.get_user_data.return_value = {'id': 1, 'name': 'John Doe'}

    username = user_service.get_username(1)

    assert username == 'JOHN DOE'
    mock_api_client.get_user_data.assert_called_once_with(1)
