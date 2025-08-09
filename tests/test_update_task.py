import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import update_task
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task


class TestUpdateTask:
    """Unit tests for update_task function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_content_only(self, mock_task_to_dict, mock_get_api):
        """Test updating a task with content only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True

        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "task_123",
            "content": "Updated task content",
            "description": "Original description",
            "priority": 2
        }

        result = await update_task("task_123", content="Updated task content")

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["id"] == "task_123"
        assert result_data["task"]["content"] == "Updated task content"

        mock_api.update_task.assert_called_once_with(
            task_id="task_123",
            content="Updated task content"
        )
        mock_api.get_task.assert_called_once_with(task_id="task_123")
        mock_task_to_dict.assert_called_once_with(mock_updated_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_multiple_fields(self, mock_task_to_dict, mock_get_api):
        """Test updating a task with multiple fields."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "task_456",
            "content": "Updated comprehensive task",
            "description": "New detailed description",
            "priority": 4,
            "labels": ["urgent", "work"],
            "due": {"date": "2023-12-31"}
        }

        result = await update_task(
            task_id="task_456",
            content="Updated comprehensive task",
            description="New detailed description",
            priority=4,
            labels=["urgent", "work"],
            due_date="2023-12-31"
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["content"] == "Updated comprehensive task"
        assert result_data["task"]["priority"] == 4
        assert result_data["task"]["labels"] == ["urgent", "work"]

        mock_api.update_task.assert_called_once_with(
            task_id="task_456",
            content="Updated comprehensive task",
            description="New detailed description",
            priority=4,
            labels=["urgent", "work"],
            due_date="2023-12-31"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_description_only(self, mock_task_to_dict, mock_get_api):
        """Test updating a task description only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "task_789",
            "content": "Original content",
            "description": "Updated description with more details"
        }

        result = await update_task(
            task_id="task_789",
            description="Updated description with more details"
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["description"] == "Updated description with more details"

        mock_api.update_task.assert_called_once_with(
            task_id="task_789",
            description="Updated description with more details"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_priority_levels(self, mock_task_to_dict, mock_get_api):
        """Test updating task with different priority levels."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        priorities = [1, 2, 3, 4]
        priority_names = ["normal", "high", "very high", "urgent"]

        for priority, name in zip(priorities, priority_names):
            mock_api.update_task.return_value = True
            mock_updated_task = Mock(spec=Task)
            mock_api.get_task.return_value = mock_updated_task

            mock_task_to_dict.return_value = {
                "id": f"priority_task_{priority}",
                "content": f"Task with {name} priority",
                "priority": priority
            }

            result = await update_task(f"priority_task_{priority}", priority=priority)

            result_data = json.loads(result)
            assert result_data["success"]
            assert result_data["task"]["priority"] == priority

            mock_api.update_task.assert_called_with(
                task_id=f"priority_task_{priority}",
                priority=priority
            )

            # Reset mocks for next iteration
            mock_api.update_task.reset_mock()
            mock_api.get_task.reset_mock()
            mock_task_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_labels(self, mock_task_to_dict, mock_get_api):
        """Test updating task labels."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "labels_task_123",
            "content": "Task with updated labels",
            "labels": ["work", "urgent", "review"]
        }

        result = await update_task(
            task_id="labels_task_123",
            labels=["work", "urgent", "review"]
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["labels"] == ["work", "urgent", "review"]

        mock_api.update_task.assert_called_once_with(
            task_id="labels_task_123",
            labels=["work", "urgent", "review"]
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_due_string(self, mock_task_to_dict, mock_get_api):
        """Test updating task with natural language due date."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "due_string_task",
            "content": "Task with updated due date",
            "due": {"string": "next Friday", "date": "2023-12-29"}
        }

        result = await update_task(
            task_id="due_string_task",
            due_string="next Friday"
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["due"]["string"] == "next Friday"

        mock_api.update_task.assert_called_once_with(
            task_id="due_string_task",
            due_string="next Friday"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_due_date(self, mock_task_to_dict, mock_get_api):
        """Test updating task with specific due date."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "due_date_task",
            "content": "Task with specific due date",
            "due": {"date": "2023-12-31"}
        }

        result = await update_task(
            task_id="due_date_task",
            due_date="2023-12-31"
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["due"]["date"] == "2023-12-31"

        mock_api.update_task.assert_called_once_with(
            task_id="due_date_task",
            due_date="2023-12-31"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_due_datetime(self, mock_task_to_dict, mock_get_api):
        """Test updating task with specific due datetime."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "due_datetime_task",
            "content": "Task with specific due datetime",
            "due": {"datetime": "2023-12-25T14:30:00Z"}
        }

        result = await update_task(
            task_id="due_datetime_task",
            due_datetime="2023-12-25T14:30:00Z"
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["due"]["datetime"] == "2023-12-25T14:30:00Z"

        mock_api.update_task.assert_called_once_with(
            task_id="due_datetime_task",
            due_datetime="2023-12-25T14:30:00Z"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_due_lang(self, mock_task_to_dict, mock_get_api):
        """Test updating task with due string in different language."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "due_lang_task",
            "content": "Tâche avec date française",
            "due": {"string": "demain", "date": "2023-12-25"}
        }

        result = await update_task(
            task_id="due_lang_task",
            due_string="demain",
            due_lang="fr"
        )

        result_data = json.loads(result)
        assert result_data["success"]

        mock_api.update_task.assert_called_once_with(
            task_id="due_lang_task",
            due_string="demain",
            due_lang="fr"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_success_assignee(self, mock_task_to_dict, mock_get_api):
        """Test updating task assignee."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "assignee_task",
            "content": "Task with new assignee",
            "assignee_id": "new_user_456"
        }

        result = await update_task(
            task_id="assignee_task",
            assignee_id="new_user_456"
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["assignee_id"] == "new_user_456"

        mock_api.update_task.assert_called_once_with(
            task_id="assignee_task",
            assignee_id="new_user_456"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_with_unicode_content(self, mock_task_to_dict, mock_get_api):
        """Test updating task with unicode characters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "unicode_task",
            "content": "Tâche mise à jour 🎯",
            "description": "Description avec émojis 📝 et caractères spéciaux",
            "labels": ["français", "测试"]
        }

        result = await update_task(
            task_id="unicode_task",
            content="Tâche mise à jour 🎯",
            description="Description avec émojis 📝 et caractères spéciaux",
            labels=["français", "测试"]
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["content"] == "Tâche mise à jour 🎯"
        assert result_data["task"]["description"] == "Description avec émojis 📝 et caractères spéciaux"
        assert result_data["task"]["labels"] == ["français", "测试"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_empty_labels_list(self, mock_task_to_dict, mock_get_api):
        """Test updating task with empty labels list."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "empty_labels_task",
            "content": "Task with cleared labels",
            "labels": []
        }

        result = await update_task(
            task_id="empty_labels_task",
            labels=[]
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["labels"] == []

        mock_api.update_task.assert_called_once_with(
            task_id="empty_labels_task",
            labels=[]
        )

    @pytest.mark.asyncio
    async def test_update_task_no_parameters_provided(self):
        """Test error when no update parameters are provided."""
        result = await update_task("task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No update parameters provided" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_update_task_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await update_task("task_123", content="Updated content")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_update_task_api_update_error(self, mock_get_api):
        """Test error handling when API update call fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.update_task.side_effect = Exception("Todoist API error: task not found")

        result = await update_task("invalid_task_id", content="Updated content")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error: task not found" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_update_task_update_returns_false(self, mock_get_api):
        """Test handling when update_task returns False."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.update_task.return_value = False

        result = await update_task("task_123", content="Updated content")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Update failed" in result_data["error"]

        mock_api.update_task.assert_called_once_with(
            task_id="task_123",
            content="Updated content"
        )
        # get_task should not be called if update failed
        mock_api.get_task.assert_not_called()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_update_task_get_task_error(self, mock_get_api):
        """Test error handling when get_task fails after successful update."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.update_task.return_value = True
        mock_api.get_task.side_effect = Exception("Failed to retrieve updated task")

        result = await update_task("task_123", content="Updated content")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Failed to retrieve updated task" in result_data["error"]

        mock_api.update_task.assert_called_once()
        mock_api.get_task.assert_called_once_with(task_id="task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_task_to_dict_error(self, mock_task_to_dict, mock_get_api):
        """Test error handling when task_to_dict fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.side_effect = Exception("Task serialization error")

        result = await update_task("task_123", content="Updated content")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task serialization error" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_parameter_filtering(self, mock_task_to_dict, mock_get_api):
        """Test that None parameters are filtered out correctly."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "filter_test_task",
            "content": "Updated content only"
        }

        # Pass some None values that should be filtered out
        result = await update_task(
            task_id="filter_test_task",
            content="Updated content only",
            description=None,  # Should be filtered out
            labels=None,  # Should be filtered out
            priority=None  # Should be filtered out
        )

        result_data = json.loads(result)
        assert result_data["success"]

        # Verify only non-None parameters were passed to API
        mock_api.update_task.assert_called_once_with(
            task_id="filter_test_task",
            content="Updated content only"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_all_parameters_none_except_task_id(self, mock_task_to_dict, mock_get_api):
        """Test that providing only None parameters (except task_id) returns error."""
        result = await update_task(
            task_id="task_123",
            content=None,
            description=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

        result_data = json.loads(result)
        assert "error" in result_data
        assert "No update parameters provided" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_return_type(self, mock_task_to_dict, mock_get_api):
        """Test that update_task returns a string (JSON)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {"id": "return_type_test", "content": "Test"}

        result = await update_task("return_type_test", content="Updated content")

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_json_structure(self, mock_task_to_dict, mock_get_api):
        """Test that the JSON output has the correct structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "structure_test",
            "content": "Structural test task"
        }

        result = await update_task("structure_test", content="Updated content")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "success" in result_data
        assert "task" in result_data
        assert result_data["success"]
        assert isinstance(result_data["task"], dict)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_update_task_comprehensive_scenario(self, mock_task_to_dict, mock_get_api):
        """Test a comprehensive real-world update scenario."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.update_task.return_value = True
        mock_updated_task = Mock(spec=Task)
        mock_api.get_task.return_value = mock_updated_task

        mock_task_to_dict.return_value = {
            "id": "comprehensive_task",
            "content": "Complete quarterly business review",
            "description": "Prepare comprehensive analysis including financial metrics, team performance, and strategic recommendations for Q4 planning session",
            "priority": 4,
            "labels": ["quarterly", "business", "urgent", "presentation"],
            "due": {"datetime": "2023-12-31T16:00:00Z"},
            "assignee_id": "senior_manager_123"
        }

        result = await update_task(
            task_id="comprehensive_task",
            content="Complete quarterly business review",
            description="Prepare comprehensive analysis including financial metrics, team performance, and strategic recommendations for Q4 planning session",
            priority=4,
            labels=["quarterly", "business", "urgent", "presentation"],
            due_datetime="2023-12-31T16:00:00Z",
            assignee_id="senior_manager_123"
        )

        result_data = json.loads(result)
        assert result_data["success"]
        assert result_data["task"]["content"] == "Complete quarterly business review"
        assert result_data["task"]["priority"] == 4
        assert len(result_data["task"]["labels"]) == 4
        assert result_data["task"]["assignee_id"] == "senior_manager_123"

        mock_api.update_task.assert_called_once_with(
            task_id="comprehensive_task",
            content="Complete quarterly business review",
            description="Prepare comprehensive analysis including financial metrics, team performance, and strategic recommendations for Q4 planning session",
            priority=4,
            labels=["quarterly", "business", "urgent", "presentation"],
            due_datetime="2023-12-31T16:00:00Z",
            assignee_id="senior_manager_123"
        )
