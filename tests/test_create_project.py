import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import create_project
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project


@pytest.fixture(autouse=True)
def clear_global_api_state():
    """Clear the global API state before each test."""
    import todoist_mcp_server
    todoist_mcp_server._api = None
    yield
    todoist_mcp_server._api = None


class TestCreateProject:
    """Unit tests for create_project function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_success_minimal(self, mock_project_to_dict, mock_get_api):
        """Test successful project creation with minimal parameters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Test Project"}
        mock_project_to_dict.return_value = expected_dict

        result = await create_project("Test Project")

        mock_get_api.assert_called_once()
        mock_api.add_project.assert_called_once_with(
            name="Test Project",
            description=None,
            parent_id=None,
            color=None,
            is_favorite=None
        )
        mock_project_to_dict.assert_called_once_with(mock_project)

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_success_all_parameters(self, mock_project_to_dict, mock_get_api):
        """Test successful project creation with all parameters."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {
            "id": "123",
            "name": "Detailed Project",
            "description": "Project description",
            "parent_id": "parent_123",
            "color": "olive_green",
            "is_favorite": True
        }
        mock_project_to_dict.return_value = expected_dict

        result = await create_project(
            name="Detailed Project",
            description="Project description",
            parent_id="parent_123",
            color="olive_green",
            is_favorite=True
        )

        mock_get_api.assert_called_once()
        mock_api.add_project.assert_called_once_with(
            name="Detailed Project",
            description="Project description",
            parent_id="parent_123",
            color="olive_green",
            is_favorite=True
        )
        mock_project_to_dict.assert_called_once_with(mock_project)

        result_dict = json.loads(result)
        assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_with_description_only(self, mock_project_to_dict, mock_get_api):
        """Test project creation with description parameter only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Project with Description"}
        mock_project_to_dict.return_value = expected_dict

        await create_project(
            name="Project with Description",
            description="This is a detailed description"
        )

        mock_api.add_project.assert_called_once_with(
            name="Project with Description",
            description="This is a detailed description",
            parent_id=None,
            color=None,
            is_favorite=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_with_parent_id_only(self, mock_project_to_dict, mock_get_api):
        """Test project creation with parent_id parameter only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Sub Project"}
        mock_project_to_dict.return_value = expected_dict

        await create_project(
            name="Sub Project",
            parent_id="parent_456"
        )

        mock_api.add_project.assert_called_once_with(
            name="Sub Project",
            description=None,
            parent_id="parent_456",
            color=None,
            is_favorite=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_with_color_only(self, mock_project_to_dict, mock_get_api):
        """Test project creation with color parameter only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Colored Project"}
        mock_project_to_dict.return_value = expected_dict

        await create_project(
            name="Colored Project",
            color="red"
        )

        mock_api.add_project.assert_called_once_with(
            name="Colored Project",
            description=None,
            parent_id=None,
            color="red",
            is_favorite=None
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_with_favorite_only(self, mock_project_to_dict, mock_get_api):
        """Test project creation with is_favorite parameter only."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Favorite Project"}
        mock_project_to_dict.return_value = expected_dict

        await create_project(
            name="Favorite Project",
            is_favorite=True
        )

        mock_api.add_project.assert_called_once_with(
            name="Favorite Project",
            description=None,
            parent_id=None,
            color=None,
            is_favorite=True
        )

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_project_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = ValueError("TODOIST_TOKEN environment variable is required")

        result = await create_project("Test Project")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "TODOIST_TOKEN environment variable is required" in result_dict["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_project_api_add_project_error(self, mock_get_api):
        """Test error handling when API add_project fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_project.side_effect = Exception("API error: Invalid project name")

        result = await create_project("Test Project")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "API error: Invalid project name" in result_dict["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_project_to_dict_error(self, mock_project_to_dict, mock_get_api):
        """Test error handling when project_to_dict fails."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project
        mock_project_to_dict.side_effect = Exception("Serialization error")

        result = await create_project("Test Project")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Serialization error" in result_dict["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_valid_name_lengths(self, mock_project_to_dict, mock_get_api):
        """Test project creation with various valid name lengths."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "test"}
        mock_project_to_dict.return_value = expected_dict

        test_cases = [
            "a",  # 1 character (minimum)
            "Test Project",  # Normal length
            "a" * 120,  # 120 characters (maximum)
        ]

        for name in test_cases:
            mock_api.add_project.reset_mock()
            mock_project_to_dict.reset_mock()

            result = await create_project(name)

            mock_api.add_project.assert_called_once()
            assert mock_api.add_project.call_args[1]["name"] == name

            result_dict = json.loads(result)
            assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_valid_description_lengths(self, mock_project_to_dict, mock_get_api):
        """Test project creation with various valid description lengths."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Test Project"}
        mock_project_to_dict.return_value = expected_dict

        test_cases = [
            "",
            "Short description",
            "a" * 1024,
        ]

        for description in test_cases:
            mock_api.add_project.reset_mock()
            mock_project_to_dict.reset_mock()

            result = await create_project("Test Project", description=description)

            mock_api.add_project.assert_called_once()
            assert mock_api.add_project.call_args[1]["description"] == description

            result_dict = json.loads(result)
            assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_various_color_values(self, mock_project_to_dict, mock_get_api):
        """Test project creation with various color values."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Colored Project"}
        mock_project_to_dict.return_value = expected_dict

        color_test_cases = [
            "red",
            "orange",
            "yellow",
            "olive_green",
            "lime_green",
            "green",
            "mint_green",
            "teal",
            "sky_blue",
            "light_blue",
            "blue",
            "grape",
            "violet",
            "lavender",
            "magenta",
            "salmon",
            "charcoal",
            "grey",
            "taupe"
        ]

        for color in color_test_cases:
            mock_api.add_project.reset_mock()
            mock_project_to_dict.reset_mock()

            result = await create_project("Colored Project", color=color)

            mock_api.add_project.assert_called_once()
            assert mock_api.add_project.call_args[1]["color"] == color

            result_dict = json.loads(result)
            assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_boolean_favorite_values(self, mock_project_to_dict, mock_get_api):
        """Test project creation with boolean is_favorite values."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Test Project"}
        mock_project_to_dict.return_value = expected_dict

        for favorite_value in [True, False]:
            mock_api.add_project.reset_mock()
            mock_project_to_dict.reset_mock()

            result = await create_project("Test Project", is_favorite=favorite_value)

            mock_api.add_project.assert_called_once()
            assert mock_api.add_project.call_args[1]["is_favorite"] == favorite_value

            result_dict = json.loads(result)
            assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_various_parent_id_formats(self, mock_project_to_dict, mock_get_api):
        """Test project creation with various parent_id formats."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Sub Project"}
        mock_project_to_dict.return_value = expected_dict

        parent_id_test_cases = [
            "123",
            "project_456",
            "parent-with-dashes",
            "very_long_parent_id_string_with_multiple_sections",
            "UPPERCASE123",
            "mixed_Case_Parent_456"
        ]

        for parent_id in parent_id_test_cases:
            mock_api.add_project.reset_mock()
            mock_project_to_dict.reset_mock()

            result = await create_project("Sub Project", parent_id=parent_id)

            mock_api.add_project.assert_called_once()
            assert mock_api.add_project.call_args[1]["parent_id"] == parent_id

            result_dict = json.loads(result)
            assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_json_output_format(self, mock_project_to_dict, mock_get_api):
        """Test that the output is properly formatted JSON."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {
            "id": "123",
            "name": "Test Project",
            "color": "red",
            "is_favorite": True,
            "unicode_field": "测试项目"
        }
        mock_project_to_dict.return_value = expected_dict

        result = await create_project("Test Project")

        result_dict = json.loads(result)
        assert result_dict == expected_dict

        assert "\n" in result
        assert "  " in result

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_multiple_projects_isolation(self, mock_project_to_dict, mock_get_api):
        """Test creating multiple projects to ensure proper isolation."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project1 = Mock(spec=Project)
        mock_project2 = Mock(spec=Project)

        # Setup different return values for each call
        mock_api.add_project.side_effect = [mock_project1, mock_project2]

        expected_dict1 = {"id": "123", "name": "Project 1"}
        expected_dict2 = {"id": "456", "name": "Project 2"}
        mock_project_to_dict.side_effect = [expected_dict1, expected_dict2]

        result1 = await create_project("Project 1")
        result2 = await create_project("Project 2")

        assert mock_api.add_project.call_count == 2
        assert mock_project_to_dict.call_count == 2

        result_dict1 = json.loads(result1)
        result_dict2 = json.loads(result2)

        assert result_dict1 == expected_dict1
        assert result_dict2 == expected_dict2

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_project_network_error(self, mock_get_api):
        """Test error handling when network error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_project.side_effect = ConnectionError("Network connection failed")

        result = await create_project("Test Project")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Network connection failed" in result_dict["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_project_authentication_error(self, mock_get_api):
        """Test error handling when authentication error occurs."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_project.side_effect = ValueError("Invalid authentication token")

        result = await create_project("Test Project")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Invalid authentication token" in result_dict["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_project_quota_exceeded_error(self, mock_get_api):
        """Test error handling when quota is exceeded."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api
        mock_api.add_project.side_effect = Exception("Project quota exceeded")

        result = await create_project("Test Project")

        result_dict = json.loads(result)
        assert "error" in result_dict
        assert "Project quota exceeded" in result_dict["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_special_characters_in_name(self, mock_project_to_dict, mock_get_api):
        """Test project creation with special characters in name."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Special Project"}
        mock_project_to_dict.return_value = expected_dict

        special_names = [
            "Project with spaces",
            "Project-with-dashes",
            "Project_with_underscores",
            "Project with números 123",
            "Project with émojis 🎯",
            "Project with symbols !@#$%",
            "Project with unicode 测试",
            "Project with quotes \"test\"",
            "Project with apostrophe's"
        ]

        for name in special_names:
            mock_api.add_project.reset_mock()
            mock_project_to_dict.reset_mock()

            result = await create_project(name)

            mock_api.add_project.assert_called_once()
            assert mock_api.add_project.call_args[1]["name"] == name

            result_dict = json.loads(result)
            assert result_dict == expected_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    @patch('todoist_mcp_server.logger')
    async def test_create_project_logging_behavior(self, mock_logger, mock_project_to_dict, mock_get_api):
        """Test that proper logging occurs during project creation."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project

        expected_dict = {"id": "123", "name": "Test Project"}
        mock_project_to_dict.return_value = expected_dict

        await create_project("Test Project")

        mock_logger.info.assert_called_once_with("Creating new project: Test Project")
        mock_logger.error.assert_not_called()

        mock_logger.reset_mock()
        mock_api.add_project.side_effect = Exception("Test error")

        await create_project("Error Project")

        mock_logger.info.assert_called_once_with("Creating new project: Error Project")
        mock_logger.error.assert_called_once_with("Error creating project Error Project: Test error")

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_create_project_return_type_consistency(self, mock_project_to_dict, mock_get_api):
        """Test that create_project always returns a string."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_project = Mock(spec=Project)
        mock_api.add_project.return_value = mock_project
        mock_project_to_dict.return_value = {"id": "123", "name": "Test"}

        result = await create_project("Test Project")
        assert isinstance(result, str)

        mock_api.add_project.side_effect = Exception("Test error")

        result = await create_project("Error Project")
        assert isinstance(result, str)

        error_dict = json.loads(result)
        assert "error" in error_dict

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_create_project_concurrent_creation_simulation(self, mock_get_api):
        """Test behavior under simulated concurrent project creation."""
        mock_api = Mock(spec=TodoistAPI)
        mock_get_api.return_value = mock_api

        mock_projects = [Mock(spec=Project) for _ in range(5)]
        mock_api.add_project.side_effect = mock_projects

        with patch('todoist_mcp_server.project_to_dict') as mock_project_to_dict:
            mock_project_to_dict.side_effect = [
                {"id": f"{i}", "name": f"Project {i}"} for i in range(5)
            ]

            results = []
            for i in range(5):
                result = await create_project(f"Project {i}")
                results.append(result)

            assert mock_api.add_project.call_count == 5
            assert mock_project_to_dict.call_count == 5

            for i, result in enumerate(results):
                result_dict = json.loads(result)
                assert result_dict["id"] == str(i)
                assert result_dict["name"] == f"Project {i}"
