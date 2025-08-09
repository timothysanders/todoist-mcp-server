from unittest.mock import Mock
from todoist_mcp_server import task_to_dict, project_to_dict, label_to_dict
from todoist_api_python.models import Task, Project, Label


class TestToDictFunctions:
    """Unit tests for task_to_dict, project_to_dict, and label_to_dict functions."""

    # =============================================================================
    # TASK_TO_DICT TESTS
    # =============================================================================

    def test_task_to_dict_success_all_fields(self):
        """Test task_to_dict with all fields populated."""
        mock_task = Mock(spec=Task)
        mock_task.id = "123456789"
        mock_task.content = "Complete project report"
        mock_task.description = "Write the quarterly project report with all metrics"
        mock_task.is_completed = False
        mock_task.priority = 3
        mock_task.project_id = "project_123"
        mock_task.section_id = "section_456"
        mock_task.parent_id = "parent_789"
        mock_task.order = 5
        mock_task.labels = ["work", "urgent"]
        mock_task.url = "https://todoist.com/showTask?id=123456789"
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.creator_id = "user_123"
        mock_task.assignee_id = "user_456"
        mock_task.assigner_id = "user_789"

        # Mock due object with to_dict method
        mock_due = Mock()
        mock_due.to_dict.return_value = {
            "date": "2023-12-31",
            "datetime": "2023-12-31T23:59:59Z",
            "string": "Dec 31",
            "timezone": "UTC"
        }
        mock_task.due = mock_due

        result = task_to_dict(mock_task)

        expected = {
            "id": "123456789",
            "content": "Complete project report",
            "description": "Write the quarterly project report with all metrics",
            "is_completed": False,
            "priority": 3,
            "project_id": "project_123",
            "section_id": "section_456",
            "parent_id": "parent_789",
            "order": 5,
            "labels": ["work", "urgent"],
            "due": {
                "date": "2023-12-31",
                "datetime": "2023-12-31T23:59:59Z",
                "string": "Dec 31",
                "timezone": "UTC"
            },
            "url": "https://todoist.com/showTask?id=123456789",
            "created_at": "2023-01-01T00:00:00Z",
            "creator_id": "user_123",
            "assignee_id": "user_456",
            "assigner_id": "user_789"
        }

        assert result == expected
        mock_due.to_dict.assert_called_once()

    def test_task_to_dict_success_minimal_fields(self):
        """Test task_to_dict with minimal required fields."""
        mock_task = Mock(spec=Task)
        mock_task.id = "123"
        mock_task.content = "Simple task"
        mock_task.description = None
        mock_task.is_completed = False
        mock_task.priority = 1
        mock_task.project_id = None
        mock_task.section_id = None
        mock_task.parent_id = None
        mock_task.order = 0
        mock_task.labels = []
        mock_task.due = None
        mock_task.url = "https://todoist.com/showTask?id=123"
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.creator_id = "user_123"
        mock_task.assignee_id = None
        mock_task.assigner_id = None

        result = task_to_dict(mock_task)

        expected = {
            "id": "123",
            "content": "Simple task",
            "description": None,
            "is_completed": False,
            "priority": 1,
            "project_id": None,
            "section_id": None,
            "parent_id": None,
            "order": 0,
            "labels": [],
            "due": None,
            "url": "https://todoist.com/showTask?id=123",
            "created_at": "2023-01-01T00:00:00Z",
            "creator_id": "user_123",
            "assignee_id": None,
            "assigner_id": None
        }

        assert result == expected

    def test_task_to_dict_completed_task(self):
        """Test task_to_dict with a completed task."""
        mock_task = Mock(spec=Task)
        mock_task.id = "completed_123"
        mock_task.content = "Finished task"
        mock_task.description = "This task is done"
        mock_task.is_completed = True
        mock_task.priority = 1
        mock_task.project_id = "project_123"
        mock_task.section_id = None
        mock_task.parent_id = None
        mock_task.order = 1
        mock_task.labels = ["completed"]
        mock_task.due = None
        mock_task.url = "https://todoist.com/showTask?id=completed_123"
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.creator_id = "user_123"
        mock_task.assignee_id = "user_123"
        mock_task.assigner_id = "user_123"

        result = task_to_dict(mock_task)

        assert result["is_completed"]
        assert result["content"] == "Finished task"
        assert result["labels"] == ["completed"]

    def test_task_to_dict_with_unicode_content(self):
        """Test task_to_dict with unicode characters in content and description."""
        mock_task = Mock(spec=Task)
        mock_task.id = "unicode_123"
        mock_task.content = "Tâche avec caractères spéciaux 🎯"
        mock_task.description = "Description avec émojis 📝 et caractères accentués"
        mock_task.is_completed = False
        mock_task.priority = 2
        mock_task.project_id = "project_123"
        mock_task.section_id = None
        mock_task.parent_id = None
        mock_task.order = 1
        mock_task.labels = ["français", "测试"]
        mock_task.due = None
        mock_task.url = "https://todoist.com/showTask?id=unicode_123"
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.creator_id = "user_123"
        mock_task.assignee_id = None
        mock_task.assigner_id = None

        result = task_to_dict(mock_task)

        assert result["content"] == "Tâche avec caractères spéciaux 🎯"
        assert result["description"] == "Description avec émojis 📝 et caractères accentués"
        assert result["labels"] == ["français", "测试"]

    def test_task_to_dict_due_none(self):
        """Test task_to_dict when due is None."""
        mock_task = Mock(spec=Task)
        mock_task.id = "no_due_123"
        mock_task.content = "Task without due date"
        mock_task.description = None
        mock_task.is_completed = False
        mock_task.priority = 1
        mock_task.project_id = None
        mock_task.section_id = None
        mock_task.parent_id = None
        mock_task.order = 0
        mock_task.labels = []
        mock_task.due = None
        mock_task.url = "https://todoist.com/showTask?id=no_due_123"
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.creator_id = "user_123"
        mock_task.assignee_id = None
        mock_task.assigner_id = None

        result = task_to_dict(mock_task)

        assert result["due"] is None

    def test_task_to_dict_high_priority(self):
        """Test task_to_dict with high priority task."""
        mock_task = Mock(spec=Task)
        mock_task.id = "urgent_123"
        mock_task.content = "Urgent task"
        mock_task.description = "This needs immediate attention"
        mock_task.is_completed = False
        mock_task.priority = 4
        mock_task.project_id = "project_123"
        mock_task.section_id = "urgent_section"
        mock_task.parent_id = None
        mock_task.order = 1
        mock_task.labels = ["urgent", "critical"]
        mock_task.due = None
        mock_task.url = "https://todoist.com/showTask?id=urgent_123"
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.creator_id = "user_123"
        mock_task.assignee_id = "user_456"
        mock_task.assigner_id = "user_123"

        result = task_to_dict(mock_task)

        assert result["priority"] == 4
        assert result["labels"] == ["urgent", "critical"]
        assert result["section_id"] == "urgent_section"

    # =============================================================================
    # PROJECT_TO_DICT TESTS
    # =============================================================================

    def test_project_to_dict_success_all_fields(self):
        """Test project_to_dict with all fields populated."""
        mock_project = Mock(spec=Project)
        mock_project.id = "project_123456"
        mock_project.name = "Work Project"
        mock_project.order = 3
        mock_project.color = "red"
        mock_project.is_shared = True
        mock_project.is_favorite = False
        mock_project.is_inbox_project = False
        mock_project.view_style = "list"
        mock_project.url = "https://todoist.com/showProject?id=project_123456"
        mock_project.parent_id = "parent_project_789"

        result = project_to_dict(mock_project)

        expected = {
            "id": "project_123456",
            "name": "Work Project",
            "order": 3,
            "color": "red",
            "is_shared": True,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "list",
            "url": "https://todoist.com/showProject?id=project_123456",
            "parent_id": "parent_project_789"
        }

        assert result == expected

    def test_project_to_dict_success_inbox_project(self):
        """Test project_to_dict with inbox project."""
        mock_project = Mock(spec=Project)
        mock_project.id = "inbox_123"
        mock_project.name = "Inbox"
        mock_project.order = 0
        mock_project.color = "grey"
        mock_project.is_shared = False
        mock_project.is_favorite = True
        mock_project.is_inbox_project = True
        mock_project.view_style = "list"
        mock_project.url = "https://todoist.com/showProject?id=inbox_123"
        mock_project.parent_id = None

        result = project_to_dict(mock_project)

        assert result["name"] == "Inbox"
        assert result["is_inbox_project"]
        assert result["is_favorite"]
        assert result["parent_id"] is None

    def test_project_to_dict_shared_project(self):
        """Test project_to_dict with shared project."""
        mock_project = Mock(spec=Project)
        mock_project.id = "shared_456"
        mock_project.name = "Team Project"
        mock_project.order = 5
        mock_project.color = "blue"
        mock_project.is_shared = True
        mock_project.is_favorite = False
        mock_project.is_inbox_project = False
        mock_project.view_style = "board"
        mock_project.url = "https://todoist.com/showProject?id=shared_456"
        mock_project.parent_id = None

        result = project_to_dict(mock_project)

        assert result["is_shared"]
        assert result["view_style"] == "board"
        assert result["color"] == "blue"

    def test_project_to_dict_with_unicode_name(self):
        """Test project_to_dict with unicode characters in name."""
        mock_project = Mock(spec=Project)
        mock_project.id = "unicode_789"
        mock_project.name = "Projet français 🇫🇷 与中文 название"
        mock_project.order = 2
        mock_project.color = "green"
        mock_project.is_shared = False
        mock_project.is_favorite = True
        mock_project.is_inbox_project = False
        mock_project.view_style = "list"
        mock_project.url = "https://todoist.com/showProject?id=unicode_789"
        mock_project.parent_id = None

        result = project_to_dict(mock_project)

        assert result["name"] == "Projet français 🇫🇷 与中文 название"
        assert result["is_favorite"]

    def test_project_to_dict_subproject(self):
        """Test project_to_dict with subproject (has parent_id)."""
        mock_project = Mock(spec=Project)
        mock_project.id = "sub_123"
        mock_project.name = "Subproject"
        mock_project.order = 1
        mock_project.color = "purple"
        mock_project.is_shared = False
        mock_project.is_favorite = False
        mock_project.is_inbox_project = False
        mock_project.view_style = "list"
        mock_project.url = "https://todoist.com/showProject?id=sub_123"
        mock_project.parent_id = "parent_456"

        result = project_to_dict(mock_project)

        assert result["parent_id"] == "parent_456"
        assert result["name"] == "Subproject"

    def test_project_to_dict_all_view_styles(self):
        """Test project_to_dict with different view styles."""
        view_styles = ["list", "board"]

        for view_style in view_styles:
            mock_project = Mock(spec=Project)
            mock_project.id = f"project_{view_style}"
            mock_project.name = f"Project {view_style}"
            mock_project.order = 1
            mock_project.color = "blue"
            mock_project.is_shared = False
            mock_project.is_favorite = False
            mock_project.is_inbox_project = False
            mock_project.view_style = view_style
            mock_project.url = f"https://todoist.com/showProject?id=project_{view_style}"
            mock_project.parent_id = None

            result = project_to_dict(mock_project)

            assert result["view_style"] == view_style

    # =============================================================================
    # LABEL_TO_DICT TESTS
    # =============================================================================

    def test_label_to_dict_success_all_fields(self):
        """Test label_to_dict with all fields populated."""
        mock_label = Mock(spec=Label)
        mock_label.id = "label_123456"
        mock_label.name = "work"
        mock_label.color = "blue"
        mock_label.order = 3
        mock_label.is_favorite = True

        result = label_to_dict(mock_label)

        expected = {
            "id": "label_123456",
            "name": "work",
            "color": "blue",
            "order": 3,
            "is_favorite": True
        }

        assert result == expected

    def test_label_to_dict_success_not_favorite(self):
        """Test label_to_dict with non-favorite label."""
        mock_label = Mock(spec=Label)
        mock_label.id = "label_789"
        mock_label.name = "personal"
        mock_label.color = "green"
        mock_label.order = 1
        mock_label.is_favorite = False

        result = label_to_dict(mock_label)

        assert result["name"] == "personal"
        assert not result["is_favorite"]
        assert result["color"] == "green"

    def test_label_to_dict_with_special_characters(self):
        """Test label_to_dict with special characters in name."""
        mock_label = Mock(spec=Label)
        mock_label.id = "label_special"
        mock_label.name = "@home-urgent_task"
        mock_label.color = "red"
        mock_label.order = 5
        mock_label.is_favorite = False

        result = label_to_dict(mock_label)

        assert result["name"] == "@home-urgent_task"

    def test_label_to_dict_with_unicode_name(self):
        """Test label_to_dict with unicode characters in name."""
        mock_label = Mock(spec=Label)
        mock_label.id = "label_unicode"
        mock_label.name = "重要 🔥 срочно"
        mock_label.color = "orange"
        mock_label.order = 2
        mock_label.is_favorite = True

        result = label_to_dict(mock_label)

        assert result["name"] == "重要 🔥 срочно"
        assert result["is_favorite"]

    def test_label_to_dict_various_colors(self):
        """Test label_to_dict with different color values."""
        colors = ["red", "blue", "green", "yellow", "orange", "purple", "grey"]

        for color in colors:
            mock_label = Mock(spec=Label)
            mock_label.id = f"label_{color}"
            mock_label.name = f"{color}_label"
            mock_label.color = color
            mock_label.order = 1
            mock_label.is_favorite = False

            result = label_to_dict(mock_label)

            assert result["color"] == color
            assert result["name"] == f"{color}_label"

    def test_label_to_dict_order_variations(self):
        """Test label_to_dict with different order values."""
        for order in [0, 1, 5, 10, 100]:
            mock_label = Mock(spec=Label)
            mock_label.id = f"label_order_{order}"
            mock_label.name = f"label_{order}"
            mock_label.color = "blue"
            mock_label.order = order
            mock_label.is_favorite = False

            result = label_to_dict(mock_label)

            assert result["order"] == order

    def test_label_to_dict_common_label_patterns(self):
        """Test label_to_dict with common label naming patterns."""
        common_patterns = [
            "@home",
            "@work",
            "@errands",
            "high-priority",
            "waiting_for",
            "someday_maybe",
            "project:work",
            "context:computer"
        ]

        for pattern in common_patterns:
            mock_label = Mock(spec=Label)
            mock_label.id = f"label_{pattern.replace('@', '').replace(':', '_')}"
            mock_label.name = pattern
            mock_label.color = "blue"
            mock_label.order = 1
            mock_label.is_favorite = False

            result = label_to_dict(mock_label)

            assert result["name"] == pattern

    # =============================================================================
    # EDGE CASES AND ERROR SCENARIOS
    # =============================================================================

    def test_task_to_dict_return_type(self):
        """Test that task_to_dict returns a dictionary."""
        mock_task = Mock(spec=Task)
        mock_task.id = "123"
        mock_task.content = "Test"
        mock_task.description = None
        mock_task.is_completed = False
        mock_task.priority = 1
        mock_task.project_id = None
        mock_task.section_id = None
        mock_task.parent_id = None
        mock_task.order = 0
        mock_task.labels = []
        mock_task.due = None
        mock_task.url = "https://todoist.com"
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.creator_id = "user_123"
        mock_task.assignee_id = None
        mock_task.assigner_id = None

        result = task_to_dict(mock_task)

        assert isinstance(result, dict)
        assert len(result) == 16  # All expected fields

    def test_project_to_dict_return_type(self):
        """Test that project_to_dict returns a dictionary."""
        mock_project = Mock(spec=Project)
        mock_project.id = "123"
        mock_project.name = "Test"
        mock_project.order = 1
        mock_project.color = "blue"
        mock_project.is_shared = False
        mock_project.is_favorite = False
        mock_project.is_inbox_project = False
        mock_project.view_style = "list"
        mock_project.url = "https://todoist.com"
        mock_project.parent_id = None

        result = project_to_dict(mock_project)

        assert isinstance(result, dict)
        assert len(result) == 10  # All expected fields

    def test_label_to_dict_return_type(self):
        """Test that label_to_dict returns a dictionary."""
        mock_label = Mock(spec=Label)
        mock_label.id = "123"
        mock_label.name = "test"
        mock_label.color = "blue"
        mock_label.order = 1
        mock_label.is_favorite = False

        result = label_to_dict(mock_label)

        assert isinstance(result, dict)
        assert len(result) == 5  # All expected fields

    def test_all_functions_with_empty_string_values(self):
        """Test all functions handle empty string values correctly."""
        mock_task = Mock(spec=Task)
        mock_task.id = ""
        mock_task.content = ""
        mock_task.description = ""
        mock_task.is_completed = False
        mock_task.priority = 1
        mock_task.project_id = ""
        mock_task.section_id = ""
        mock_task.parent_id = ""
        mock_task.order = 0
        mock_task.labels = []
        mock_task.due = None
        mock_task.url = ""
        mock_task.created_at = ""
        mock_task.creator_id = ""
        mock_task.assignee_id = ""
        mock_task.assigner_id = ""

        task_result = task_to_dict(mock_task)
        assert task_result["id"] == ""
        assert task_result["content"] == ""

        mock_project = Mock(spec=Project)
        mock_project.id = ""
        mock_project.name = ""
        mock_project.order = 0
        mock_project.color = ""
        mock_project.is_shared = False
        mock_project.is_favorite = False
        mock_project.is_inbox_project = False
        mock_project.view_style = ""
        mock_project.url = ""
        mock_project.parent_id = ""

        project_result = project_to_dict(mock_project)
        assert project_result["name"] == ""

        mock_label = Mock(spec=Label)
        mock_label.id = ""
        mock_label.name = ""
        mock_label.color = ""
        mock_label.order = 0
        mock_label.is_favorite = False

        label_result = label_to_dict(mock_label)
        assert label_result["name"] == ""
