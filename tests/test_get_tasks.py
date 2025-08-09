import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import get_tasks


class TestGetTasks:
    """Unit tests for get_tasks function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_tasks_success_no_filters(self, mock_task_to_dict, mock_get_api):
        """Test getting all tasks without filters."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task = Mock()
        mock_api.get_tasks.return_value = [[mock_task]]  # Paginator returns list of lists
        mock_task_to_dict.return_value = {"id": "123", "content": "Test task"}

        result = await get_tasks()

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert len(result_data["tasks"]) == 1
        assert result_data["tasks"][0]["id"] == "123"

        mock_api.get_tasks.assert_called_once_with(
            project_id=None, section_id=None, label=None, ids=None
        )
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_tasks_with_project_id(self, mock_task_to_dict, mock_get_api):
        """Test getting tasks filtered by project ID."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.get_tasks.return_value = [[]]  # Empty result

        result = await get_tasks(project_id="12345")

        mock_api.get_tasks.assert_called_once_with(
            project_id="12345", section_id=None, label=None, ids=None
        )

        result_data = json.loads(result)
        assert result_data["count"] == 0
        assert result_data["tasks"] == []

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_tasks_with_filter_expression(self, mock_task_to_dict, mock_get_api):
        """Test getting tasks using filter expression."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task = Mock()
        mock_api.filter_tasks.return_value = [[mock_task]]
        mock_task_to_dict.return_value = {"id": "456", "content": "Today task"}

        result = await get_tasks(filter_expr="today")

        mock_api.filter_tasks.assert_called_once_with(query="today", lang=None)

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["tasks"][0]["id"] == "456"

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_tasks_with_multiple_filters(self, mock_task_to_dict, mock_get_api):
        """Test getting tasks with multiple filter parameters."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.get_tasks.return_value = [[]]

        await get_tasks(
            project_id="123",
            section_id="456",
            label="work",
            ids=["task1", "task2"]
        )

        mock_api.get_tasks.assert_called_once_with(
            project_id="123",
            section_id="456",
            label="work",
            ids=["task1", "task2"]
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_tasks_multiple_tasks(self, mock_task_to_dict, mock_get_api):
        """Test getting multiple tasks."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_api.get_tasks.return_value = [[mock_task1, mock_task2]]

        mock_task_to_dict.side_effect = [
            {"id": "1", "content": "Task 1"},
            {"id": "2", "content": "Task 2"}
        ]

        result = await get_tasks()

        result_data = json.loads(result)
        assert result_data["count"] == 2
        assert len(result_data["tasks"]) == 2
        assert result_data["tasks"][0]["id"] == "1"
        assert result_data["tasks"][1]["id"] == "2"

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_tasks_api_error(self, mock_get_api):
        """Test error handling when API call fails."""
        mock_get_api.side_effect = Exception("API connection failed")

        result = await get_tasks()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API connection failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_tasks_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.get_tasks.side_effect = Exception("Todoist API error")

        result = await get_tasks()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_tasks_filter_with_language(self, mock_task_to_dict, mock_get_api):
        """Test filter expression with language parameter."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.filter_tasks.return_value = [[]]

        await get_tasks(filter_expr="heute", lang="de")

        mock_api.filter_tasks.assert_called_once_with(query="heute", lang="de")
