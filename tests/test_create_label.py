import asyncio
import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import create_label
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Label


@pytest.fixture(autouse=True)
def clear_global_api_state():
    """Clear the global API state before each test."""
    import todoist_mcp_server
    todoist_mcp_server._api = None
    yield
    todoist_mcp_server._api = None

@pytest.fixture
def mock_label():
    return Mock(spec=Label)


class TestCreateLabel:
    """Unit tests for create_label function."""

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_success_minimal(self, mock_label_to_dict, mock_get_api, mock_label):
        """Test successful label creation with minimal parameters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Test Label"}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label("Test Label")

        mock_get_api.assert_called_once()
        mock_api.add_label.assert_called_once_with(
            name="Test Label",
            color=None,
            is_favorite=None
        )
        mock_label_to_dict.assert_called_once_with(mock_label)

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_success_all_parameters(self, mock_label_to_dict, mock_get_api, mock_label):
        """Test successful label creation with all parameters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {
            "id": "123",
            "name": "Important Label",
            "color": "red",
            "is_favorite": True
        }
        mock_label_to_dict.return_value = expected_dict

        result = await create_label(
            name="Important Label",
            color="red",
            is_favorite=True
        )

        mock_get_api.assert_called_once()
        mock_api.add_label.assert_called_once_with(
            name="Important Label",
            color="red",
            is_favorite=True
        )
        mock_label_to_dict.assert_called_once_with(mock_label)

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_with_color_only(self, mock_label_to_dict, mock_get_api, mock_label):
        """Test label creation with color parameter only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Colored Label"}
        mock_label_to_dict.return_value = expected_dict

        await create_label(
            name="Colored Label",
            color="blue"
        )

        mock_api.add_label.assert_called_once_with(
            name="Colored Label",
            color="blue",
            is_favorite=None
        )

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_with_favorite_only(self, mock_label_to_dict, mock_get_api, mock_label):
        """Test label creation with is_favorite parameter only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Favorite Label"}
        mock_label_to_dict.return_value = expected_dict

        await create_label(
            name="Favorite Label",
            is_favorite=True
        )

        mock_api.add_label.assert_called_once_with(
            name="Favorite Label",
            color=None,
            is_favorite=True
        )

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = ValueError("TODOIST_TOKEN environment variable is required")

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "TODOIST_TOKEN environment variable is required" in result_dict["error"]

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_api_add_label_error(self, mock_get_api):
        """Test error handling when API add_label fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_label.side_effect = Exception("API error: Invalid label name")

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "API error: Invalid label name" in result_dict["error"]

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_label_to_dict_error(self, mock_label_to_dict, mock_get_api, mock_label):
        """Test error handling when label_to_dict fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label
        mock_label_to_dict.side_effect = Exception("Serialization error")

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Serialization error" in result_dict["error"]

    @pytest.mark.parametrize("name", [
        "a",  # testing minimum character length
        "Label",  # normal length
        "a" * 60,  # testing maximum character length
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_valid_name_lengths(self, mock_label_to_dict, mock_get_api, mock_label, name):
        """Test label creation with various valid name lengths."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": name}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label(name)

        mock_api.add_label.assert_called_once_with(
            name=name,
            color=None,
            is_favorite=None
        )

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @pytest.mark.parametrize("color", [
        "red",
        "orange",
        "yellow",
        "olive_green",
        "lime_green",
        "green",
        "mint_green",
        "teal",
        "sky_blue",
        "light_blue",
        "blue",
        "grape",
        "violet",
        "lavender",
        "magenta",
        "salmon",
        "charcoal",
        "grey",
        "taupe"
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_various_color_values(self, mock_label_to_dict, mock_get_api, mock_label, color):
        """Test label creation with various color values."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Colored Label"}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label("Colored Label", color=color)

        mock_api.add_label.assert_called_once()
        assert mock_api.add_label.call_args[1]["color"] == color

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @pytest.mark.parametrize("favorite_value", [
        True,
        False
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_boolean_favorite_values(self, mock_label_to_dict, mock_get_api, mock_label, favorite_value):
        """Test label creation with boolean is_favorite values."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Test Label"}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label("Test Label", is_favorite=favorite_value)

        mock_api.add_label.assert_called_once()
        assert mock_api.add_label.call_args[1]["is_favorite"] == favorite_value

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_json_output_format(self, mock_label_to_dict, mock_get_api, mock_label):
        """Test that the output is properly formatted JSON."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {
            "id": "123",
            "name": "Test Label",
            "color": "red",
            "is_favorite": True
        }
        mock_label_to_dict.return_value = expected_dict

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert result_dict == expected_dict

        assert "\n" in result
        assert "  " in result

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_multiple_labels_isolation(self, mock_label_to_dict, mock_get_api):
        """Test creating multiple labels to ensure proper isolation."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_label1 = Mock(spec=Label)
        mock_label2 = Mock(spec=Label)

        # Setup different return values for each call
        mock_api.add_label.side_effect = [mock_label1, mock_label2]

        expected_dict1 = {"id": "123", "name": "Label 1"}
        expected_dict2 = {"id": "456", "name": "Label 2"}
        mock_label_to_dict.side_effect = [expected_dict1, expected_dict2]

        result1 = await create_label("Label 1")
        result2 = await create_label("Label 2")

        assert mock_api.add_label.call_count == 2
        assert mock_label_to_dict.call_count == 2

        result_dict1 = json.loads(result1)
        result_dict2 = json.loads(result2)

        assert result_dict1 == expected_dict1
        assert result_dict2 == expected_dict2

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_label.side_effect = ConnectionError("Network connection failed")

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Network connection failed" in result_dict["error"]

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_authentication_error(self, mock_get_api):
        """Test error handling when authentication error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_label.side_effect = ValueError("Invalid authentication token")

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Invalid authentication token" in result_dict["error"]

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_quota_exceeded_error(self, mock_get_api):
        """Test error handling when quota is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_label.side_effect = Exception("Label quota exceeded")

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Label quota exceeded" in result_dict["error"]

    @pytest.mark.parametrize("special_names", [
        "label with spaces",
        "label-with-dashes",
        "label_with_underscores",
        "label with números 123",
        "label with émojis 🏷️",
        "label with symbols !@#$%",
        "label with unicode 测试",
        "label with quotes \"test\"",
        "label with apostrophe's",
        "@work",
        "#important",
        "work:urgent"
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_special_characters_in_name(self, mock_label_to_dict, mock_get_api, mock_label, special_names):
        """Test label creation with special characters in name."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Special Label"}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label(special_names)

        mock_api.add_label.assert_called_once()
        assert mock_api.add_label.call_args[1]["name"] == special_names

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @patch('todoist_mcp_server.logger')
    @pytest.mark.asyncio
    async def test_create_label_logging_behavior(self, mock_logger, mock_label_to_dict, mock_get_api, mock_label):
        """Test that proper logging occurs during label creation."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Test Label"}
        mock_label_to_dict.return_value = expected_dict

        await create_label("Test Label")

        mock_logger.info.assert_called_once_with("Creating new label: Test Label")
        mock_logger.error.assert_not_called()

        mock_logger.reset_mock()
        mock_api.add_label.side_effect = Exception("Test error")

        await create_label("Error Label")

        mock_logger.info.assert_called_once_with("Creating new label: Error Label")
        mock_logger.error.assert_called_once_with("Error creating label Error Label: Test error")

    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_return_type_consistency(self, mock_label_to_dict, mock_get_api, mock_label):
        """Test that create_label always returns a string."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label
        mock_label_to_dict.return_value = {"id": "123", "name": "Test"}

        result = await create_label("Test Label")
        assert isinstance(result, str)

        mock_api.add_label.side_effect = Exception("Test error")

        result = await create_label("Error Label")
        assert isinstance(result, str)

        error_dict = json.loads(result)
        assert "error" in error_dict

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_concurrent_creation_simulation(self, mock_get_api):
        """Test behavior under simulated concurrent label creation."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        # Create multiple mock labels
        mock_labels = [Mock(spec=Label) for _ in range(5)]
        mock_api.add_label.side_effect = mock_labels

        with patch('todoist_mcp_server.label_to_dict') as mock_label_to_dict:
            mock_label_to_dict.side_effect = [
                {"id": f"{i}", "name": f"Label {i}"} for i in range(5)
            ]

            results = []
            for i in range(5):
                result = await create_label(f"Label {i}")
                results.append(result)

            assert mock_api.add_label.call_count == 5
            assert mock_label_to_dict.call_count == 5

            for i, result in enumerate(results):
                result_dict = json.loads(result)
                assert result_dict["id"] == str(i)
                assert result_dict["name"] == f"Label {i}"

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_duplicate_name_handling(self, mock_get_api):
        """Test behavior when creating labels with duplicate names."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_label.side_effect = Exception("Label name already exists")

        result = await create_label("existing-label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Label name already exists" in result_dict["error"]

    @patch('todoist_mcp_server.get_api')
    @pytest.mark.asyncio
    async def test_create_label_invalid_color_handling(self, mock_get_api):
        """Test behavior when creating labels with invalid colors."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_label.side_effect = Exception("Invalid color value")

        result = await create_label("test-label", color="invalid_color")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Invalid color value" in result_dict["error"]

    @pytest.mark.parametrize("common_patterns", [
        "work",
        "personal",
        "urgent",
        "important",
        "home",
        "office",
        "project",
        "meeting",
        "deadline",
        "waiting",
        "someday",
        "review",
        "call",
        "email",
        "errands",
        "shopping",
        "health",
        "finance",
        "travel",
        "hobby"
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_common_label_patterns(self, mock_label_to_dict, mock_get_api, mock_label, common_patterns):
        """Test creation with common label naming patterns."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "test"}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label(common_patterns)

        mock_api.add_label.assert_called_once()
        assert mock_api.add_label.call_args[1]["name"] == common_patterns

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @pytest.mark.parametrize("boundary_case", [
        "a", # single character
        "ab", # two characters
        "a" * 59, # 59 characters
        "a" * 60, # 60 characters (maximum)
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_boundary_length_validation(self, mock_label_to_dict, mock_get_api, mock_label, boundary_case):
        """Test label creation at exact boundary lengths."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "boundary_test"}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label(boundary_case)

        mock_api.add_label.assert_called_once()
        assert mock_api.add_label.call_args[1]["name"] == boundary_case

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @pytest.mark.parametrize("color, is_favorite", [
        (None, None),
        (None, True),
        (None, False),
        ("red", None),
        ("red", True),
        ("red", False),
        ("blue", True),
        ("green", False)
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_color_and_favorite_combinations(self, mock_label_to_dict, mock_get_api, mock_label, color, is_favorite):
        """Test all combinations of color and favorite parameters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.add_label.return_value = mock_label

        expected_dict = {"id": "123", "name": "Combo Label"}
        mock_label_to_dict.return_value = expected_dict

        result = await create_label("Combo Label", color=color, is_favorite=is_favorite)

        mock_api.add_label.assert_called_once()
        call_args = mock_api.add_label.call_args[1]
        assert call_args["name"] == "Combo Label"
        assert call_args["color"] == color
        assert call_args["is_favorite"] == is_favorite

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @pytest.mark.parametrize("error_scenario", [
        TimeoutError("Request timeout"),
        asyncio.TimeoutError("Async timeout"),
        ConnectionError("Connection lost"),
        Exception("Unexpected async error")
    ])
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    @pytest.mark.asyncio
    async def test_create_label_async_error_propagation(self, mock_label_to_dict, mock_get_api, error_scenario):
        """Test that async errors are properly propagated and handled."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_api.add_label.side_effect = error_scenario

        result = await create_label("Test Label")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert str(error_scenario) in result_dict["error"]
