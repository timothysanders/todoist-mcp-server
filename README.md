# Todoist MCP Server
A Model Context Protocol (MCP) server that provides seamless integration with Todoist, allowing AI assistants like Claude to interact with your Todoist tasks and projects.

## Features
This MCP server provides the following tools for Todoist integration:

### Task Management
- **`get_tasks`** - Retrieve tasks with powerful filtering options
- **`create_task`** - Create new tasks with full parameter support
- **`update_task`** - Update existing tasks
- **`complete_task`** - Mark tasks as completed
- **`delete_task`** - Delete tasks permanently

### Project & Label Management
- **`get_projects`** - Retrieve all projects
- **`get_labels`** - Retrieve all labels

## Prerequisites
- Python 3.10 or higher
- A Todoist account with API access
- Todoist API token (bearer token)

## Installation
### 1. Set up the Project
```bash
# Create project directory
mkdir todoist-mcp-server
cd todoist-mcp-server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies
Using the requirements file:
```bash
pip install -r requirements.txt
```

### 3. Get Your Todoist API Token
1. Go to [Todoist Integrations](https://app.todoist.com/app/settings/integrations/developer)
2. Create a new app or use an existing one
3. Copy your API token

### 4. Configure Environment
Create a `.env` file or set the environment variable:
```bash
export TODOIST_TOKEN="your_bearer_token_here"
```

Or create a `.env` file:
```env
TODOIST_TOKEN=your_bearer_token_here
```

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

## Integration with Claude Desktop
Add the following configuration to your `claude_desktop_config.json` file:

### macOS
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows  
Location: `%APPDATA%\Claude\claude_desktop_config.json`

### Configuration
```json
{
  "mcpServers": {
    "todoist": {
      "command": "/absolute/path/to/virtual/environment/python",
      "args": ["/absolute/path/to/todoist_mcp_server.py"],
      "env": {
        "TODOIST_TOKEN": "your_bearer_token_here"
      }
    }
  }
}
```

**Important Notes:**
- Use the absolute path to your `todoist_mcp_server.py` file
- You may need to use the full path to your Python executable (e.g., `/path/to/venv/bin/python`)
- On Windows, use double backslashes (`\\`) or forward slashes (`/`) in paths
- After adding the configuration, restart Claude Desktop

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

### Contributing
1. Follow the existing code style with type hints and docstrings
2. All functions should have comprehensive Numpy-style docstrings
3. Add appropriate error handling for new features
4. Test new tools with the MCP Inspector before