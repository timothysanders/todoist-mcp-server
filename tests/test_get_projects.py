import pytest
import json
from unittest.mock import Mock, patch
from todoist_mcp_server import get_projects


class TestGetProjects:
    """Unit tests for get_projects function."""

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_success_empty(self, mock_project_to_dict, mock_get_api):
        """Test getting projects when no projects exist."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_api.get_projects.return_value = [[]]  # Paginator returns list of lists, empty

        result = await get_projects()

        result_data = json.loads(result)
        assert result_data["count"] == 0
        assert len(result_data["projects"]) == 0
        assert result_data["projects"] == []

        mock_api.get_projects.assert_called_once()
        mock_project_to_dict.assert_not_called()

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_success_single_project(self, mock_project_to_dict, mock_get_api):
        """Test getting projects with a single project."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_project = Mock()
        mock_api.get_projects.return_value = [[mock_project]]
        mock_project_to_dict.return_value = {
            "id": "123456789",
            "name": "Work Project",
            "color": "red",
            "is_shared": False,
            "is_favorite": True
        }

        result = await get_projects()

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert len(result_data["projects"]) == 1
        assert result_data["projects"][0]["id"] == "123456789"
        assert result_data["projects"][0]["name"] == "Work Project"
        assert result_data["projects"][0]["color"] == "red"

        mock_api.get_projects.assert_called_once()
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_success_multiple_projects(self, mock_project_to_dict, mock_get_api):
        """Test getting multiple projects."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_project1 = Mock()
        mock_project2 = Mock()
        mock_project3 = Mock()
        mock_api.get_projects.return_value = [[mock_project1, mock_project2, mock_project3]]

        mock_project_to_dict.side_effect = [
            {"id": "1", "name": "Personal", "color": "blue"},
            {"id": "2", "name": "Work", "color": "red"},
            {"id": "3", "name": "Shopping", "color": "green"}
        ]

        result = await get_projects()

        result_data = json.loads(result)
        assert result_data["count"] == 3
        assert len(result_data["projects"]) == 3
        assert result_data["projects"][0]["id"] == "1"
        assert result_data["projects"][0]["name"] == "Personal"
        assert result_data["projects"][1]["id"] == "2"
        assert result_data["projects"][1]["name"] == "Work"
        assert result_data["projects"][2]["id"] == "3"
        assert result_data["projects"][2]["name"] == "Shopping"

        mock_api.get_projects.assert_called_once()
        assert mock_project_to_dict.call_count == 3

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_projects_get_api_error(self, mock_get_api):
        """Test error handling when get_api fails."""
        mock_get_api.side_effect = Exception("API initialization failed")

        result = await get_projects()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "API initialization failed" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    async def test_get_projects_api_call_error(self, mock_get_api):
        """Test error handling when API call fails."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.get_projects.side_effect = Exception("Todoist API error: connection timeout")

        result = await get_projects()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Todoist API error: connection timeout" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_project_to_dict_error(self, mock_project_to_dict, mock_get_api):
        """Test error handling when project_to_dict fails."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_project = Mock()
        mock_api.get_projects.return_value = [[mock_project]]
        mock_project_to_dict.side_effect = Exception("Project serialization error")

        result = await get_projects()

        result_data = json.loads(result)
        assert "error" in result_data
        assert "Project serialization error" in result_data["error"]

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_complex_project_data(self, mock_project_to_dict, mock_get_api):
        """Test getting projects with complex project data including special characters."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_project = Mock()
        mock_api.get_projects.return_value = [[mock_project]]
        mock_project_to_dict.return_value = {
            "id": "999",
            "name": "Projét avec caractères spéciaux 🎯",
            "color": "purple",
            "is_shared": True,
            "is_favorite": False,
            "collaborators": ["user1@example.com", "user2@example.com"],
            "created_at": "2023-01-01T00:00:00Z"
        }

        result = await get_projects()

        result_data = json.loads(result)
        assert result_data["count"] == 1
        assert result_data["projects"][0]["name"] == "Projét avec caractères spéciaux 🎯"
        assert result_data["projects"][0]["is_shared"]
        assert len(result_data["projects"][0]["collaborators"]) == 2

        mock_api.get_projects.assert_called_once()
        mock_project_to_dict.assert_called_once_with(mock_project)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_paginator_structure(self, mock_project_to_dict, mock_get_api):
        """Test that the function correctly handles the paginator structure."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_project1 = Mock()
        mock_project2 = Mock()
        mock_paginator = [[mock_project1, mock_project2]]  # Paginator returns a nested structure
        mock_api.get_projects.return_value = mock_paginator

        mock_project_to_dict.side_effect = [
            {"id": "1", "name": "Project 1"},
            {"id": "2", "name": "Project 2"}
        ]

        result = await get_projects()

        result_data = json.loads(result)
        assert result_data["count"] == 2
        assert len(result_data["projects"]) == 2

        mock_api.get_projects.assert_called_once()
        assert mock_project_to_dict.call_count == 2

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_json_formatting(self, mock_project_to_dict, mock_get_api):
        """Test that the JSON output is properly formatted."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api

        mock_project = Mock()
        mock_api.get_projects.return_value = [[mock_project]]
        mock_project_to_dict.return_value = {"id": "1", "name": "Test Project"}

        result = await get_projects()

        result_data = json.loads(result)
        assert isinstance(result_data, dict)
        assert "projects" in result_data
        assert "count" in result_data

        assert isinstance(result_data["projects"], list)
        assert isinstance(result_data["count"], int)

    @pytest.mark.asyncio
    @patch('todoist_mcp_server.get_api')
    @patch('todoist_mcp_server.project_to_dict')
    async def test_get_projects_return_type(self, mock_project_to_dict, mock_get_api):
        """Test that the function returns a string (JSON)."""
        mock_api = Mock()
        mock_get_api.return_value = mock_api
        mock_api.get_projects.return_value = [[]]

        result = await get_projects()

        assert isinstance(result, str)
        json.loads(result)