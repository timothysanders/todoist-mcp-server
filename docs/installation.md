# Installation

## 1. Clone the Repo
```bash
git clone https://github.com/timothysanders/todoist-mcp-server.git
cd todoist-mcp-server
```

## 2. Set up the Project
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

## 3. Install Dependencies
Using the requirements file:
```bash
pip install -r requirements.txt
```

## 4. Retrieve Todoist API Token
1. Go to [Todoist Integrations](https://app.todoist.com/app/settings/integrations/developer)
2. Create a new app or use an existing one
3. Copy your API token

Alternatively, you can create a new API token from the Todoist application
1. Go to Settings -> Integrations
2. Toggle to "Developer"
3. Select "Issue a new API token"

## 5. Environment Configuration
Create a `.env` file or set the environment variable with the value retrieved from the API token in the previous step:
```bash
export TODOIST_TOKEN="your_bearer_token_here"
```

Or create a `.env` file (using the sample `.env.example`):
```env
TODOIST_TOKEN=your_bearer_token_here
```

## 6. Configure Desktop Applications
### Integration with Claude Desktop
Add the following configuration to your `claude_desktop_config.json` file:

#### `claude_desktop_config.json` Example
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
- Use the absolute path to the `todoist_mcp_server.py` file
- You may need to use the full path to your Python executable (e.g., `/path/to/venv/bin/python`)
- On Windows, use double backslashes (`\\`) or forward slashes (`/`) in paths
- After adding the configuration, restart Claude Desktop to begin using the tools
- 
#### macOS
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Windows  
Location: `%APPDATA%\Claude\claude_desktop_config.json`
