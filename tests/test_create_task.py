import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import create_task
from todoist_api_python.models import Task


@pytest.fixture
def mock_task():
    return Mock(spec=Task)

class TestCreateTask:
    """Unit tests for create_task function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_success_minimal(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with minimal parameters (content only)."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "123456789"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "123456789",
            "content": "Buy groceries",
            "description": None,
            "is_completed": False,
            "priority": 1,
            "project_id": None,
            "labels": [],
            "due": None
        }

        result = await create_task("Buy groceries")

        result_data = json.loads(result)
        assert result_data["id"] == "123456789"
        assert result_data["content"] == "Buy groceries"

        mock_api.add_task.assert_called_once_with(
            content="Buy groceries",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )
        mock_task_to_dict.assert_called_once_with(mock_task)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_success_all_parameters(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with all parameters specified."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "full_task_123"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "full_task_123",
            "content": "Complete project report",
            "description": "Write comprehensive quarterly report",
            "is_completed": False,
            "priority": 3,
            "project_id": "project_456",
            "section_id": "section_789",
            "parent_id": "parent_123",
            "order": 5,
            "labels": ["work", "urgent"],
            "due": {"date": "2023-12-31"},
            "assignee_id": "user_789"
        }

        result = await create_task(
            content="Complete project report",
            description="Write comprehensive quarterly report",
            project_id="project_456",
            section_id="section_789",
            parent_id="parent_123",
            order=5,
            labels=["work", "urgent"],
            priority=3,
            due_string="December 31st",
            due_date="2023-12-31",
            due_datetime="2023-12-31T23:59:59Z",
            due_lang="en",
            assignee_id="user_789"
        )

        result_data = json.loads(result)
        assert result_data["id"] == "full_task_123"
        assert result_data["content"] == "Complete project report"
        assert result_data["priority"] == 3
        assert result_data["labels"] == ["work", "urgent"]

        mock_api.add_task.assert_called_once_with(
            content="Complete project report",
            description="Write comprehensive quarterly report",
            project_id="project_456",
            section_id="section_789",
            parent_id="parent_123",
            order=5,
            labels=["work", "urgent"],
            priority=3,
            due_string="December 31st",
            due_date="2023-12-31",
            due_datetime="2023-12-31T23:59:59Z",
            due_lang="en",
            assignee_id="user_789"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_description(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with description."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "desc_task_123"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "desc_task_123",
            "content": "Plan vacation",
            "description": "Research destinations, book flights, and reserve hotels",
            "is_completed": False
        }

        result = await create_task(
            content="Plan vacation",
            description="Research destinations, book flights, and reserve hotels"
        )

        result_data = json.loads(result)
        assert result_data["content"] == "Plan vacation"
        assert result_data["description"] == "Research destinations, book flights, and reserve hotels"

        mock_api.add_task.assert_called_once_with(
            content="Plan vacation",
            description="Research destinations, book flights, and reserve hotels",
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_project_and_section(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with project and section IDs."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "proj_task_456"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "proj_task_456",
            "content": "Review code",
            "project_id": "work_project_123",
            "section_id": "code_review_section"
        }

        result = await create_task(
            content="Review code",
            project_id="work_project_123",
            section_id="code_review_section"
        )

        result_data = json.loads(result)
        assert result_data["project_id"] == "work_project_123"
        assert result_data["section_id"] == "code_review_section"

        mock_api.add_task.assert_called_once_with(
            content="Review code",
            description=None,
            project_id="work_project_123",
            section_id="code_review_section",
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_priority_levels(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating tasks with different priority levels."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        priorities = [1, 2, 3, 4]
        priority_names = ["normal", "high", "very high", "urgent"]

        for priority, name in zip(priorities, priority_names):
            mock_task.id = f"priority_{priority}_task"
            mock_api.add_task.return_value = mock_task

            mock_task_to_dict.return_value = {
                "id": f"priority_{priority}_task",
                "content": f"Task with {name} priority",
                "priority": priority
            }

            result = await create_task(
                content=f"Task with {name} priority",
                priority=priority
            )

            result_data = json.loads(result)
            assert result_data["priority"] == priority

            # Reset mock for next iteration
            mock_api.add_task.reset_mock()
            mock_task_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_labels(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with multiple labels."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "labeled_task_789"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "labeled_task_789",
            "content": "Important meeting",
            "labels": ["work", "urgent", "meeting"]
        }

        result = await create_task(
            content="Important meeting",
            labels=["work", "urgent", "meeting"]
        )

        result_data = json.loads(result)
        assert result_data["labels"] == ["work", "urgent", "meeting"]

        mock_api.add_task.assert_called_once_with(
            content="Important meeting",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=["work", "urgent", "meeting"],
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_due_string(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with natural language due date."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "due_string_task"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "due_string_task",
            "content": "Submit report",
            "due": {"string": "tomorrow", "date": "2023-12-25"}
        }

        result = await create_task(
            content="Submit report",
            due_string="tomorrow"
        )

        result_data = json.loads(result)
        assert result_data["due"]["string"] == "tomorrow"

        mock_api.add_task.assert_called_once_with(
            content="Submit report",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string="tomorrow",
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_due_date(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with specific due date."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "due_date_task"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "due_date_task",
            "content": "Annual review",
            "due": {"date": "2023-12-31"}
        }

        result = await create_task(
            content="Annual review",
            due_date="2023-12-31"
        )

        result_data = json.loads(result)
        assert result_data["due"]["date"] == "2023-12-31"

        mock_api.add_task.assert_called_once_with(
            content="Annual review",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date="2023-12-31",
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_due_datetime(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with specific due datetime."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "due_datetime_task"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "due_datetime_task",
            "content": "Conference call",
            "due": {"datetime": "2023-12-25T14:30:00Z"}
        }

        result = await create_task(
            content="Conference call",
            due_datetime="2023-12-25T14:30:00Z"
        )

        result_data = json.loads(result)
        assert result_data["due"]["datetime"] == "2023-12-25T14:30:00Z"

        mock_api.add_task.assert_called_once_with(
            content="Conference call",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime="2023-12-25T14:30:00Z",
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_due_lang(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with due string in different language."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "due_lang_task"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "due_lang_task",
            "content": "Réunion importante",
            "due": {"string": "demain", "date": "2023-12-25"}
        }

        result = await create_task(
            content="Réunion importante",
            due_string="demain",
            due_lang="fr"
        )

        result_data = json.loads(result)
        assert result_data["content"] == "Réunion importante"

        mock_api.add_task.assert_called_once_with(
            content="Réunion importante",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string="demain",
            due_date=None,
            due_datetime=None,
            due_lang="fr",
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_subtask(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a subtask with parent_id."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "subtask_123"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "subtask_123",
            "content": "Research vendors",
            "parent_id": "parent_task_456"
        }

        result = await create_task(
            content="Research vendors",
            parent_id="parent_task_456"
        )

        result_data = json.loads(result)
        assert result_data["parent_id"] == "parent_task_456"

        mock_api.add_task.assert_called_once_with(
            content="Research vendors",
            description=None,
            project_id=None,
            section_id=None,
            parent_id="parent_task_456",
            order=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_assignee(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with assignee."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "assigned_task_789"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "assigned_task_789",
            "content": "Team presentation",
            "assignee_id": "team_member_123"
        }

        result = await create_task(
            content="Team presentation",
            assignee_id="team_member_123"
        )

        result_data = json.loads(result)
        assert result_data["assignee_id"] == "team_member_123"

        mock_api.add_task.assert_called_once_with(
            content="Team presentation",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id="team_member_123"
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_order(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with specific order."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "ordered_task_456"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "ordered_task_456",
            "content": "First priority task",
            "order": 1
        }

        result = await create_task(
            content="First priority task",
            order=1
        )

        result_data = json.loads(result)
        assert result_data["order"] == 1

        mock_api.add_task.assert_called_once_with(
            content="First priority task",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=1,
            labels=None,
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_with_unicode_content(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with unicode characters in content and description."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "unicode_task_123"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "unicode_task_123",
            "content": "Tâche importante 🎯",
            "description": "Description avec émojis 📝 et caractères spéciaux",
            "labels": ["français", "测试"]
        }

        result = await create_task(
            content="Tâche importante 🎯",
            description="Description avec émojis 📝 et caractères spéciaux",
            labels=["français", "测试"]
        )

        result_data = json.loads(result)
        assert result_data["content"] == "Tâche importante 🎯"
        assert result_data["description"] == "Description avec émojis 📝 et caractères spéciaux"
        assert result_data["labels"] == ["français", "测试"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_task_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await create_task("Test task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_task_api_call_error(self, mock_get_api):
        """Test error handling when API call fails."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.add_task.side_effect = Exception("Todoist API error: invalid project")

        result = await create_task("Test task", project_id="invalid_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error: invalid project" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_task_to_dict_error(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test error handling when task_to_dict fails."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "123"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.side_effect = Exception("Task serialization error")

        result = await create_task("Test task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task serialization error" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_empty_labels_list(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test creating a task with empty labels list."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "empty_labels_task"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "empty_labels_task",
            "content": "Task with empty labels",
            "labels": []
        }

        result = await create_task(
            content="Task with empty labels",
            labels=[]
        )

        result_data = json.loads(result)
        assert result_data["labels"] == []

        mock_api.add_task.assert_called_once_with(
            content="Task with empty labels",
            description=None,
            project_id=None,
            section_id=None,
            parent_id=None,
            order=None,
            labels=[],
            priority=None,
            due_string=None,
            due_date=None,
            due_datetime=None,
            due_lang=None,
            assignee_id=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_return_type(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test that create_task returns a string (JSON)."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "return_type_test"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {"id": "return_type_test", "content": "Test"}

        result = await create_task("Test task")

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.task_to_dict')
    async def test_create_task_json_formatting(self, mock_task_to_dict, mock_get_api, mock_task):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_task.id = "json_format_test"
        mock_api.add_task.return_value = mock_task

        mock_task_to_dict.return_value = {
            "id": "json_format_test",
            "content": "JSON format test",
            "description": "Testing JSON formatting"
        }

        result = await create_task("JSON format test", description="Testing JSON formatting")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert result_data["id"] == "json_format_test"
        assert result_data["content"] == "JSON format test"
