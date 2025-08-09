import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import reopen_task
from todoist_api_python.api import TodoistAPI


class TestReopenTask:
    """Unit tests for reopen_task function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_success(self, mock_get_api):
        """Test successfully reopening a task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = True

        result = await reopen_task("task_123")

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["message"] == "Task task_123 reopened"

        mock_api.uncomplete_task.assert_called_once_with(task_id="task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_success_different_task_ids(self, mock_get_api):
        """Test reopening tasks with different task ID formats."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        test_task_ids = [
            "123456789",
            "task_xyz_789",
            "completed-task-456",
            "very_long_completed_task_id_with_multiple_sections_987654321",
            "task.completed.dots.456",
            "COMPLETED_TASK_ID_789"
        ]

        for task_id in test_task_ids:
            mock_api.uncomplete_task.return_value = True

            result = await reopen_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} reopened"

            mock_api.uncomplete_task.assert_called_with(task_id=task_id)

            # Reset mock for next iteration
            mock_api.uncomplete_task.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_api_returns_false(self, mock_get_api):
        """Test handling when API uncomplete_task returns False."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = False

        result = await reopen_task("task_456")

        result_data = json.loads(result)
        assert "error" in result_data
        assert result_data["error"] == "Failed to reopen task"

        mock_api.uncomplete_task.assert_called_once_with(task_id="task_456")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await reopen_task("task_789")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_api_call_error(self, mock_get_api):
        """Test error handling when API uncomplete_task call fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("Todoist API error: task not found")

        result = await reopen_task("invalid_task_id")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error: task not found" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="invalid_task_id")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_task_not_completed(self, mock_get_api):
        """Test error handling when trying to reopen a task that is not completed."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("Task is not completed")

        result = await reopen_task("active_task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task is not completed" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="active_task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_task_not_found(self, mock_get_api):
        """Test error handling when task does not exist."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("404 Not Found: Task does not exist")

        result = await reopen_task("nonexistent_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "404 Not Found: Task does not exist" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="nonexistent_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = ConnectionError("Network connection failed")

        result = await reopen_task("task_network_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Network connection failed" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="task_network_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_authentication_error(self, mock_get_api):
        """Test error handling when authentication fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("401 Unauthorized: Invalid token")

        result = await reopen_task("task_auth_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "401 Unauthorized: Invalid token" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="task_auth_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_permission_error(self, mock_get_api):
        """Test error handling when user lacks permission to reopen task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("403 Forbidden: Insufficient permissions")

        result = await reopen_task("restricted_task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "403 Forbidden: Insufficient permissions" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="restricted_task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_rate_limit_error(self, mock_get_api):
        """Test error handling when API rate limit is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("429 Too Many Requests: Rate limit exceeded")

        result = await reopen_task("rate_limit_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "429 Too Many Requests: Rate limit exceeded" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="rate_limit_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_server_error(self, mock_get_api):
        """Test error handling when server error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("500 Internal Server Error")

        result = await reopen_task("server_error_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "500 Internal Server Error" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="server_error_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_with_unicode_task_id(self, mock_get_api):
        """Test reopening task with unicode characters in task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = True

        unicode_task_id = "tâche_complétée_测试_🔄"

        result = await reopen_task(unicode_task_id)

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["message"] == f"Task {unicode_task_id} reopened"

        mock_api.uncomplete_task.assert_called_once_with(task_id=unicode_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_with_special_characters(self, mock_get_api):
        """Test reopening task with special characters in task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        special_task_ids = [
            "completed-task-with-dashes-123",
            "completed_task_with_underscores_456",
            "completed.task.with.dots.789",
            "completed@task@symbols#123",
            "completed%20task%20encoded",
            "completed+task+plus+signs+456"
        ]

        for task_id in special_task_ids:
            mock_api.uncomplete_task.return_value = True

            result = await reopen_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} reopened"

            mock_api.uncomplete_task.assert_called_with(task_id=task_id)

            # Reset mock for next iteration
            mock_api.uncomplete_task.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_empty_string_task_id(self, mock_get_api):
        """Test reopening task with empty string task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("Invalid task ID: empty string")

        result = await reopen_task("")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: empty string" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_whitespace_task_id(self, mock_get_api):
        """Test reopening task with whitespace-only task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("Invalid task ID: whitespace only")

        whitespace_task_id = "   "

        result = await reopen_task(whitespace_task_id)

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: whitespace only" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id=whitespace_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_return_type(self, mock_get_api):
        """Test that reopen_task returns a string (JSON)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = True

        result = await reopen_task("return_type_test")

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_json_structure_success(self, mock_get_api):
        """Test that successful reopening returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = True

        result = await reopen_task("structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "success" in result_data
        assert "message" in result_data
        assert result_data["success"]
        assert isinstance(result_data["message"], str)
        assert "structure_test" in result_data["message"]
        assert "reopened" in result_data["message"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_json_structure_failure(self, mock_get_api):
        """Test that failed reopening returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = False

        result = await reopen_task("failure_structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "error" in result_data
        assert isinstance(result_data["error"], str)
        assert "Failed to reopen task" in result_data["error"]
        assert "success" not in result_data
        assert "message" not in result_data

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_json_structure_exception(self, mock_get_api):
        """Test that exception returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("Test exception")

        result = await reopen_task("exception_structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "error" in result_data
        assert isinstance(result_data["error"], str)
        assert "Test exception" in result_data["error"]
        assert "success" not in result_data
        assert "message" not in result_data

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_json_formatting(self, mock_get_api):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = True

        result = await reopen_task("format_test")

        result_data = json.loads(result)

        reformatted = json.dumps(result_data, indent=2)

        assert isinstance(result_data, dict)
        assert isinstance(reformatted, str)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_multiple_consecutive_calls(self, mock_get_api):
        """Test multiple consecutive task reopenings."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        task_ids = ["completed_task_1", "completed_task_2", "completed_task_3", "completed_task_4", "completed_task_5"]

        for task_id in task_ids:
            mock_api.uncomplete_task.return_value = True

            result = await reopen_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} reopened"

            mock_api.uncomplete_task.assert_called_with(task_id=task_id)

        assert mock_api.uncomplete_task.call_count == len(task_ids)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_mixed_success_failure(self, mock_get_api):
        """Test mixed success and failure scenarios in sequence."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = True
        success_result = await reopen_task("success_task")
        success_data = json.loads(success_result)
        assert success_data["success"]
        assert "reopened" in success_data["message"]

        mock_api.uncomplete_task.return_value = False
        failure_result = await reopen_task("failure_task")
        failure_data = json.loads(failure_result)
        assert "error" in failure_data
        assert "Failed to reopen task" in failure_data["error"]

        mock_api.uncomplete_task.side_effect = Exception("Task is not completed")
        exception_result = await reopen_task("exception_task")
        exception_data = json.loads(exception_result)
        assert "error" in exception_data
        assert "Task is not completed" in exception_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_very_long_task_id(self, mock_get_api):
        """Test reopening task with very long task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = True

        long_task_id = "very_long_completed_task_id_" + "x" * 200 + "_end"

        result = await reopen_task(long_task_id)

        result_data = json.loads(result)
        assert result_data["success"]
        assert long_task_id in result_data["message"]
        assert "reopened" in result_data["message"]

        mock_api.uncomplete_task.assert_called_once_with(task_id=long_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_api_none_response(self, mock_get_api):
        """Test handling when API returns None instead of boolean."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.return_value = None

        result = await reopen_task("none_response_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Failed to reopen task" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="none_response_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_timeout_error(self, mock_get_api):
        """Test error handling when API call times out."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = TimeoutError("Request timed out")

        result = await reopen_task("timeout_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Request timed out" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="timeout_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_already_active_scenario(self, mock_get_api):
        """Test specific scenario when trying to reopen an already active task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("Cannot reopen task: Task is already active")

        result = await reopen_task("already_active_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot reopen task: Task is already active" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="already_active_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_shared_project_permission(self, mock_get_api):
        """Test error when trying to reopen task in shared project without permission."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception(
            "Cannot modify task in shared project: Insufficient permissions")

        result = await reopen_task("shared_project_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot modify task in shared project: Insufficient permissions" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="shared_project_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_reopen_task_deleted_task_scenario(self, mock_get_api):
        """Test error when trying to reopen a task that has been deleted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.uncomplete_task.side_effect = Exception("Task has been permanently deleted")

        result = await reopen_task("deleted_task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task has been permanently deleted" in result_data["error"]

        mock_api.uncomplete_task.assert_called_once_with(task_id="deleted_task_123")
