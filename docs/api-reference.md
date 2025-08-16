# API Reference
## Task Management
- **`create_task`** - Create new tasks with full parameter support
- **`update_task`** - Update existing tasks
- **`complete_task`** - Mark tasks as completed
- **`reopen_task`** - Reopen a previously completed task
- **`delete_task`** - Delete tasks permanently
### `get_task`
Retrieve a specific task by ID.

**Parameters:**
- `task_id` (required): The ID of the task to retrieve

**Return Examples:**
```json
{
  "id": "123456789",
  "content": "Complete project report",
  "description": "Include Q4 metrics and projections",
  "is_completed": false,
  "priority": 3,
  "project_id": "project_123",
  "section_id": "section_456",
  "parent_id": null,
  "order": 5,
  "labels": ["work", "urgent", "report"],
  "due": {
    "date": "2024-01-31",
    "datetime": "2024-01-31T17:00:00Z",
    "string": "Jan 31 5pm",
    "timezone": "America/New_York"
  },
  "url": "https://todoist.com/showTask?id=123456789",
  "created_at": "2024-01-01T10:00:00Z",
  "creator_id": "user_123",
  "assignee_id": "user_456",
  "assigner_id": "user_123"
}
```

**Filter Examples:**

### `get_tasks`
Retrieve tasks with optional filtering.

**Parameters:**
- `project_id` (optional): Filter by project ID
- `label_id` (optional): Filter by label ID  
- `filter_expr` (optional): Todoist filter expression
- `lang` (optional): Language for filter parsing (default: "en")

**Return Examples:**

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