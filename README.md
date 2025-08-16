# Todoist MCP Server
A Model Context Protocol (MCP) server that provides seamless integration with Todoist, allowing AI assistants like Claude to interact with your Todoist tasks and projects.

## Features
This MCP server provides the following tools for Todoist integration:

### Task Management
- **`get_task`** - Retrieve a specific task with filtering options
- **`get_tasks`** - Retrieve tasks with powerful filtering options
- **`create_task`** - Create new tasks with full parameter support
- **`update_task`** - Update existing tasks
- **`complete_task`** - Mark tasks as completed
- **`reopen_task`** - Reopen a previously completed task
- **`delete_task`** - Delete tasks permanently

### Project Management
- **`create_project`** - Create a new project
- **`get_project`** - Retrieve a single project by ID
- **`get_projects`** - Retrieve all projects

### Label Management
- **`create_label`** - Create a new label
- **`get_labels`** - Retrieve all labels

### Comments
- **`get_comments`** - Retrieve comments associated with a task/project

## Prerequisites
- Python 3.10 or higher
- A Todoist account with API access
- Todoist API token (bearer token)

## Usage
### Running the Server Standalone
```bash
python todoist_mcp_server.py
```

### Testing with MCP Inspector
Install the MCP CLI tools:
```bash
pip install "mcp[cli]"
```

Test your server:
```bash
mcp dev todoist_mcp_server.py
```
This will open a web interface where you can test all the tools.

### Run Unit Tests
To run unit tests, make sure you have installed the project requirements and then run the following command from the repository root
```bash
# Run all tests
python -m pytest
```
To verify unit test coverage, run the following command
```bash
python -m pytest --cov=todoist_mcp_server
```

### Pre-commit Hooks
This project utilizes the [pre-commit](https://pre-commit.com/) library to install and run pre-commit hooks.

First, install pre-commit using pip
```bash
pip install pre-commit
```
Then use pre-commit to install the `.pre-commit-config.yaml` file
```bash
pre-commit install
```
To validate the installation, you can run either of the following commands
```bash
ls -la .git/hooks
# look for `pre-commit` in the output

pre-commit run --all-files
```

## Tool Examples
Once integrated with Claude, you can use natural language to interact with your Todoist:

### Reading Tasks
- "What tasks do I have today?"
- "Show me all my overdue tasks"
- "List tasks in my Work project"
- "What tasks are labeled with @urgent?"

### Creating Tasks
- "Create a task to buy groceries"
- "Add a high-priority task to finish the report by tomorrow"
- "Create a subtask under my project planning task"

### Managing Tasks
- "Mark my grocery shopping task as complete"
- "Update my meeting task to be due next Friday"
- "Delete the old planning task"
- "Change the priority of my report task to urgent"

### Projects and Labels
- "Show me all my projects"
- "List all available labels"
- "Create a label with the color olive green and mark is as a favorite"

## API Reference
### get_tasks
Retrieve tasks with optional filtering.

**Parameters:**
- `project_id` (optional): Filter by project ID
- `label_id` (optional): Filter by label ID  
- `filter_expr` (optional): Todoist filter expression
- `lang` (optional): Language for filter parsing (default: "en")

**Filter Examples:**
- `"today"` - Tasks due today
- `"overdue"` - Overdue tasks
- `"@work"` - Tasks with the "work" label
- `"p1"` - Priority 1 (urgent) tasks
- `"next 7 days"` - Tasks due in the next week

### create_task
Create a new task.

**Parameters:**
- `content` (required): Task title
- `description` (optional): Task description
- `project_id` (optional): Project to add task to
- `priority` (optional): 1 (normal) to 4 (urgent)
- `due_string` (optional): Natural language due date
- `labels` (optional): List of label names

### create_project
Create a new project

**Parameters:**
- `name` (required): Name for new project
- `description` (optional): Project description
- `parent_id` (optional): The parent project to link the new project to
- `color` (optional): The color to assign to the new project
- `is_favorite` (optional): Whether to mark this project as a favorite

### create_label
Create a new label

**Parameters:**
- `name` (required): Name for the new label
- `color` (optional): The color to assign to the new label
- `is_favorite` (optional): Whether to mark this label as a favorite

### Other Tools
All tools return JSON responses and include comprehensive error handling.

## Error Handling
The server includes robust error handling:
- Invalid API tokens are caught at startup
- HTTP errors are logged and returned as JSON
- Network timeouts are handled gracefully
- All errors include descriptive messages

## Logging
The server logs to stderr (not stdout to avoid interfering with MCP protocol):
- INFO level for normal operations
- ERROR level for failures
- All requests and responses are logged for debugging

## Development
### Project Structure
```
todoist-mcp-server/
├── todoist_mcp_server.py      # Main server implementation
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── .env.example          # Environment template
└── README.md             # This file
```

### Branch Naming Conventions
**General Format**: `type/issue-number-brief-description`

**Types**:
- `feature/` - New functionality or enhancements
- `bug/` - Bug fixes
- `hotfix/` - Critical fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks

#### Examples
```text
feature/23-add-project-creation
bug/45-fix-task-completion-error
docs/12-update-api-documentation
refactor/67-restructure-task-handlers
test/34-add-integration-tests
hotfix/89-critical-auth-bug
```

### Contributing
1. Follow the existing code style with type hints and docstrings
2. All functions should have comprehensive Numpy-style docstrings
3. Add appropriate error handling for new features
4. Test new tools with the MCP Inspector before