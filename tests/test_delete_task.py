import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import delete_task
from todoist_api_python.api import TodoistAPI


class TestDeleteTask:
    """Unit tests for delete_task function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_success(self, mock_get_api):
        """Test successfully deleting a task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True

        result = await delete_task("task_123")

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["message"] == "Task task_123 deleted"

        mock_api.delete_task.assert_called_once_with(task_id="task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_success_different_task_ids(self, mock_get_api):
        """Test deleting tasks with different task ID formats."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        test_task_ids = [
            "123456789",
            "task_delete_789",
            "old-task-456",
            "very_long_task_id_to_be_permanently_deleted_123456789",
            "task.to.delete.456",
            "TASK_TO_DELETE_789",
            "temp_task_cleanup_2023"
        ]

        for task_id in test_task_ids:
            mock_api.delete_task.return_value = True

            result = await delete_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} deleted"

            mock_api.delete_task.assert_called_with(task_id=task_id)

            # Reset mock for next iteration
            mock_api.delete_task.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_api_returns_false(self, mock_get_api):
        """Test handling when API delete_task returns False."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = False

        result = await delete_task("task_456")

        result_data = json.loads(result)
        assert "error" in result_data
        assert result_data["error"] == "Failed to delete task"

        mock_api.delete_task.assert_called_once_with(task_id="task_456")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await delete_task("task_789")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_api_call_error(self, mock_get_api):
        """Test error handling when API delete_task call fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Todoist API error: task not found")

        result = await delete_task("invalid_task_id")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error: task not found" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="invalid_task_id")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_not_found(self, mock_get_api):
        """Test error handling when task does not exist."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("404 Not Found: Task does not exist")

        result = await delete_task("nonexistent_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "404 Not Found: Task does not exist" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="nonexistent_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_already_deleted(self, mock_get_api):
        """Test error handling when task has already been deleted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Task has already been deleted")

        result = await delete_task("already_deleted_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task has already been deleted" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="already_deleted_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_has_subtasks(self, mock_get_api):
        """Test error handling when task has subtasks that prevent deletion."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Cannot delete task: Task has active subtasks")

        result = await delete_task("parent_task_with_subtasks")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot delete task: Task has active subtasks" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="parent_task_with_subtasks")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = ConnectionError("Network connection failed")

        result = await delete_task("task_network_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Network connection failed" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="task_network_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_authentication_error(self, mock_get_api):
        """Test error handling when authentication fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("401 Unauthorized: Invalid token")

        result = await delete_task("task_auth_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "401 Unauthorized: Invalid token" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="task_auth_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_permission_error(self, mock_get_api):
        """Test error handling when user lacks permission to delete task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("403 Forbidden: Insufficient permissions to delete task")

        result = await delete_task("restricted_task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "403 Forbidden: Insufficient permissions to delete task" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="restricted_task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_shared_project_restriction(self, mock_get_api):
        """Test error when trying to delete task in shared project without admin rights."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Cannot delete task in shared project: Admin privileges required")

        result = await delete_task("shared_project_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot delete task in shared project: Admin privileges required" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="shared_project_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_rate_limit_error(self, mock_get_api):
        """Test error handling when API rate limit is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("429 Too Many Requests: Rate limit exceeded")

        result = await delete_task("rate_limit_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "429 Too Many Requests: Rate limit exceeded" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="rate_limit_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_server_error(self, mock_get_api):
        """Test error handling when server error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("500 Internal Server Error: Database unavailable")

        result = await delete_task("server_error_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "500 Internal Server Error: Database unavailable" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="server_error_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_with_unicode_task_id(self, mock_get_api):
        """Test deleting task with unicode characters in task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True

        unicode_task_id = "tâche_à_supprimer_测试_🗑️"

        result = await delete_task(unicode_task_id)

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["message"] == f"Task {unicode_task_id} deleted"

        mock_api.delete_task.assert_called_once_with(task_id=unicode_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_with_special_characters(self, mock_get_api):
        """Test deleting task with special characters in task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        special_task_ids = [
            "delete-task-with-dashes-123",
            "delete_task_with_underscores_456",
            "delete.task.with.dots.789",
            "delete@task@symbols#123",
            "delete%20task%20encoded",
            "delete+task+plus+signs+456",
            "delete[task]brackets{789}",
            "delete|task|pipes|123"
        ]

        for task_id in special_task_ids:
            mock_api.delete_task.return_value = True

            result = await delete_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} deleted"

            mock_api.delete_task.assert_called_with(task_id=task_id)

            # Reset mock for next iteration
            mock_api.delete_task.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_empty_string_task_id(self, mock_get_api):
        """Test deleting task with empty string task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Invalid task ID: empty string")

        result = await delete_task("")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: empty string" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_whitespace_task_id(self, mock_get_api):
        """Test deleting task with whitespace-only task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Invalid task ID: whitespace only")

        whitespace_task_id = "   "

        result = await delete_task(whitespace_task_id)

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid task ID: whitespace only" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id=whitespace_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_cascade_deletion(self, mock_get_api):
        """Test successful deletion of task with subtasks (cascade deletion)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True

        result = await delete_task("parent_task_cascade")

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["message"] == "Task parent_task_cascade deleted"

        mock_api.delete_task.assert_called_once_with(task_id="parent_task_cascade")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_return_type(self, mock_get_api):
        """Test that delete_task returns a string (JSON)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True

        result = await delete_task("return_type_test")

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_json_structure_success(self, mock_get_api):
        """Test that successful deletion returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True

        result = await delete_task("structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "success" in result_data
        assert "message" in result_data
        assert result_data["success"]
        assert isinstance(result_data["message"], str)
        assert "structure_test" in result_data["message"]
        assert "deleted" in result_data["message"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_json_structure_failure(self, mock_get_api):
        """Test that failed deletion returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = False

        result = await delete_task("failure_structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "error" in result_data
        assert isinstance(result_data["error"], str)
        assert "Failed to delete task" in result_data["error"]
        assert "success" not in result_data
        assert "message" not in result_data

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_json_structure_exception(self, mock_get_api):
        """Test that exception returns correct JSON structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Test deletion exception")

        result = await delete_task("exception_structure_test")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "error" in result_data
        assert isinstance(result_data["error"], str)
        assert "Test deletion exception" in result_data["error"]
        assert "success" not in result_data
        assert "message" not in result_data

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_json_formatting(self, mock_get_api):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True

        result = await delete_task("format_test")

        result_data = json.loads(result)

        reformatted = json.dumps(result_data, indent=2)

        assert isinstance(result_data, dict)
        assert isinstance(reformatted, str)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_bulk_deletion_simulation(self, mock_get_api):
        """Test multiple consecutive task deletions (bulk cleanup scenario)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        task_ids = [
            "cleanup_task_1",
            "cleanup_task_2",
            "cleanup_task_3",
            "old_completed_task_4",
            "archived_task_5"
        ]

        for task_id in task_ids:
            mock_api.delete_task.return_value = True

            result = await delete_task(task_id)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["message"] == f"Task {task_id} deleted"

            mock_api.delete_task.assert_called_with(task_id=task_id)

        # Verify total number of calls
        assert mock_api.delete_task.call_count == len(task_ids)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_mixed_success_failure(self, mock_get_api):
        """Test mixed success and failure scenarios in sequence."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True
        success_result = await delete_task("success_delete_task")
        success_data = json.loads(success_result)
        assert success_data["success"]
        assert "deleted" in success_data["message"]

        mock_api.delete_task.return_value = False
        failure_result = await delete_task("failure_delete_task")
        failure_data = json.loads(failure_result)
        assert "error" in failure_data
        assert "Failed to delete task" in failure_data["error"]

        mock_api.delete_task.side_effect = Exception("403 Forbidden: Insufficient permissions")
        permission_result = await delete_task("permission_delete_task")
        permission_data = json.loads(permission_result)
        assert "error" in permission_data
        assert "403 Forbidden: Insufficient permissions" in permission_data["error"]

        mock_api.delete_task.side_effect = Exception("404 Not Found: Task does not exist")
        notfound_result = await delete_task("notfound_delete_task")
        notfound_data = json.loads(notfound_result)
        assert "error" in notfound_data
        assert "404 Not Found: Task does not exist" in notfound_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_very_long_task_id(self, mock_get_api):
        """Test deleting task with very long task ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = True

        long_task_id = "very_long_task_id_for_deletion_testing_" + "x" * 200 + "_end"

        result = await delete_task(long_task_id)

        result_data = json.loads(result)
        assert result_data["success"]
        assert long_task_id in result_data["message"]
        assert "deleted" in result_data["message"]

        mock_api.delete_task.assert_called_once_with(task_id=long_task_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_api_none_response(self, mock_get_api):
        """Test handling when API returns None instead of boolean."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.return_value = None

        result = await delete_task("none_response_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Failed to delete task" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="none_response_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_timeout_error(self, mock_get_api):
        """Test error handling when API call times out."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = TimeoutError("Request timed out during deletion")

        result = await delete_task("timeout_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Request timed out during deletion" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="timeout_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_concurrent_deletion_conflict(self, mock_get_api):
        """Test error when task is deleted by another client concurrently."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("409 Conflict: Task was modified by another client")

        result = await delete_task("concurrent_deletion_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "409 Conflict: Task was modified by another client" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="concurrent_deletion_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_recurring_task_restriction(self, mock_get_api):
        """Test error when trying to delete a recurring task template."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Cannot delete recurring task template: Use archive instead")

        result = await delete_task("recurring_task_template")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot delete recurring task template: Use archive instead" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="recurring_task_template")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_delete_task_project_archived_restriction(self, mock_get_api):
        """Test error when trying to delete task from archived project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.delete_task.side_effect = Exception("Cannot delete task from archived project")

        result = await delete_task("archived_project_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot delete task from archived project" in result_data["error"]

        mock_api.delete_task.assert_called_once_with(task_id="archived_project_task")
