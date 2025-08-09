import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import complete_task
from todoist_api_python.api import TodoistAPI


class TestCompleteTask:
    """Unit tests for complete_task function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_success(self, mock_get_api):
        """Test successfully completing a task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = True

        result = await complete_task("task_123")

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["message"] == "Task task_123 completed"

        mock_api.complete_task.assert_called_once_with(task_id="task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_success_different_task_ids(self, mock_get_api):
        """Test completing tasks with different task ID formats."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        test_task_ids = [
            "123456789",
            "task_abc_123",
            "proj-123-task-456",
            "very_long_task_id_with_multiple_underscores_123456789",
            "task.with.dots.123",
            "UPPERCASE_TASK_ID_456"
        ]

        for task_id in test_task_ids:
            mock_api.complete_task.return_value = True

            result = await complete_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} completed"

            mock_api.complete_task.assert_called_with(task_id=task_id)

            # Reset mock for next iteration
            mock_api.complete_task.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_api_returns_false(self, mock_get_api):
        """Test handling when API complete_task returns False."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = False

        result = await complete_task("task_456")

        result_data = json.loads(result)
        assert "error" in result_data
        assert result_data["error"] == "Failed to complete task"

        mock_api.complete_task.assert_called_once_with(task_id="task_456")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await complete_task("task_789")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_api_call_error(self, mock_get_api):
        """Test error handling when API complete_task call fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("Todoist API error: task not found")

        result = await complete_task("invalid_task_id")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error: task not found" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="invalid_task_id")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = ConnectionError("Network connection failed")

        result = await complete_task("task_network_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Network connection failed" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="task_network_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_authentication_error(self, mock_get_api):
        """Test error handling when authentication fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("401 Unauthorized: Invalid token")

        result = await complete_task("task_auth_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "401 Unauthorized: Invalid token" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="task_auth_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_permission_error(self, mock_get_api):
        """Test error handling when user lacks permission to complete task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("403 Forbidden: Insufficient permissions")

        result = await complete_task("restricted_task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "403 Forbidden: Insufficient permissions" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="restricted_task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_rate_limit_error(self, mock_get_api):
        """Test error handling when API rate limit is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("429 Too Many Requests: Rate limit exceeded")

        result = await complete_task("rate_limit_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "429 Too Many Requests: Rate limit exceeded" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="rate_limit_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_server_error(self, mock_get_api):
        """Test error handling when server error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("500 Internal Server Error")

        result = await complete_task("server_error_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "500 Internal Server Error" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="server_error_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_with_unicode_task_id(self, mock_get_api):
        """Test completing task with unicode characters in task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = True

        unicode_task_id = "tâche_123_测试_🎯"

        result = await complete_task(unicode_task_id)

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["message"] == f"Task {unicode_task_id} completed"

        mock_api.complete_task.assert_called_once_with(task_id=unicode_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_with_special_characters(self, mock_get_api):
        """Test completing task with special characters in task ID."""
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
            mock_api.complete_task.return_value = True

            result = await complete_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} completed"

            mock_api.complete_task.assert_called_with(task_id=task_id)

            # Reset mock for next iteration
            mock_api.complete_task.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_empty_string_task_id(self, mock_get_api):
        """Test completing task with empty string task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("Invalid task ID: empty string")

        result = await complete_task("")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: empty string" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_whitespace_task_id(self, mock_get_api):
        """Test completing task with whitespace-only task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("Invalid task ID: whitespace only")

        whitespace_task_id = "   "

        result = await complete_task(whitespace_task_id)

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: whitespace only" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id=whitespace_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_return_type(self, mock_get_api):
        """Test that complete_task returns a string (JSON)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = True

        result = await complete_task("return_type_test")

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_json_structure_success(self, mock_get_api):
        """Test that successful completion returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = True

        result = await complete_task("structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "success" in result_data
        assert "message" in result_data
        assert result_data["success"]
        assert isinstance(result_data["message"], str)
        assert "structure_test" in result_data["message"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_json_structure_failure(self, mock_get_api):
        """Test that failed completion returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = False

        result = await complete_task("failure_structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "error" in result_data
        assert isinstance(result_data["error"], str)
        assert "success" not in result_data
        assert "message" not in result_data

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_json_structure_exception(self, mock_get_api):
        """Test that exception returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = Exception("Test exception")

        result = await complete_task("exception_structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "error" in result_data
        assert isinstance(result_data["error"], str)
        assert "Test exception" in result_data["error"]
        assert "success" not in result_data
        assert "message" not in result_data

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_json_formatting(self, mock_get_api):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = True

        result = await complete_task("format_test")

        result_data = json.loads(result)

        # Re-serialize to check formatting
        reformatted = json.dumps(result_data, indent=2)

        # Both should be valid JSON
        assert isinstance(result_data, dict)
        assert isinstance(reformatted, str)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_multiple_consecutive_calls(self, mock_get_api):
        """Test multiple consecutive task completions."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        task_ids = ["task_1", "task_2", "task_3", "task_4", "task_5"]

        for task_id in task_ids:
            mock_api.complete_task.return_value = True

            result = await complete_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} completed"

            mock_api.complete_task.assert_called_with(task_id=task_id)

        # Verify total number of calls
        assert mock_api.complete_task.call_count == len(task_ids)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_mixed_success_failure(self, mock_get_api):
        """Test mixed success and failure scenarios in sequence."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = True
        success_result = await complete_task("success_task")
        success_data = json.loads(success_result)
        assert success_data["success"]

        # Reset and test failed completion
        mock_api.complete_task.return_value = False
        failure_result = await complete_task("failure_task")
        failure_data = json.loads(failure_result)
        assert "error" in failure_data

        # Reset and test exception
        mock_api.complete_task.side_effect = Exception("API error")
        exception_result = await complete_task("exception_task")
        exception_data = json.loads(exception_result)
        assert "error" in exception_data
        assert "API error" in exception_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_very_long_task_id(self, mock_get_api):
        """Test completing task with very long task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = True

        long_task_id = "very_long_task_id_" + "x" * 200 + "_end"

        result = await complete_task(long_task_id)

        result_data = json.loads(result)
        assert result_data["success"]
        assert long_task_id in result_data["message"]

        mock_api.complete_task.assert_called_once_with(task_id=long_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_api_none_response(self, mock_get_api):
        """Test handling when API returns None instead of boolean."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.return_value = None

        result = await complete_task("none_response_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Failed to complete task" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="none_response_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_complete_task_timeout_error(self, mock_get_api):
        """Test error handling when API call times out."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.complete_task.side_effect = TimeoutError("Request timed out")

        result = await complete_task("timeout_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Request timed out" in result_data["error"]

        mock_api.complete_task.assert_called_once_with(task_id="timeout_task")
