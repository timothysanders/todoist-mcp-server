import pytest
import os
from unittest.mock import Mock, patch
from todoist_mcp_server import get_api
from todoist_api_python.api import TodoistAPI


@pytest.fixture(autouse=True)
def clear_global_api_state():
    """Clear the global API state before each test."""
    import todoist_mcp_server
    todoist_mcp_server._api = None
    yield
    todoist_mcp_server._api = None

class TestGetApi:
    """Unit tests for get_api function."""

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_success_with_token(self, mock_todoist_api, mock_getenv):
        """Test successful API initialization with valid token."""
        mock_getenv.return_value = "test_token_123"

        mock_api_instance = Mock(spec=TodoistAPI)
        mock_todoist_api.return_value = mock_api_instance

        result = get_api()

        mock_getenv.assert_called_once_with("TODOIST_TOKEN")

        mock_todoist_api.assert_called_once_with("test_token_123")

        assert result == mock_api_instance

    @patch('todoist_mcp_server.os.getenv')
    def test_get_api_missing_token_none(self, mock_getenv):
        """Test error handling when TODOIST_TOKEN is None."""
        mock_getenv.return_value = None

        with pytest.raises(ValueError) as excinfo:
            get_api()

        assert "TODOIST_TOKEN environment variable is required" in str(excinfo.value)
        mock_getenv.assert_called_once_with("TODOIST_TOKEN")

    @patch('todoist_mcp_server.os.getenv')
    def test_get_api_missing_token_empty_string(self, mock_getenv):
        """Test error handling when TODOIST_TOKEN is empty string."""
        mock_getenv.return_value = ""

        with pytest.raises(ValueError) as excinfo:
            get_api()

        assert "TODOIST_TOKEN environment variable is required" in str(excinfo.value)
        mock_getenv.assert_called_once_with("TODOIST_TOKEN")

    @patch('todoist_mcp_server.os.getenv')
    def test_get_api_missing_token_whitespace(self, mock_getenv):
        """Test error handling when TODOIST_TOKEN is only whitespace."""
        mock_getenv.return_value = "   "

        with pytest.raises(ValueError) as excinfo:
            get_api()

        assert "TODOIST_TOKEN environment variable is required" in str(excinfo.value)
        mock_getenv.assert_called_once_with("TODOIST_TOKEN")

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_singleton_behavior(self, mock_todoist_api, mock_getenv):
        """Test that get_api returns the same instance on multiple calls (singleton pattern)."""
        mock_getenv.return_value = "test_token_123"
        mock_api_instance = Mock(spec=TodoistAPI)
        mock_todoist_api.return_value = mock_api_instance

        result1 = get_api()

        result2 = get_api()

        result3 = get_api()

        mock_todoist_api.assert_called_once_with("test_token_123")

        mock_getenv.assert_called_once_with("TODOIST_TOKEN")

        assert result1 == result2 == result3 == mock_api_instance

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_with_different_token_formats(self, mock_todoist_api, mock_getenv):
        """Test API initialization with various valid token formats."""
        test_cases = [
            "simple_token",
            "token-with-dashes",
            "token_with_underscores",
            "TOKEN123WITH456NUMBERS",
            "very_long_token_string_with_multiple_sections_and_special_chars_123456789",
            "token.with.dots"
        ]

        for token in test_cases:
            # Reset the global state for each test case
            import todoist_mcp_server
            todoist_mcp_server._api = None

            mock_getenv.return_value = token
            mock_api_instance = Mock(spec=TodoistAPI)
            mock_todoist_api.return_value = mock_api_instance

            result = get_api()

            mock_todoist_api.assert_called_with(token)
            assert result == mock_api_instance

            # Reset mocks for next iteration
            mock_getenv.reset_mock()
            mock_todoist_api.reset_mock()

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_todoist_api_initialization_error(self, mock_todoist_api, mock_getenv):
        """Test error handling when TodoistAPI initialization fails."""
        mock_getenv.return_value = "test_token_123"
        mock_todoist_api.side_effect = Exception("API initialization failed")

        with pytest.raises(Exception) as excinfo:
            get_api()

        assert "API initialization failed" in str(excinfo.value)
        mock_getenv.assert_called_once_with("TODOIST_TOKEN")
        mock_todoist_api.assert_called_once_with("test_token_123")

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_todoist_api_authentication_error(self, mock_todoist_api, mock_getenv):
        """Test error handling when TodoistAPI raises authentication error."""
        mock_getenv.return_value = "invalid_token"
        mock_todoist_api.side_effect = ValueError("Invalid token provided")

        with pytest.raises(ValueError) as excinfo:
            get_api()

        assert "Invalid token provided" in str(excinfo.value)
        mock_getenv.assert_called_once_with("TODOIST_TOKEN")
        mock_todoist_api.assert_called_once_with("invalid_token")

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_network_error_during_init(self, mock_todoist_api, mock_getenv):
        """Test error handling when network error occurs during API initialization."""
        mock_getenv.return_value = "test_token_123"
        mock_todoist_api.side_effect = ConnectionError("Network connection failed")

        with pytest.raises(ConnectionError) as excinfo:
            get_api()

        assert "Network connection failed" in str(excinfo.value)
        mock_getenv.assert_called_once_with("TODOIST_TOKEN")
        mock_todoist_api.assert_called_once_with("test_token_123")

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_global_state_isolation(self, mock_todoist_api, mock_getenv):
        """Test that the global _api variable is properly managed."""
        import todoist_mcp_server

        assert todoist_mcp_server._api is None

        mock_getenv.return_value = "test_token_123"
        mock_api_instance = Mock(spec=TodoistAPI)
        mock_todoist_api.return_value = mock_api_instance

        # First call should initialize the global variable
        result = get_api()
        assert todoist_mcp_server._api == mock_api_instance
        assert result == mock_api_instance

        # Verify subsequent calls use the cached instance
        result2 = get_api()
        assert result2 == mock_api_instance

        mock_todoist_api.assert_called_once_with("test_token_123")

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_return_type(self, mock_todoist_api, mock_getenv):
        """Test that get_api returns the correct type."""
        mock_getenv.return_value = "test_token_123"
        mock_api_instance = Mock(spec=TodoistAPI)
        mock_todoist_api.return_value = mock_api_instance

        result = get_api()

        assert isinstance(result, type(mock_api_instance))
        assert result == mock_api_instance

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_multiple_error_scenarios(self, mock_todoist_api, mock_getenv):
        """Test multiple error scenarios in sequence."""
        import todoist_mcp_server

        # Test 1: Missing token
        mock_getenv.return_value = None
        with pytest.raises(ValueError):
            get_api()

        # Reset for next test
        todoist_mcp_server._api = None

        # Test 2: API initialization failure
        mock_getenv.return_value = "test_token"
        mock_todoist_api.side_effect = Exception("Init failed")
        with pytest.raises(Exception):
            get_api()

        # Reset for next test
        todoist_mcp_server._api = None
        mock_todoist_api.side_effect = None

        # Test 3: Successful initialization after failures
        mock_api_instance = Mock(spec=TodoistAPI)
        mock_todoist_api.return_value = mock_api_instance
        result = get_api()
        assert result == mock_api_instance

    def test_get_api_actual_environment_integration(self):
        """Test get_api behavior with actual environment variables (if available)."""
        import todoist_mcp_server

        # Store original state
        original_api = todoist_mcp_server._api
        original_token = os.environ.get("TODOIST_TOKEN")

        try:
            # Reset state
            todoist_mcp_server._api = None

            if "TODOIST_TOKEN" in os.environ:
                result = get_api()
                assert result is not None
                assert isinstance(result, TodoistAPI)
            else:
                with pytest.raises(ValueError):
                    get_api()

        finally:
            # Restore original state
            todoist_mcp_server._api = original_api
            if original_token is not None:
                os.environ["TODOIST_TOKEN"] = original_token
            elif "TODOIST_TOKEN" in os.environ:
                del os.environ["TODOIST_TOKEN"]

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_concurrent_access_simulation(self, mock_todoist_api, mock_getenv):
        """Test behavior under simulated concurrent access scenarios."""
        mock_getenv.return_value = "test_token_123"
        mock_api_instance = Mock(spec=TodoistAPI)
        mock_todoist_api.return_value = mock_api_instance

        # Simulate multiple "concurrent" calls
        results = []
        for i in range(10):
            result = get_api()
            results.append(result)

        # Verify all calls return the same instance
        assert all(result == mock_api_instance for result in results)

        # Verify initialization only happened once
        mock_todoist_api.assert_called_once_with("test_token_123")
        mock_getenv.assert_called_once_with("TODOIST_TOKEN")

    @patch('todoist_mcp_server.os.getenv')
    @patch('todoist_mcp_server.TodoistAPI')
    def test_get_api_edge_case_token_values(self, mock_todoist_api, mock_getenv):
        """Test edge cases for token values."""
        import todoist_mcp_server

        edge_cases = [
            ("0", True),  # Numeric string (valid)
            ("false", True),  # Boolean-like string (valid)
            ("null", True),  # Null-like string (valid)
            ("undefined", True),  # Undefined-like string (valid)
            ("a", True),  # Single character (valid)
            ("  token  ", True),  # Token with surrounding spaces (valid - os.getenv strips)
        ]

        for token_value, should_succeed in edge_cases:
            # Reset state
            todoist_mcp_server._api = None
            mock_getenv.reset_mock()
            mock_todoist_api.reset_mock()

            mock_getenv.return_value = token_value
            mock_api_instance = Mock(spec=TodoistAPI)
            mock_todoist_api.return_value = mock_api_instance

            if should_succeed:
                result = get_api()
                assert result == mock_api_instance
                mock_todoist_api.assert_called_once_with(token_value)
            else:
                with pytest.raises(ValueError):
                    get_api()
