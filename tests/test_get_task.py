import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import get_task
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task


class TestGetTask:
    """Unit tests for get_task function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_success_basic(self, mock_task_to_dict, mock_get_api):
        """Test successfully retrieving a basic task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "task_123",
            "content": "Basic test task",
            "description": "A simple task for testing",
            "is_completed": False,
            "priority": 1,
            "project_id": "project_456",
            "labels": [],
            "due": None
        }

        result = await get_task("task_123")

        result_data = json.loads(result)
        assert result_data["id"] == "task_123"
        assert result_data["content"] == "Basic test task"
        assert result_data["description"] == "A simple task for testing"
        assert not result_data["is_completed"]

        mock_api.get_task.assert_called_once_with(task_id="task_123")
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_success_complex(self, mock_task_to_dict, mock_get_api):
        """Test successfully retrieving a complex task with all fields."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "complex_task_456",
            "content": "Complex task with all features",
            "description": "A comprehensive task with multiple attributes and settings",
            "is_completed": False,
            "priority": 4,
            "project_id": "project_789",
            "section_id": "section_123",
            "parent_id": "parent_task_456",
            "order": 5,
            "labels": ["urgent", "work", "review"],
            "due": {
                "date": "2023-12-31",
                "datetime": "2023-12-31T23:59:59Z",
                "string": "Dec 31",
                "timezone": "UTC"
            },
            "url": "https://todoist.com/showTask?id=complex_task_456",
            "created_at": "2023-01-01T00:00:00Z",
            "creator_id": "user_123",
            "assignee_id": "user_456",
            "assigner_id": "user_789"
        }

        result = await get_task("complex_task_456")

        result_data = json.loads(result)
        assert result_data["id"] == "complex_task_456"
        assert result_data["content"] == "Complex task with all features"
        assert result_data["priority"] == 4
        assert result_data["labels"] == ["urgent", "work", "review"]
        assert result_data["due"]["date"] == "2023-12-31"
        assert result_data["assignee_id"] == "user_456"

        mock_api.get_task.assert_called_once_with(task_id="complex_task_456")
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_success_completed_task(self, mock_task_to_dict, mock_get_api):
        """Test successfully retrieving a completed task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "completed_task_789",
            "content": "This task is completed",
            "description": "A task that has been marked as done",
            "is_completed": True,
            "priority": 2,
            "project_id": "project_123",
            "labels": ["done", "archived"],
            "due": None
        }

        result = await get_task("completed_task_789")

        result_data = json.loads(result)
        assert result_data["id"] == "completed_task_789"
        assert result_data["content"] == "This task is completed"
        assert result_data["is_completed"]
        assert result_data["labels"] == ["done", "archived"]

        mock_api.get_task.assert_called_once_with(task_id="completed_task_789")
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_success_subtask(self, mock_task_to_dict, mock_get_api):
        """Test successfully retrieving a subtask."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "subtask_321",
            "content": "Subtask under main project",
            "description": "This is a child task",
            "is_completed": False,
            "priority": 1,
            "project_id": "project_456",
            "parent_id": "parent_task_789",
            "order": 2,
            "labels": ["subtask"],
            "due": None
        }

        result = await get_task("subtask_321")

        result_data = json.loads(result)
        assert result_data["id"] == "subtask_321"
        assert result_data["content"] == "Subtask under main project"
        assert result_data["parent_id"] == "parent_task_789"
        assert result_data["labels"] == ["subtask"]

        mock_api.get_task.assert_called_once_with(task_id="subtask_321")
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_success_different_task_ids(self, mock_task_to_dict, mock_get_api):
        """Test retrieving tasks with different task ID formats."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        test_task_ids = [
            "123456789",
            "task_abc_123",
            "get-task-456",
            "very_long_task_id_for_retrieval_testing_123456789",
            "task.with.dots.789",
            "UPPERCASE_TASK_ID_456"
        ]

        for task_id in test_task_ids:
            mock_task = Mock(spec=Task)
            mock_api.get_task.return_value = mock_task

            mock_task_to_dict.return_value = {
                "id": task_id,
                "content": f"Task {task_id}",
                "description": f"Description for {task_id}",
                "is_completed": False,
                "priority": 1
            }

            result = await get_task(task_id)

            result_data = json.loads(result)
            assert result_data["id"] == task_id
            assert result_data["content"] == f"Task {task_id}"

            mock_api.get_task.assert_called_with(task_id=task_id)

            # Reset mocks for next iteration
            mock_api.get_task.reset_mock()
            mock_task_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_success_unicode_content(self, mock_task_to_dict, mock_get_api):
        """Test retrieving task with unicode characters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "unicode_task_123",
            "content": "Tâche avec caractères spéciaux 🎯",
            "description": "Description avec émojis 📝 et caractères accentués français",
            "is_completed": False,
            "priority": 3,
            "labels": ["français", "测试", "задача"]
        }

        result = await get_task("unicode_task_123")

        result_data = json.loads(result)
        assert result_data["content"] == "Tâche avec caractères spéciaux 🎯"
        assert result_data["description"] == "Description avec émojis 📝 et caractères accentués français"
        assert result_data["labels"] == ["français", "测试", "задача"]

        mock_api.get_task.assert_called_once_with(task_id="unicode_task_123")
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_not_found(self, mock_get_api):
        """Test error handling when task is not found."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("404 Not Found: Task does not exist")

        result = await get_task("nonexistent_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "404 Not Found: Task does not exist" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="nonexistent_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_deleted_task(self, mock_get_api):
        """Test error handling when trying to retrieve a deleted task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("Task has been deleted")

        result = await get_task("deleted_task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task has been deleted" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="deleted_task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_permission_denied(self, mock_get_api):
        """Test error handling when user lacks permission to view task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("403 Forbidden: Access denied to private task")

        result = await get_task("private_task_456")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "403 Forbidden: Access denied to private task" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="private_task_456")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await get_task("task_789")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = ConnectionError("Network connection failed")

        result = await get_task("task_network_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Network connection failed" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="task_network_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_authentication_error(self, mock_get_api):
        """Test error handling when authentication fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("401 Unauthorized: Invalid token")

        result = await get_task("task_auth_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "401 Unauthorized: Invalid token" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="task_auth_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_rate_limit_error(self, mock_get_api):
        """Test error handling when API rate limit is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("429 Too Many Requests: Rate limit exceeded")

        result = await get_task("rate_limit_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "429 Too Many Requests: Rate limit exceeded" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="rate_limit_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_server_error(self, mock_get_api):
        """Test error handling when server error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("500 Internal Server Error")

        result = await get_task("server_error_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "500 Internal Server Error" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="server_error_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_task_to_dict_error(self, mock_task_to_dict, mock_get_api):
        """Test error handling when task_to_dict fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.side_effect = Exception("Task serialization error")

        result = await get_task("serialization_error_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task serialization error" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="serialization_error_task")
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_empty_string_task_id(self, mock_get_api):
        """Test retrieving task with empty string task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("Invalid task ID: empty string")

        result = await get_task("")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: empty string" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_whitespace_task_id(self, mock_get_api):
        """Test retrieving task with whitespace-only task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("Invalid task ID: whitespace only")

        whitespace_task_id = "   "

        result = await get_task(whitespace_task_id)

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: whitespace only" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id=whitespace_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_with_special_characters(self, mock_task_to_dict, mock_get_api):
        """Test retrieving task with special characters in task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        special_task_ids = [
            "task-with-dashes-123",
            "task_with_underscores_456",
            "task.with.dots.789",
            "task@with@symbols#123",
            "task%20with%20encoding",
            "task+plus+signs+456"
        ]

        for task_id in special_task_ids:
            mock_task = Mock(spec=Task)
            mock_api.get_task.return_value = mock_task

            mock_task_to_dict.return_value = {
                "id": task_id,
                "content": f"Task with special characters: {task_id}",
                "is_completed": False
            }

            result = await get_task(task_id)

            result_data = json.loads(result)
            assert result_data["id"] == task_id
            assert task_id in result_data["content"]

            mock_api.get_task.assert_called_with(task_id=task_id)

            # Reset mocks for next iteration
            mock_api.get_task.reset_mock()
            mock_task_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_return_type(self, mock_task_to_dict, mock_get_api):
        """Test that get_task returns a string (JSON)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "return_type_test",
            "content": "Test task",
            "is_completed": False
        }

        result = await get_task("return_type_test")

        assert isinstance(result, str)
        # Verify it's valid JSON
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_json_formatting(self, mock_task_to_dict, mock_get_api):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "format_test",
            "content": "JSON formatting test task",
            "description": "Testing proper JSON output formatting",
            "is_completed": False,
            "priority": 2
        }

        result = await get_task("format_test")

        # Verify that the result is valid JSON with proper formatting
        result_data = json.loads(result)

        # Re-serialize to check formatting
        reformatted = json.dumps(result_data, indent=2, ensure_ascii=False, default=str)

        # Both should be valid JSON
        assert isinstance(result_data, dict)
        assert isinstance(reformatted, str)
        assert result_data["content"] == "JSON formatting test task"

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_direct_response_structure(self, mock_task_to_dict, mock_get_api):
        """Test that get_task returns task data directly (not wrapped in success/error structure)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "direct_response_test",
            "content": "Direct response test task",
            "description": "Testing direct task data response",
            "is_completed": False,
            "priority": 1,
            "labels": ["test"]
        }

        result = await get_task("direct_response_test")

        result_data = json.loads(result)

        # Should return task data directly, not wrapped in success/error structure
        assert "id" in result_data
        assert "content" in result_data
        assert "is_completed" in result_data
        assert "success" not in result_data  # No wrapper
        assert "message" not in result_data  # No wrapper
        assert result_data["id"] == "direct_response_test"
        assert result_data["content"] == "Direct response test task"

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_timeout_error(self, mock_get_api):
        """Test error handling when API call times out."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = TimeoutError("Request timed out")

        result = await get_task("timeout_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Request timed out" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="timeout_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_very_long_task_id(self, mock_task_to_dict, mock_get_api):
        """Test retrieving task with very long task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        # Create a very long task ID
        long_task_id = "very_long_task_id_for_retrieval_testing_" + "x" * 200 + "_end"

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": long_task_id,
            "content": "Task with very long ID",
            "description": "Testing retrieval with extremely long task identifier",
            "is_completed": False
        }

        result = await get_task(long_task_id)

        result_data = json.loads(result)
        assert result_data["id"] == long_task_id
        assert result_data["content"] == "Task with very long ID"

        mock_api.get_task.assert_called_once_with(task_id=long_task_id)
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_task_archived_project_access(self, mock_get_api):
        """Test error when trying to access task from archived project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_task.side_effect = Exception("Cannot access task from archived project")

        result = await get_task("archived_project_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot access task from archived project" in result_data["error"]

        mock_api.get_task.assert_called_once_with(task_id="archived_project_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_multiple_consecutive_calls(self, mock_task_to_dict, mock_get_api):
        """Test multiple consecutive task retrievals."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        task_ids = ["task_1", "task_2", "task_3", "task_4", "task_5"]

        for task_id in task_ids:
            mock_task = Mock(spec=Task)
            mock_api.get_task.return_value = mock_task

            mock_task_to_dict.return_value = {
                "id": task_id,
                "content": f"Content for {task_id}",
                "is_completed": False
            }

            result = await get_task(task_id)

            result_data = json.loads(result)
            assert result_data["id"] == task_id
            assert result_data["content"] == f"Content for {task_id}"

            mock_api.get_task.assert_called_with(task_id=task_id)

        # Verify total number of calls
        assert mock_api.get_task.call_count == len(task_ids)
        assert mock_task_to_dict.call_count == len(task_ids)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_get_task_high_priority_task(self, mock_task_to_dict, mock_get_api):
        """Test retrieving a high-priority task with all urgency indicators."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "urgent_task_999",
            "content": "URGENT: Critical system maintenance",
            "description": "This task requires immediate attention and cannot be delayed",
            "is_completed": False,
            "priority": 4,  # Highest priority
            "project_id": "critical_project",
            "labels": ["urgent", "critical", "system", "maintenance"],
            "due": {
                "date": "2023-12-24",
                "datetime": "2023-12-24T09:00:00Z",
                "string": "today"
            },
            "assignee_id": "admin_user"
        }

        result = await get_task("urgent_task_999")

        result_data = json.loads(result)
        assert result_data["priority"] == 4
        assert "URGENT" in result_data["content"]
        assert "urgent" in result_data["labels"]
        assert "critical" in result_data["labels"]
        assert result_data["due"]["string"] == "today"

        mock_api.get_task.assert_called_once_with(task_id="urgent_task_999")
        mock_task_to_dict.assert_called_once_with(mock_task)