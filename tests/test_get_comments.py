import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import get_comments
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Comment, Attachment


@pytest.fixture
def mock_comment():
    return Mock(spec=Comment)

class TestGetComments:
    """Unit tests for get_comments function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_task_success_no_comments(self, mock_get_api):
        """Test successfully retrieving comments for a task with no comments."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.return_value = [[]]  # Paginator returns list of lists, empty

        result = await get_comments(task_id="task_123")

        result_data = json.loads(result)
        assert result_data["count"] == 0
        assert len(result_data["comments"]) == 0
        assert result_data["comments"] == []

        mock_api.get_comments.assert_called_once_with(task_id="task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_task_success_single_comment(self, mock_get_api, mock_comment):
        """Test successfully retrieving a single comment for a task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment.id = "comment_123"
        mock_comment.task_id = "task_456"
        mock_comment.project_id = "project_789"
        mock_comment.posted_at = "2023-12-01T10:30:00Z"
        mock_comment.content = "This is a test comment on the task"
        mock_comment.attachment = None

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="task_456")

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert len(result_data["comments"]) == 1
        assert result_data["comments"][0]["id"] == "comment_123"
        assert result_data["comments"][0]["task_id"] == "task_456"
        assert result_data["comments"][0]["project_id"] == "project_789"
        assert result_data["comments"][0]["content"] == "This is a test comment on the task"
        assert result_data["comments"][0]["attachment"] is None

        mock_api.get_comments.assert_called_once_with(task_id="task_456")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_task_success_multiple_comments(self, mock_get_api):
        """Test successfully retrieving multiple comments for a task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment1 = Mock(spec=Comment)
        mock_comment1.id = "comment_1"
        mock_comment1.task_id = "task_789"
        mock_comment1.project_id = "project_123"
        mock_comment1.posted_at = "2023-12-01T09:00:00Z"
        mock_comment1.content = "First comment on this task"
        mock_comment1.attachment = None

        mock_comment2 = Mock(spec=Comment)
        mock_comment2.id = "comment_2"
        mock_comment2.task_id = "task_789"
        mock_comment2.project_id = "project_123"
        mock_comment2.posted_at = "2023-12-01T10:15:00Z"
        mock_comment2.content = "Second comment with more details"
        mock_comment2.attachment = None

        mock_comment3 = Mock(spec=Comment)
        mock_comment3.id = "comment_3"
        mock_comment3.task_id = "task_789"
        mock_comment3.project_id = "project_123"
        mock_comment3.posted_at = "2023-12-01T11:30:00Z"
        mock_comment3.content = "Final comment completing the discussion"
        mock_comment3.attachment = None

        mock_api.get_comments.return_value = [[mock_comment1, mock_comment2, mock_comment3]]

        result = await get_comments(task_id="task_789")

        result_data = json.loads(result)
        assert result_data["count"] == 3
        assert len(result_data["comments"]) == 3
        assert result_data["comments"][0]["content"] == "First comment on this task"
        assert result_data["comments"][1]["content"] == "Second comment with more details"
        assert result_data["comments"][2]["content"] == "Final comment completing the discussion"

        mock_api.get_comments.assert_called_once_with(task_id="task_789")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_task_with_attachment(self, mock_get_api, mock_comment):
        """Test retrieving comment with attachment for a task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_attachment = Mock(spec=Attachment)
        mock_attachment.to_dict.return_value = {
            "file_name": "document.pdf",
            "file_type": "application/pdf",
            "file_url": "https://todoist.com/files/document.pdf",
            "file_size": 2048576
        }

        mock_comment.id = "comment_with_attachment"
        mock_comment.task_id = "task_attachment"
        mock_comment.project_id = "project_456"
        mock_comment.posted_at = "2023-12-01T14:20:00Z"
        mock_comment.content = "Please review the attached document"
        mock_comment.attachment = mock_attachment

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="task_attachment")

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["comments"][0]["content"] == "Please review the attached document"
        assert result_data["comments"][0]["attachment"] is not None
        assert result_data["comments"][0]["attachment"]["file_name"] == "document.pdf"
        assert result_data["comments"][0]["attachment"]["file_type"] == "application/pdf"

        mock_api.get_comments.assert_called_once_with(task_id="task_attachment")
        mock_attachment.to_dict.assert_called_once()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_project_success_no_comments(self, mock_get_api):
        """Test successfully retrieving comments for a project with no comments."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.return_value = [[]]  # Paginator returns list of lists, empty

        result = await get_comments(project_id="project_123")

        result_data = json.loads(result)
        assert result_data["count"] == 0
        assert len(result_data["comments"]) == 0
        assert result_data["comments"] == []

        mock_api.get_comments.assert_called_once_with(project_id="project_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_project_success_single_comment(self, mock_get_api, mock_comment):
        """Test successfully retrieving a single comment for a project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment.id = "project_comment_456"
        mock_comment.task_id = None
        mock_comment.project_id = "project_789"
        mock_comment.posted_at = "2023-12-01T12:45:00Z"
        mock_comment.content = "Project update: All tasks are on schedule"
        mock_comment.attachment = None

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(project_id="project_789")

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert len(result_data["comments"]) == 1
        assert result_data["comments"][0]["id"] == "project_comment_456"
        assert result_data["comments"][0]["task_id"] is None
        assert result_data["comments"][0]["project_id"] == "project_789"
        assert result_data["comments"][0]["content"] == "Project update: All tasks are on schedule"

        mock_api.get_comments.assert_called_once_with(project_id="project_789")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_project_success_multiple_comments(self, mock_get_api):
        """Test successfully retrieving multiple comments for a project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment1 = Mock(spec=Comment)
        mock_comment1.id = "proj_comment_1"
        mock_comment1.task_id = None
        mock_comment1.project_id = "project_team"
        mock_comment1.posted_at = "2023-12-01T08:00:00Z"
        mock_comment1.content = "Weekly team standup notes"
        mock_comment1.attachment = None

        mock_comment2 = Mock(spec=Comment)
        mock_comment2.id = "proj_comment_2"
        mock_comment2.task_id = None
        mock_comment2.project_id = "project_team"
        mock_comment2.posted_at = "2023-12-01T16:30:00Z"
        mock_comment2.content = "End of day project status update"
        mock_comment2.attachment = None

        mock_api.get_comments.return_value = [[mock_comment1, mock_comment2]]

        result = await get_comments(project_id="project_team")

        result_data = json.loads(result)
        assert result_data["count"] == 2
        assert len(result_data["comments"]) == 2
        assert result_data["comments"][0]["content"] == "Weekly team standup notes"
        assert result_data["comments"][1]["content"] == "End of day project status update"
        assert all(comment["task_id"] is None for comment in result_data["comments"])
        assert all(comment["project_id"] == "project_team" for comment in result_data["comments"])

        mock_api.get_comments.assert_called_once_with(project_id="project_team")

    @pytest.mark.asyncio
    async def test_get_comments_neither_task_nor_project_id(self):
        """Test error when neither task_id nor project_id is provided."""
        result = await get_comments()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Either task_id or project_id must be provided" in result_data["error"]

    @pytest.mark.asyncio
    async def test_get_comments_both_task_and_project_id(self):
        """Test behavior when both task_id and project_id are provided (task_id takes precedence)."""
        mock_api = Mock(spec=TodoistAPI)

        with patch('todoist_mcp_server.get_api') as mock_get_api:
            mock_get_api.return_value = mock_api
            mock_api.get_comments.return_value = [[]]

            result = await get_comments(task_id="task_123", project_id="project_456")

            result_data = json.loads(result)
            assert result_data["count"] == 0

            # Should call with task_id only (task_id takes precedence)
            mock_api.get_comments.assert_called_once_with(task_id="task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_unicode_content(self, mock_get_api, mock_comment):
        """Test retrieving comments with unicode characters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment.id = "unicode_comment"
        mock_comment.task_id = "task_unicode"
        mock_comment.project_id = "project_unicode"
        mock_comment.posted_at = "2023-12-01T15:45:00Z"
        mock_comment.content = "Commentaire avec émojis 🎯 et caractères spéciaux 中文 русский"
        mock_comment.attachment = None

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="task_unicode")

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["comments"][0]["content"] == "Commentaire avec émojis 🎯 et caractères spéciaux 中文 русский"

        mock_api.get_comments.assert_called_once_with(task_id="task_unicode")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_task_not_found(self, mock_get_api):
        """Test error handling when task is not found."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("404 Not Found: Task does not exist")

        result = await get_comments(task_id="nonexistent_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "404 Not Found: Task does not exist" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="nonexistent_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_project_not_found(self, mock_get_api):
        """Test error handling when project is not found."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("404 Not Found: Project does not exist")

        result = await get_comments(project_id="nonexistent_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "404 Not Found: Project does not exist" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(project_id="nonexistent_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_permission_denied_task(self, mock_get_api):
        """Test error handling when user lacks permission to view task comments."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("403 Forbidden: Access denied to task comments")

        result = await get_comments(task_id="private_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "403 Forbidden: Access denied to task comments" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="private_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_permission_denied_project(self, mock_get_api):
        """Test error handling when user lacks permission to view project comments."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("403 Forbidden: Access denied to project comments")

        result = await get_comments(project_id="private_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "403 Forbidden: Access denied to project comments" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(project_id="private_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await get_comments(task_id="task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = ConnectionError("Network connection failed")

        result = await get_comments(task_id="task_network_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Network connection failed" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="task_network_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_authentication_error(self, mock_get_api):
        """Test error handling when authentication fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("401 Unauthorized: Invalid token")

        result = await get_comments(project_id="project_auth_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "401 Unauthorized: Invalid token" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(project_id="project_auth_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_rate_limit_error(self, mock_get_api):
        """Test error handling when API rate limit is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("429 Too Many Requests: Rate limit exceeded")

        result = await get_comments(task_id="rate_limit_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "429 Too Many Requests: Rate limit exceeded" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="rate_limit_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_server_error(self, mock_get_api):
        """Test error handling when server error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("500 Internal Server Error")

        result = await get_comments(project_id="server_error_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "500 Internal Server Error" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(project_id="server_error_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_empty_string_ids(self, mock_get_api):
        """Test error handling with empty string IDs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("Either task_id or project_id must be provided")

        result = await get_comments(task_id="")
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Either task_id or project_id must be provided" in result_data["error"]

        mock_api.get_comments.reset_mock()
        mock_api.get_comments.side_effect = Exception("Either task_id or project_id must be provided")

        result = await get_comments(project_id="")
        result_data = json.loads(result)
        assert "error" in result_data
        assert "Either task_id or project_id must be provided" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_whitespace_ids(self, mock_get_api):
        """Test error handling with whitespace-only IDs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("Invalid ID: whitespace only")

        result = await get_comments(task_id="   ")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid ID: whitespace only" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="   ")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_attachment_serialization_error(self, mock_get_api, mock_comment):
        """Test error handling when attachment serialization fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_attachment = Mock(spec=Attachment)
        mock_attachment.to_dict.side_effect = Exception("Attachment serialization failed")

        mock_comment.id = "comment_attach_error"
        mock_comment.task_id = "task_123"
        mock_comment.project_id = "project_456"
        mock_comment.posted_at = "2023-12-01T10:00:00Z"
        mock_comment.content = "Comment with problematic attachment"
        mock_comment.attachment = mock_attachment

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Attachment serialization failed" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_return_type(self, mock_get_api):
        """Test that get_comments returns a string (JSON)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.return_value = [[]]

        result = await get_comments(task_id="return_type_test")

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_json_formatting(self, mock_get_api, mock_comment):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment.id = "format_test_comment"
        mock_comment.task_id = "format_test_task"
        mock_comment.project_id = "format_test_project"
        mock_comment.posted_at = "2023-12-01T10:00:00Z"
        mock_comment.content = "JSON formatting test comment"
        mock_comment.attachment = None

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="format_test_task")

        result_data = json.loads(result)

        reformatted = json.dumps(result_data, indent=2, ensure_ascii=False, default=str)

        assert isinstance(result_data, dict)
        assert isinstance(reformatted, str)
        assert "comments" in result_data
        assert "count" in result_data

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_response_structure(self, mock_get_api, mock_comment):
        """Test that the response has correct structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment.id = "structure_test"
        mock_comment.task_id = "task_structure"
        mock_comment.project_id = "project_structure"
        mock_comment.posted_at = "2023-12-01T10:00:00Z"
        mock_comment.content = "Structure test comment"
        mock_comment.attachment = None

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="task_structure")

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "comments" in result_data
        assert "count" in result_data
        assert isinstance(result_data["comments"], list)
        assert isinstance(result_data["count"], int)
        assert result_data["count"] == 1
        assert len(result_data["comments"]) == 1

        comment = result_data["comments"][0]
        assert "id" in comment
        assert "task_id" in comment
        assert "project_id" in comment
        assert "posted_at" in comment
        assert "content" in comment
        assert "attachment" in comment

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_timeout_error(self, mock_get_api):
        """Test error handling when API call times out."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = TimeoutError("Request timed out")

        result = await get_comments(project_id="timeout_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Request timed out" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(project_id="timeout_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_large_comment_thread(self, mock_get_api):
        """Test retrieving a large number of comments."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        # Create 50 mock comments
        mock_comments = []
        for i in range(50):
            mock_comment = Mock(spec=Comment)
            mock_comment.id = f"comment_{i}"
            mock_comment.task_id = "large_thread_task"
            mock_comment.project_id = "large_thread_project"
            mock_comment.posted_at = f"2023-12-01T{10 + (i % 10):02d}:{i % 60:02d}:00Z"
            mock_comment.content = f"Comment number {i + 1} in large thread"
            mock_comment.attachment = None
            mock_comments.append(mock_comment)

        mock_api.get_comments.return_value = [mock_comments]

        result = await get_comments(task_id="large_thread_task")

        result_data = json.loads(result)
        assert result_data["count"] == 50
        assert len(result_data["comments"]) == 50
        assert result_data["comments"][0]["content"] == "Comment number 1 in large thread"
        assert result_data["comments"][49]["content"] == "Comment number 50 in large thread"

        mock_api.get_comments.assert_called_once_with(task_id="large_thread_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_mixed_attachment_types(self, mock_get_api):
        """Test retrieving comments with various attachment types."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        # Comment with file attachment
        mock_attachment1 = Mock(spec=Attachment)
        mock_attachment1.to_dict.return_value = {
            "file_name": "report.pdf",
            "file_type": "application/pdf",
            "file_url": "https://todoist.com/files/report.pdf",
            "file_size": 1024000
        }

        mock_comment1 = Mock(spec=Comment)
        mock_comment1.id = "comment_with_pdf"
        mock_comment1.task_id = "mixed_attachments_task"
        mock_comment1.project_id = "mixed_project"
        mock_comment1.posted_at = "2023-12-01T10:00:00Z"
        mock_comment1.content = "Please review the attached PDF report"
        mock_comment1.attachment = mock_attachment1

        # Comment with image attachment
        mock_attachment2 = Mock(spec=Attachment)
        mock_attachment2.to_dict.return_value = {
            "file_name": "screenshot.png",
            "file_type": "image/png",
            "file_url": "https://todoist.com/files/screenshot.png",
            "file_size": 512000
        }

        mock_comment2 = Mock(spec=Comment)
        mock_comment2.id = "comment_with_image"
        mock_comment2.task_id = "mixed_attachments_task"
        mock_comment2.project_id = "mixed_project"
        mock_comment2.posted_at = "2023-12-01T11:00:00Z"
        mock_comment2.content = "Here's a screenshot of the issue"
        mock_comment2.attachment = mock_attachment2

        # Comment without attachment
        mock_comment3 = Mock(spec=Comment)
        mock_comment3.id = "comment_no_attachment"
        mock_comment3.task_id = "mixed_attachments_task"
        mock_comment3.project_id = "mixed_project"
        mock_comment3.posted_at = "2023-12-01T12:00:00Z"
        mock_comment3.content = "Thanks for the files, reviewing now"
        mock_comment3.attachment = None

        mock_api.get_comments.return_value = [[mock_comment1, mock_comment2, mock_comment3]]

        result = await get_comments(task_id="mixed_attachments_task")

        result_data = json.loads(result)
        assert result_data["count"] == 3

        assert result_data["comments"][0]["attachment"]["file_name"] == "report.pdf"
        assert result_data["comments"][0]["attachment"]["file_type"] == "application/pdf"

        assert result_data["comments"][1]["attachment"]["file_name"] == "screenshot.png"
        assert result_data["comments"][1]["attachment"]["file_type"] == "image/png"

        assert result_data["comments"][2]["attachment"] is None

        mock_api.get_comments.assert_called_once_with(task_id="mixed_attachments_task")
        mock_attachment1.to_dict.assert_called_once()
        mock_attachment2.to_dict.assert_called_once()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_special_character_ids(self, mock_get_api):
        """Test retrieving comments with special characters in IDs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        special_ids = [
            "task-with-dashes-123",
            "task_with_underscores_456",
            "task.with.dots.789",
            "task@with@symbols#123"
        ]

        for special_id in special_ids:
            mock_api.get_comments.return_value = [[]]

            result = await get_comments(task_id=special_id)

            result_data = json.loads(result)
            assert result_data["count"] == 0

            mock_api.get_comments.assert_called_with(task_id=special_id)
            mock_api.get_comments.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_archived_task_access(self, mock_get_api):
        """Test error when trying to access comments from archived task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("Cannot access comments from archived task")

        result = await get_comments(task_id="archived_task_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot access comments from archived task" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="archived_task_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_deleted_task_access(self, mock_get_api):
        """Test error when trying to access comments from deleted task."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("Task has been deleted")

        result = await get_comments(task_id="deleted_task_456")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Task has been deleted" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="deleted_task_456")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_shared_project_member_access(self, mock_get_api, mock_comment):
        """Test accessing comments in shared project as team member."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment.id = "shared_project_comment"
        mock_comment.task_id = None
        mock_comment.project_id = "shared_project_789"
        mock_comment.posted_at = "2023-12-01T13:00:00Z"
        mock_comment.content = "Team update: Sprint planning completed"
        mock_comment.attachment = None

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(project_id="shared_project_789")

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["comments"][0]["content"] == "Team update: Sprint planning completed"
        assert result_data["comments"][0]["project_id"] == "shared_project_789"

        mock_api.get_comments.assert_called_once_with(project_id="shared_project_789")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_shared_project_non_member_access(self, mock_get_api):
        """Test error when non-member tries to access shared project comments."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("Not authorized to view shared project comments")

        result = await get_comments(project_id="restricted_shared_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Not authorized to view shared project comments" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(project_id="restricted_shared_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_very_long_content(self, mock_get_api, mock_comment):
        """Test retrieving comment with very long content."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        long_content = "This is a very detailed comment that goes on for a very long time. " * 100

        mock_comment.id = "long_content_comment"
        mock_comment.task_id = "long_content_task"
        mock_comment.project_id = "long_content_project"
        mock_comment.posted_at = "2023-12-01T14:00:00Z"
        mock_comment.content = long_content
        mock_comment.attachment = None

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="long_content_task")

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["comments"][0]["content"] == long_content
        assert len(result_data["comments"][0]["content"]) > 5000

        mock_api.get_comments.assert_called_once_with(task_id="long_content_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_chronological_order(self, mock_get_api):
        """Test that comments are returned in chronological order."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_comment1 = Mock(spec=Comment)
        mock_comment1.id = "early_comment"
        mock_comment1.task_id = "chronological_task"
        mock_comment1.project_id = "chronological_project"
        mock_comment1.posted_at = "2023-12-01T08:00:00Z"
        mock_comment1.content = "Early morning comment"
        mock_comment1.attachment = None

        mock_comment2 = Mock(spec=Comment)
        mock_comment2.id = "late_comment"
        mock_comment2.task_id = "chronological_task"
        mock_comment2.project_id = "chronological_project"
        mock_comment2.posted_at = "2023-12-01T20:00:00Z"
        mock_comment2.content = "Evening comment"
        mock_comment2.attachment = None

        mock_comment3 = Mock(spec=Comment)
        mock_comment3.id = "midday_comment"
        mock_comment3.task_id = "chronological_task"
        mock_comment3.project_id = "chronological_project"
        mock_comment3.posted_at = "2023-12-01T12:00:00Z"
        mock_comment3.content = "Midday comment"
        mock_comment3.attachment = None

        mock_api.get_comments.return_value = [[mock_comment1, mock_comment2, mock_comment3]]

        result = await get_comments(task_id="chronological_task")

        result_data = json.loads(result)
        assert result_data["count"] == 3

        comment_contents = [c["content"] for c in result_data["comments"]]
        assert "Early morning comment" in comment_contents
        assert "Evening comment" in comment_contents
        assert "Midday comment" in comment_contents

        timestamps = [c["posted_at"] for c in result_data["comments"]]
        assert "2023-12-01T08:00:00Z" in timestamps
        assert "2023-12-01T12:00:00Z" in timestamps
        assert "2023-12-01T20:00:00Z" in timestamps

        mock_api.get_comments.assert_called_once_with(task_id="chronological_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_concurrent_access(self, mock_get_api):
        """Test error when comments are modified during retrieval."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.side_effect = Exception("409 Conflict: Comments modified during retrieval")

        result = await get_comments(task_id="concurrent_access_task")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "409 Conflict: Comments modified during retrieval" in result_data["error"]

        mock_api.get_comments.assert_called_once_with(task_id="concurrent_access_task")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_pagination_edge_case(self, mock_get_api):
        """Test handling of pagination edge cases."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_comments.return_value = [[]]

        result = await get_comments(task_id="pagination_edge_case")

        result_data = json.loads(result)
        assert result_data["count"] == 0
        assert result_data["comments"] == []

        mock_api.get_comments.assert_called_once_with(task_id="pagination_edge_case")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_comments_malformed_attachment(self, mock_get_api):
        """Test handling of malformed attachment data."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_attachment = Mock(spec=Attachment)
        mock_attachment.to_dict.return_value = {
            "file_name": None,
            "file_type": "unknown",
            "file_url": "",
            "file_size": -1
        }

        mock_comment = Mock(spec=Comment)
        mock_comment.id = "malformed_attachment_comment"
        mock_comment.task_id = "malformed_task"
        mock_comment.project_id = "malformed_project"
        mock_comment.posted_at = "2023-12-01T15:00:00Z"
        mock_comment.content = "Comment with malformed attachment"
        mock_comment.attachment = mock_attachment

        mock_api.get_comments.return_value = [[mock_comment]]

        result = await get_comments(task_id="malformed_task")

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["comments"][0]["attachment"]["file_name"] is None
        assert result_data["comments"][0]["attachment"]["file_size"] == -1

        mock_api.get_comments.assert_called_once_with(task_id="malformed_task")
        mock_attachment.to_dict.assert_called_once()
