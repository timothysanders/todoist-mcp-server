import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import get_project
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project


@pytest.fixture
def mock_project():
    return Mock(spec=Project)

class TestGetProject:
    """Unit tests for get_project function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_success_basic(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test successfully retrieving a basic project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "project_123",
            "name": "Basic Test Project",
            "order": 1,
            "color": "blue",
            "is_shared": False,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "list",
            "url": "https://todoist.com/showProject?id=project_123",
            "parent_id": None
        }

        result = await get_project("project_123")

        result_data = json.loads(result)
        assert result_data["id"] == "project_123"
        assert result_data["name"] == "Basic Test Project"
        assert result_data["color"] == "blue"
        assert not result_data["is_shared"]
        assert result_data["view_style"] == "list"

        mock_api.get_project.assert_called_once_with(project_id="project_123")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_success_inbox(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test successfully retrieving the inbox project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "inbox_456",
            "name": "Inbox",
            "order": 0,
            "color": "grey",
            "is_shared": False,
            "is_favorite": True,
            "is_inbox_project": True,
            "view_style": "list",
            "url": "https://todoist.com/showProject?id=inbox_456",
            "parent_id": None
        }

        result = await get_project("inbox_456")

        result_data = json.loads(result)
        assert result_data["id"] == "inbox_456"
        assert result_data["name"] == "Inbox"
        assert result_data["is_inbox_project"]
        assert result_data["is_favorite"]
        assert result_data["color"] == "grey"

        mock_api.get_project.assert_called_once_with(project_id="inbox_456")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_success_shared(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test successfully retrieving a shared project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "shared_789",
            "name": "Team Collaboration Project",
            "order": 5,
            "color": "red",
            "is_shared": True,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "board",
            "url": "https://todoist.com/showProject?id=shared_789",
            "parent_id": None,
            "collaborators": ["user1@example.com", "user2@example.com"],
            "shared_labels": ["team", "collaboration"]
        }

        result = await get_project("shared_789")

        result_data = json.loads(result)
        assert result_data["id"] == "shared_789"
        assert result_data["name"] == "Team Collaboration Project"
        assert result_data["is_shared"]
        assert result_data["view_style"] == "board"
        assert result_data["color"] == "red"
        assert "collaborators" in result_data

        mock_api.get_project.assert_called_once_with(project_id="shared_789")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_success_subproject(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test successfully retrieving a subproject."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "subproject_321",
            "name": "Development Subproject",
            "order": 2,
            "color": "green",
            "is_shared": False,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "list",
            "url": "https://todoist.com/showProject?id=subproject_321",
            "parent_id": "parent_project_456"
        }

        result = await get_project("subproject_321")

        result_data = json.loads(result)
        assert result_data["id"] == "subproject_321"
        assert result_data["name"] == "Development Subproject"
        assert result_data["parent_id"] == "parent_project_456"
        assert result_data["color"] == "green"

        mock_api.get_project.assert_called_once_with(project_id="subproject_321")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_success_different_project_ids(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving projects with different project ID formats."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        test_project_ids = [
            "123456789",
            "project_abc_123",
            "work-project-456",
            "very_long_project_id_for_testing_purposes_123456789",
            "project.with.dots.789",
            "PROJECT_UPPERCASE_456"
        ]

        for project_id in test_project_ids:
            mock_api.get_project.return_value = mock_project

            mock_project_to_dict.return_value = {
                "id": project_id,
                "name": f"Project {project_id}",
                "order": 1,
                "color": "blue",
                "is_shared": False,
                "is_favorite": False,
                "is_inbox_project": False,
                "view_style": "list",
                "url": f"https://todoist.com/showProject?id={project_id}",
                "parent_id": None
            }

            result = await get_project(project_id)

            result_data = json.loads(result)
            assert result_data["id"] == project_id
            assert result_data["name"] == f"Project {project_id}"

            mock_api.get_project.assert_called_with(project_id=project_id)

            # Reset mocks for next iteration
            mock_api.get_project.reset_mock()
            mock_project_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_success_unicode_content(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving project with unicode characters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "unicode_project_123",
            "name": "Projet français avec émojis 🎯",
            "order": 3,
            "color": "purple",
            "is_shared": True,
            "is_favorite": True,
            "is_inbox_project": False,
            "view_style": "board",
            "url": "https://todoist.com/showProject?id=unicode_project_123",
            "parent_id": None,
            "description": "Description avec caractères spéciaux et 中文"
        }

        result = await get_project("unicode_project_123")

        result_data = json.loads(result)
        assert result_data["name"] == "Projet français avec émojis 🎯"
        assert result_data["description"] == "Description avec caractères spéciaux et 中文"
        assert result_data["color"] == "purple"

        mock_api.get_project.assert_called_once_with(project_id="unicode_project_123")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_success_all_view_styles(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving projects with different view styles."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        view_styles = ["list", "board"]

        for view_style in view_styles:
            mock_api.get_project.return_value = mock_project

            mock_project_to_dict.return_value = {
                "id": f"project_{view_style}",
                "name": f"Project with {view_style} view",
                "order": 1,
                "color": "blue",
                "is_shared": False,
                "is_favorite": False,
                "is_inbox_project": False,
                "view_style": view_style,
                "url": f"https://todoist.com/showProject?id=project_{view_style}",
                "parent_id": None
            }

            result = await get_project(f"project_{view_style}")

            result_data = json.loads(result)
            assert result_data["view_style"] == view_style
            assert result_data["name"] == f"Project with {view_style} view"

            mock_api.get_project.assert_called_with(project_id=f"project_{view_style}")

            # Reset mocks for next iteration
            mock_api.get_project.reset_mock()
            mock_project_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_not_found(self, mock_get_api):
        """Test error handling when project is not found."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("404 Not Found: Project does not exist")

        result = await get_project("nonexistent_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "404 Not Found: Project does not exist" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="nonexistent_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_deleted_project(self, mock_get_api):
        """Test error handling when trying to retrieve a deleted project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("Project has been deleted")

        result = await get_project("deleted_project_123")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Project has been deleted" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="deleted_project_123")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_archived_project(self, mock_get_api):
        """Test error handling when trying to retrieve an archived project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("Cannot access archived project")

        result = await get_project("archived_project_456")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Cannot access archived project" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="archived_project_456")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_permission_denied(self, mock_get_api):
        """Test error handling when user lacks permission to view project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("403 Forbidden: Access denied to private project")

        result = await get_project("private_project_789")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "403 Forbidden: Access denied to private project" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="private_project_789")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_shared_project_access_denied(self, mock_get_api):
        """Test error when user lacks access to shared project."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("Not a member of shared project")

        result = await get_project("restricted_shared_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Not a member of shared project" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="restricted_shared_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await get_project("project_789")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = ConnectionError("Network connection failed")

        result = await get_project("project_network_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Network connection failed" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="project_network_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_authentication_error(self, mock_get_api):
        """Test error handling when authentication fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("401 Unauthorized: Invalid token")

        result = await get_project("project_auth_test")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "401 Unauthorized: Invalid token" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="project_auth_test")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_rate_limit_error(self, mock_get_api):
        """Test error handling when API rate limit is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("429 Too Many Requests: Rate limit exceeded")

        result = await get_project("rate_limit_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "429 Too Many Requests: Rate limit exceeded" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="rate_limit_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_server_error(self, mock_get_api):
        """Test error handling when server error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("500 Internal Server Error")

        result = await get_project("server_error_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "500 Internal Server Error" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="server_error_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_project_to_dict_error(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test error handling when project_to_dict fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.side_effect = Exception("Project serialization error")

        result = await get_project("serialization_error_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Project serialization error" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="serialization_error_project")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_empty_string_project_id(self, mock_get_api):
        """Test retrieving project with empty string project ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("Invalid project ID: empty string")

        result = await get_project("")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid project ID: empty string" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_whitespace_project_id(self, mock_get_api):
        """Test retrieving project with whitespace-only project ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("Invalid project ID: whitespace only")

        whitespace_project_id = "   "

        result = await get_project(whitespace_project_id)

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Invalid project ID: whitespace only" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id=whitespace_project_id)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_with_special_characters(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving project with special characters in project ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        special_project_ids = [
            "project-with-dashes-123",
            "project_with_underscores_456",
            "project.with.dots.789",
            "project@with@symbols#123",
            "project%20with%20encoding",
            "project+plus+signs+456"
        ]

        for project_id in special_project_ids:
            mock_api.get_project.return_value = mock_project

            mock_project_to_dict.return_value = {
                "id": project_id,
                "name": f"Project with special characters: {project_id}",
                "order": 1,
                "color": "blue",
                "is_shared": False,
                "is_favorite": False,
                "is_inbox_project": False,
                "view_style": "list",
                "url": f"https://todoist.com/showProject?id={project_id}",
                "parent_id": None
            }

            result = await get_project(project_id)

            result_data = json.loads(result)
            assert result_data["id"] == project_id
            assert project_id in result_data["name"]

            mock_api.get_project.assert_called_with(project_id=project_id)

            # Reset mocks for next iteration
            mock_api.get_project.reset_mock()
            mock_project_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_return_type(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test that get_project returns a string (JSON)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "return_type_test",
            "name": "Test Project",
            "order": 1,
            "color": "blue",
            "is_shared": False,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "list",
            "url": "https://todoist.com/showProject?id=return_type_test",
            "parent_id": None
        }

        result = await get_project("return_type_test")

        assert isinstance(result, str)
        json.loads(result)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_json_formatting(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "format_test",
            "name": "JSON formatting test project",
            "order": 2,
            "color": "green",
            "is_shared": True,
            "is_favorite": True,
            "is_inbox_project": False,
            "view_style": "board",
            "url": "https://todoist.com/showProject?id=format_test",
            "parent_id": None
        }

        result = await get_project("format_test")

        result_data = json.loads(result)

        reformatted = json.dumps(result_data, indent=2, ensure_ascii=False, default=str)

        assert isinstance(result_data, dict)
        assert isinstance(reformatted, str)
        assert result_data["name"] == "JSON formatting test project"

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_direct_response_structure(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test that get_project returns project data directly (not wrapped in success/error structure)."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "direct_response_test",
            "name": "Direct response test project",
            "order": 1,
            "color": "purple",
            "is_shared": False,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "list",
            "url": "https://todoist.com/showProject?id=direct_response_test",
            "parent_id": None
        }

        result = await get_project("direct_response_test")

        result_data = json.loads(result)

        # Should return project data directly, not wrapped in success/error structure
        assert "id" in result_data
        assert "name" in result_data
        assert "color" in result_data
        assert "success" not in result_data
        assert "message" not in result_data
        assert result_data["id"] == "direct_response_test"
        assert result_data["name"] == "Direct response test project"

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_timeout_error(self, mock_get_api):
        """Test error handling when API call times out."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = TimeoutError("Request timed out")

        result = await get_project("timeout_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Request timed out" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="timeout_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_very_long_project_id(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving project with very long project ID."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        long_project_id = "very_long_project_id_for_retrieval_testing_" + "x" * 200 + "_end"

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": long_project_id,
            "name": "Project with very long ID",
            "order": 1,
            "color": "blue",
            "is_shared": False,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "list",
            "url": f"https://todoist.com/showProject?id={long_project_id}",
            "parent_id": None
        }

        result = await get_project(long_project_id)

        result_data = json.loads(result)
        assert result_data["id"] == long_project_id
        assert result_data["name"] == "Project with very long ID"

        mock_api.get_project.assert_called_once_with(project_id=long_project_id)
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_multiple_consecutive_calls(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test multiple consecutive project retrievals."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        project_ids = ["project_1", "project_2", "project_3", "project_4", "project_5"]

        for project_id in project_ids:
            mock_api.get_project.return_value = mock_project

            mock_project_to_dict.return_value = {
                "id": project_id,
                "name": f"Project {project_id}",
                "order": 1,
                "color": "blue",
                "is_shared": False,
                "is_favorite": False,
                "is_inbox_project": False,
                "view_style": "list",
                "url": f"https://todoist.com/showProject?id={project_id}",
                "parent_id": None
            }

            result = await get_project(project_id)

            result_data = json.loads(result)
            assert result_data["id"] == project_id
            assert result_data["name"] == f"Project {project_id}"

            mock_api.get_project.assert_called_with(project_id=project_id)

        assert mock_api.get_project.call_count == len(project_ids)
        assert mock_project_to_dict.call_count == len(project_ids)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_favorite_project(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving a favorite project with special attributes."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "favorite_project_999",
            "name": "⭐ Important Work Project",
            "order": 1,
            "color": "yellow",
            "is_shared": True,
            "is_favorite": True,
            "is_inbox_project": False,
            "view_style": "board",
            "url": "https://todoist.com/showProject?id=favorite_project_999",
            "parent_id": None,
            "collaborators": ["manager@company.com", "team@company.com"],
            "created_at": "2023-01-01T00:00:00Z"
        }

        result = await get_project("favorite_project_999")

        result_data = json.loads(result)
        assert result_data["is_favorite"]
        assert "⭐" in result_data["name"]
        assert result_data["color"] == "yellow"
        assert result_data["is_shared"]
        assert result_data["view_style"] == "board"
        assert "collaborators" in result_data

        mock_api.get_project.assert_called_once_with(project_id="favorite_project_999")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_all_colors(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving projects with different color schemes."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        colors = ["red", "orange", "yellow", "green", "blue", "purple", "grey"]

        for color in colors:
            mock_api.get_project.return_value = mock_project

            mock_project_to_dict.return_value = {
                "id": f"project_{color}",
                "name": f"Project with {color} color",
                "order": 1,
                "color": color,
                "is_shared": False,
                "is_favorite": False,
                "is_inbox_project": False,
                "view_style": "list",
                "url": f"https://todoist.com/showProject?id=project_{color}",
                "parent_id": None
            }

            result = await get_project(f"project_{color}")

            result_data = json.loads(result)
            assert result_data["color"] == color
            assert result_data["name"] == f"Project with {color} color"

            mock_api.get_project.assert_called_with(project_id=f"project_{color}")

            # Reset mocks for next iteration
            mock_api.get_project.reset_mock()
            mock_project_to_dict.reset_mock()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_workspace_limitation(self, mock_get_api):
        """Test error when trying to access project from different workspace."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("Project not accessible from current workspace")

        result = await get_project("other_workspace_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Project not accessible from current workspace" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="other_workspace_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_team_business_restriction(self, mock_get_api):
        """Test error when accessing team/business project without proper subscription."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("Team project requires business subscription")

        result = await get_project("team_business_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Team project requires business subscription" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="team_business_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_complex_hierarchy(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving project with complex hierarchical structure."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "complex_hierarchy_project",
            "name": "Development > Frontend > React Components",
            "order": 15,
            "color": "blue",
            "is_shared": True,
            "is_favorite": False,
            "is_inbox_project": False,
            "view_style": "list",
            "url": "https://todoist.com/showProject?id=complex_hierarchy_project",
            "parent_id": "frontend_project_456",
            "child_projects": ["component_library_789", "ui_toolkit_123"],
            "project_path": ["Development", "Frontend", "React Components"],
            "depth_level": 3
        }

        result = await get_project("complex_hierarchy_project")

        result_data = json.loads(result)
        assert "Development > Frontend > React Components" in result_data["name"]
        assert result_data["parent_id"] == "frontend_project_456"
        assert "child_projects" in result_data
        assert "project_path" in result_data
        assert result_data["depth_level"] == 3

        mock_api.get_project.assert_called_once_with(project_id="complex_hierarchy_project")
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_project_concurrent_modification_conflict(self, mock_get_api):
        """Test error when project is modified by another client during retrieval."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.side_effect = Exception("409 Conflict: Project was modified by another client")

        result = await get_project("concurrent_modification_project")

        result_data = json.loads(result)
        assert "error" in result_data
        assert "409 Conflict: Project was modified by another client" in result_data["error"]

        mock_api.get_project.assert_called_once_with(project_id="concurrent_modification_project")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_project_template_project(self, mock_project_to_dict, mock_get_api, mock_project):
        """Test retrieving a project template with special metadata."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_api.get_project.return_value = mock_project

        mock_project_to_dict.return_value = {
            "id": "template_project_555",
            "name": "📋 Project Template: Marketing Campaign",
            "order": 0,
            "color": "orange",
            "is_shared": False,
            "is_favorite": True,
            "is_inbox_project": False,
            "view_style": "board",
            "url": "https://todoist.com/showProject?id=template_project_555",
            "parent_id": None,
            "is_template": True,
            "template_category": "marketing",
            "default_sections": ["Planning", "In Progress", "Review", "Complete"],
            "template_description": "Standard template for marketing campaign management"
        }

        result = await get_project("template_project_555")

        result_data = json.loads(result)
        assert "📋" in result_data["name"]
        assert "Template" in result_data["name"]
        assert result_data["is_template"]
        assert result_data["template_category"] == "marketing"
        assert "default_sections" in result_data
        assert len(result_data["default_sections"]) == 4

        mock_api.get_project.assert_called_once_with(project_id="template_project_555")
        mock_project_to_dict.assert_called_once_with(mock_project)
