import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import get_labels


class TestGetLabels:
    """Unit tests for get_labels function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_success_empty(self, mock_label_to_dict, mock_get_api):
        """Test getting labels when no labels exist."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_api.get_labels.return_value = [[]]  # Paginator returns list of lists, empty

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 0
        assert len(result_data["labels"]) == 0
        assert result_data["labels"] == []

        mock_api.get_labels.assert_called_once()
        mock_label_to_dict.assert_not_called()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_success_single_label(self, mock_label_to_dict, mock_get_api):
        """Test getting labels with a single label."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_label = Mock()
        mock_api.get_labels.return_value = [[mock_label]]  # Paginator returns list of lists
        mock_label_to_dict.return_value = {
            "id": "123456789",
            "name": "work",
            "color": "blue",
            "order": 1,
            "is_favorite": False
        }

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert len(result_data["labels"]) == 1
        assert result_data["labels"][0]["id"] == "123456789"
        assert result_data["labels"][0]["name"] == "work"
        assert result_data["labels"][0]["color"] == "blue"

        mock_api.get_labels.assert_called_once()
        mock_label_to_dict.assert_called_once_with(mock_label)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_success_multiple_labels(self, mock_label_to_dict, mock_get_api):
        """Test getting multiple labels."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_label1 = Mock()
        mock_label2 = Mock()
        mock_label3 = Mock()
        mock_api.get_labels.return_value = [[mock_label1, mock_label2, mock_label3]]

        mock_label_to_dict.side_effect = [
            {"id": "1", "name": "urgent", "color": "red", "order": 1},
            {"id": "2", "name": "work", "color": "blue", "order": 2},
            {"id": "3", "name": "personal", "color": "green", "order": 3}
        ]

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 3
        assert len(result_data["labels"]) == 3
        assert result_data["labels"][0]["id"] == "1"
        assert result_data["labels"][0]["name"] == "urgent"
        assert result_data["labels"][1]["id"] == "2"
        assert result_data["labels"][1]["name"] == "work"
        assert result_data["labels"][2]["id"] == "3"
        assert result_data["labels"][2]["name"] == "personal"

        mock_api.get_labels.assert_called_once()
        assert mock_label_to_dict.call_count == 3

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_labels_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await get_labels()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_labels_api_call_error(self, mock_get_api):
        """Test error handling when API call fails."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.get_labels.side_effect = Exception("Todoist API error: authentication failed")

        result = await get_labels()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error: authentication failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_label_to_dict_error(self, mock_label_to_dict, mock_get_api):
        """Test error handling when label_to_dict fails."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_label = Mock()
        mock_api.get_labels.return_value = [[mock_label]]
        mock_label_to_dict.side_effect = Exception("Label serialization error")

        result = await get_labels()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Label serialization error" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_complex_label_data(self, mock_label_to_dict, mock_get_api):
        """Test getting labels with complex label data including special characters."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_label = Mock()
        mock_api.get_labels.return_value = [[mock_label]]
        mock_label_to_dict.return_value = {
            "id": "999",
            "name": "étiquette spéciale 🏷️",
            "color": "orange",
            "order": 5,
            "is_favorite": True,
            "created_at": "2023-01-01T00:00:00Z"
        }

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["labels"][0]["name"] == "étiquette spéciale 🏷️"
        assert result_data["labels"][0]["color"] == "orange"
        assert result_data["labels"][0]["is_favorite"]

        mock_api.get_labels.assert_called_once()
        mock_label_to_dict.assert_called_once_with(mock_label)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_paginator_structure(self, mock_label_to_dict, mock_get_api):
        """Test that the function correctly handles the paginator structure."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        # Test the specific paginator structure: list(paginator)[0]
        mock_label1 = Mock()
        mock_label2 = Mock()
        mock_paginator = [[mock_label1, mock_label2]]  # Paginator returns a nested structure
        mock_api.get_labels.return_value = mock_paginator

        mock_label_to_dict.side_effect = [
            {"id": "1", "name": "Label 1"},
            {"id": "2", "name": "Label 2"}
        ]

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 2
        assert len(result_data["labels"]) == 2

        mock_api.get_labels.assert_called_once()
        assert mock_label_to_dict.call_count == 2

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_common_label_names(self, mock_label_to_dict, mock_get_api):
        """Test getting labels with common label names and scenarios."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_label1 = Mock()
        mock_label2 = Mock()
        mock_label3 = Mock()
        mock_label4 = Mock()
        mock_api.get_labels.return_value = [[mock_label1, mock_label2, mock_label3, mock_label4]]

        mock_label_to_dict.side_effect = [
            {"id": "1", "name": "@home", "color": "green"},
            {"id": "2", "name": "@work", "color": "blue"},
            {"id": "3", "name": "high-priority", "color": "red"},
            {"id": "4", "name": "waiting_for", "color": "yellow"}
        ]

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 4
        assert len(result_data["labels"]) == 4

        label_names = [label["name"] for label in result_data["labels"]]
        assert "@home" in label_names
        assert "@work" in label_names
        assert "high-priority" in label_names
        assert "waiting_for" in label_names

        mock_api.get_labels.assert_called_once()
        assert mock_label_to_dict.call_count == 4

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_json_formatting(self, mock_label_to_dict, mock_get_api):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_label = Mock()
        mock_api.get_labels.return_value = [[mock_label]]
        mock_label_to_dict.return_value = {"id": "1", "name": "test_label"}

        result = await get_labels()

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "labels" in result_data
        assert "count" in result_data

        assert isinstance(result_data["labels"], list)
        assert isinstance(result_data["count"], int)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_return_type(self, mock_label_to_dict, mock_get_api):
        """Test that the function returns a string (JSON)."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.get_labels.return_value = [[]]

        result = await get_labels()

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_large_dataset(self, mock_label_to_dict, mock_get_api):
        """Test getting a large number of labels."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_labels = [Mock() for _ in range(50)]
        mock_api.get_labels.return_value = [mock_labels]

        # Create side effects for label_to_dict
        mock_label_to_dict.side_effect = [
            {"id": str(i), "name": f"label_{i}", "color": "blue"}
            for i in range(50)
        ]

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 50
        assert len(result_data["labels"]) == 50
        assert result_data["labels"][0]["name"] == "label_0"
        assert result_data["labels"][49]["name"] == "label_49"

        mock_api.get_labels.assert_called_once()
        assert mock_label_to_dict.call_count == 50

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.label_to_dict')
    async def test_get_labels_unicode_and_special_chars(self, mock_label_to_dict, mock_get_api):
        """Test labels with various unicode characters and special symbols."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_label1 = Mock()
        mock_label2 = Mock()
        mock_label3 = Mock()
        mock_api.get_labels.return_value = [[mock_label1, mock_label2, mock_label3]]

        mock_label_to_dict.side_effect = [
            {"id": "1", "name": "重要", "color": "red"},  # Chinese
            {"id": "2", "name": "срочно", "color": "orange"},  # Russian
            {"id": "3", "name": "🔥hot-topic⭐", "color": "yellow"}  # Emojis and special chars
        ]

        result = await get_labels()

        result_data = json.loads(result)
        assert result_data["count"] == 3
        assert result_data["labels"][0]["name"] == "重要"
        assert result_data["labels"][1]["name"] == "срочно"
        assert result_data["labels"][2]["name"] == "🔥hot-topic⭐"

        mock_api.get_labels.assert_called_once()
        assert mock_label_to_dict.call_count == 3
