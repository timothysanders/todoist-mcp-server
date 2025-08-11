# Changelog
All notable changes to the Todoist MCP server project will be documented in this file.

## [Unreleased]
### Added
- **create_project tool** ([#2](https://github.com/timothysanders/todoist-mcp-server/issues/2))
  - Allows for the creation of new projects
  - Includes full unit test suite
- **create_label tool** ([#3](https://github.com/timothysanders/todoist-mcp-server/issues/3))
  - Allows for the creation of new labels
  - Includes full unit test suite

## [0.0.2]
### Added
- **Development Infrastructure**
  - Comprehensive test suite for all MCP tools
  - Pre-commit hooks with Ruff linting and pytest
  - Structured logging system
- **Documentation & Setup**
  - Installation and setup instructions added to README
  - Complete API reference with examples
  - Claude Desktop integration guide
  - Environment variable configuration with .env support
  - Branch naming conventions and contributing guidelines
- **Technical Features**
  - FastMCP server implementation
  - Error handling and validation
  - Unicode and special character support
  - Filter expressions support
### Changed
- Fixes for data processing bugs in `get_tasks`, `get_projects`, and `get_labels` where responses with multiple tasks/projects/labels would only return the first item.

## [0.0.1]
### Added
- **Core Task Management**
  - `get_tasks` - Retrieve tasks with filtering options
  - `get_task` - Retrieve a specific task by ID
  - `create_task` - Create new tasks with parameter support
  - `update_task` - Update existing tasks
  - `complete_task` - Mark tasks as completed
  - `reopen_task` - Reopen completed tasks
  - `delete_task` - Delete tasks permanently
- **Project & Label Management**
  - `get_projects` - Retrieve all projects
  - `get_project` - Retrieve a specific project by ID
  - `get_labels` - Retrieve all labels
  - `get_comments` - Retrieve comments for tasks and projects

---
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
