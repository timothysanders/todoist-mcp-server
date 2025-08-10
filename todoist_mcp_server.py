"""
Todoist MCP Server

A Model Context Protocol (MCP) server for interacting with Todoist tasks.
This server provides tools for reading, creating, updating, and managing Todoist tasks
using the official Todoist Python SDK.

Usage:
    python todoist_mcp_server.py

Environment Variables:
    TODOIST_TOKEN: Your Todoist API bearer token (required)

MCP Configuration for Claude Desktop:
Add this to your claude_desktop_config.json:
{
  "mcpServers": {
    "todoist": {
      "command": "python",
      "args": ["/path/to/todoist_mcp_server.py"],
      "env": {
        "TODOIST_TOKEN": "your_bearer_token_here"
      }
    }
  }
}
"""

import os
import sys
import logging
from typing import Annotated, Any, Dict, List, Optional
import json

from pydantic import Field
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task, Project, Label
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file, if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

mcp = FastMCP("todoist-mcp-server")


_api: Optional[TodoistAPI] = None


def get_api() -> TodoistAPI:
    """
    Get or create the Todoist API instance.

    Returns
    -------
    TodoistAPI
        The initialized Todoist API client

    Raises
    ------
    ValueError
        If the TODOIST_TOKEN environment variable is not set
    """
    global _api
    if _api is None:
        token = os.getenv("TODOIST_TOKEN")
        if not token or not token.strip():
            raise ValueError("TODOIST_TOKEN environment variable is required")
        _api = TodoistAPI(token)
    return _api


def task_to_dict(task: Task) -> Dict[str, Any]:
    """
    Convert a Task object to a dictionary for JSON serialization.

    Parameters
    ----------
    task : Task
        The task object from the Todoist SDK

    Returns
    -------
    Dict[str, Any]
        Dictionary representation of the task
    """
    return {
        "id": task.id,
        "content": task.content,
        "description": task.description,
        "is_completed": task.is_completed,
        "priority": task.priority,
        "project_id": task.project_id,
        "section_id": task.section_id,
        "parent_id": task.parent_id,
        "order": task.order,
        "labels": task.labels,
        "due": task.due.to_dict() if task.due else None,
        "url": task.url,
        "created_at": task.created_at,
        "creator_id": task.creator_id,
        "assignee_id": task.assignee_id,
        "assigner_id": task.assigner_id
    }


def project_to_dict(project: Project) -> Dict[str, Any]:
    """
    Convert a Project object to a dictionary for JSON serialization.

    Parameters
    ----------
    project : Project
        The project object from the Todoist SDK

    Returns
    -------
    Dict[str, Any]
        Dictionary representation of the project
    """
    return {
        "id": project.id,
        "name": project.name,
        "order": project.order,
        "color": project.color,
        "is_shared": project.is_shared,
        "is_favorite": project.is_favorite,
        "is_inbox_project": project.is_inbox_project,
        "view_style": project.view_style,
        "url": project.url,
        "parent_id": project.parent_id
    }


def label_to_dict(label: Label) -> Dict[str, Any]:
    """
    Convert a Label object to a dictionary for JSON serialization.

    Parameters
    ----------
    label : Label
        The label object from the Todoist SDK

    Returns
    -------
    Dict[str, Any]
        Dictionary representation of the label
    """
    return {
        "id": label.id,
        "name": label.name,
        "color": label.color,
        "order": label.order,
        "is_favorite": label.is_favorite
    }


@mcp.tool()
async def get_tasks(
    project_id: Optional[str] = None,
    section_id: Optional[str] = None,
    label: Optional[str] = None,
    filter_expr: Optional[str] = None,
    lang: Optional[str] = None,
    ids: Optional[List[str]] = None
) -> str:
    """
    Retrieve tasks from Todoist with optional filtering.

    This tool fetches active tasks from the Todoist account. Filters can be added
    for project, section, label, or using Todoist's filter expressions. More details
    on filtering can be found here: https://www.todoist.com/help/articles/introduction-to-filters-V98wIH

    Parameters
    ----------
    project_id : Optional[str]
        Filter tasks by project ID
    section_id : Optional[str]
        Filter tasks by section ID
    label : Optional[str]
        Filter tasks by label name
    filter_expr : Optional[str]
        Todoist filter expression (e.g., "today", "overdue", "@work")
    lang : Optional[str]
        Language for filter parsing (default: "en")
    ids : Optional[List[str]]
        Specific task IDs to retrieve

    Returns
    -------
    str
        JSON string containing the list of tasks

    Examples
    --------
    Get all tasks:
        get_tasks()

    Get tasks for a specific project:
        get_tasks(project_id="12345")

    Get tasks with a specific label:
        get_tasks(label="work")

    Get tasks using filter expressions:
        get_tasks(filter_expr="today")
        get_tasks(filter_expr="overdue")
        get_tasks(filter_expr="p1")  # Priority 1 tasks
    """
    try:
        api = get_api()

        logger.info(f"Fetching tasks with filters - project_id: {project_id}, section_id: {section_id}, label: {label}, filter: {filter_expr}")

        if filter_expr:
            tasks_paginator = api.filter_tasks(
                query=filter_expr,
                lang=lang
            )
        else:
            tasks_paginator = api.get_tasks(
                project_id=project_id,
                section_id=section_id,
                label=label,
                ids=ids
            )

        formatted_tasks = [task_to_dict(task) for task in list(tasks_paginator)[0]]

        result = {
            "tasks": formatted_tasks,
            "count": len(formatted_tasks)
        }

        logger.info(f"Retrieved {len(formatted_tasks)} tasks")
        return json.dumps(result, indent=2, ensure_ascii=False, default=str)

    except Exception as e:
        logger.error(f"Error getting tasks: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def create_task(
    content: str,
    description: Optional[str] = None,
    project_id: Optional[str] = None,
    section_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    order: Optional[int] = None,
    labels: Optional[List[str]] = None,
    priority: Optional[int] = None,
    due_string: Optional[str] = None,
    due_date: Optional[str] = None,
    due_datetime: Optional[str] = None,
    due_lang: Optional[str] = None,
    assignee_id: Optional[str] = None
) -> str:
    """
    Create a new task in Todoist.

    This tool creates a new task with the specified content and optional parameters
    using the official Todoist Python SDK.

    Parameters
    ----------
    content : str
        The task content/title (required)
    description : Optional[str]
        Task description
    project_id : Optional[str]
        Project ID to add the task to
    section_id : Optional[str]
        Section ID within the project
    parent_id : Optional[str]
        Parent task ID for creating subtasks
    order : Optional[int]
        Task order in the project
    labels : Optional[List[str]]
        List of label names to assign
    priority : Optional[int]
        Task priority (1=normal, 2=high, 3=very high, 4=urgent)
    due_string : Optional[str]
        Human-readable due date (e.g., "tomorrow", "next Monday")
    due_date : Optional[str]
        Due date in YYYY-MM-DD format
    due_datetime : Optional[str]
        Due datetime in RFC3339 format
    due_lang : Optional[str]
        Language for parsing due_string
    assignee_id : Optional[str]
        User ID to assign the task to

    Returns
    -------
    str
        JSON string containing the created task information

    Examples
    --------
    Create a simple task:
        create_task("Buy groceries")

    Create a task with due date:
        create_task("Finish report", due_string="tomorrow")

    Create a high-priority task:
        create_task("Important meeting", priority=3)

    Create a task with labels:
        create_task("Review code", labels=["work", "urgent"])
    """
    try:
        api = get_api()

        logger.info(f"Creating task: {content}")

        task = api.add_task(
            content=content,
            description=description,
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            order=order,
            labels=labels,
            priority=priority,
            due_string=due_string,
            due_date=due_date,
            due_datetime=due_datetime,
            due_lang=due_lang,
            assignee_id=assignee_id
        )

        result = task_to_dict(task)
        logger.info(f"Task created successfully with ID: {task.id}")
        return json.dumps(result, indent=2, ensure_ascii=False, default=str)

    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def update_task(
    task_id: str,
    content: Optional[str] = None,
    description: Optional[str] = None,
    labels: Optional[List[str]] = None,
    priority: Optional[int] = None,
    due_string: Optional[str] = None,
    due_date: Optional[str] = None,
    due_datetime: Optional[str] = None,
    due_lang: Optional[str] = None,
    assignee_id: Optional[str] = None
) -> str:
    """
    Update an existing task in Todoist.

    This tool updates the specified task with new values for the provided parameters
    using the official Todoist Python SDK.

    Parameters
    ----------
    task_id : str
        The ID of the task to update (required)
    content : Optional[str]
        New task content/title
    description : Optional[str]
        New task description
    labels : Optional[List[str]]
        New list of label names
    priority : Optional[int]
        New task priority (1=normal, 2=high, 3=very high, 4=urgent)
    due_string : Optional[str]
        New human-readable due date
    due_date : Optional[str]
        New due date in YYYY-MM-DD format
    due_datetime : Optional[str]
        New due datetime in RFC3339 format
    due_lang : Optional[str]
        Language for parsing due_string
    assignee_id : Optional[str]
        New assignee user ID

    Returns
    -------
    str
        JSON string containing the updated task information

    Examples
    --------
    Update task content:
        update_task("task_id_here", content="Updated task title")

    Change task priority:
        update_task("task_id_here", priority=4)

    Set new due date:
        update_task("task_id_here", due_string="next Friday")

    Update labels:
        update_task("task_id_here", labels=["work", "important"])
    """
    try:
        api = get_api()

        update_params = {
            k: v for k, v in {
                "content": content,
                "description": description,
                "labels": labels,
                "priority": priority,
                "due_string": due_string,
                "due_date": due_date,
                "due_datetime": due_datetime,
                "due_lang": due_lang,
                "assignee_id": assignee_id
            }.items() if v is not None
        }

        if not update_params:
            return json.dumps({"error": "No update parameters provided"}, indent=2)

        logger.info(f"Updating task {task_id}: {update_params}")

        success = api.update_task(task_id=task_id, **update_params)

        if success:
            updated_task = api.get_task(task_id=task_id)
            result = task_to_dict(updated_task)
            logger.info(f"Task {task_id} updated successfully")
            return json.dumps({"success": True, "task": result}, indent=2, ensure_ascii=False, default=str)
        else:
            return json.dumps({"error": "Update failed"}, indent=2)

    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def complete_task(task_id: str) -> str:
    """
    Mark a task as completed in Todoist.

    This tool marks the specified task as completed using the official Todoist Python SDK.
    The task will be moved to the completed tasks list and will no longer appear in active task queries.

    Parameters
    ----------
    task_id : str
        The ID of the task to complete (required)

    Returns
    -------
    str
        JSON string indicating success or containing error information

    Examples
    --------
    Complete a task:
        complete_task("task_id_here")
    """
    try:
        api = get_api()

        logger.info(f"Completing task {task_id}")

        success = api.complete_task(task_id=task_id)

        if success:
            logger.info(f"Task {task_id} completed successfully")
            return json.dumps({"success": True, "message": f"Task {task_id} completed"}, indent=2)
        else:
            return json.dumps({"error": "Failed to complete task"}, indent=2)

    except Exception as e:
        logger.error(f"Error completing task {task_id}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def reopen_task(task_id: str) -> str:
    """
    Reopen a completed task in Todoist.

    This tool reopens a previously completed task using the official Todoist Python SDK.

    Parameters
    ----------
    task_id : str
        The ID of the task to reopen (required)

    Returns
    -------
    str
        JSON string indicating success or containing error information

    Examples
    --------
    Reopen a task:
        reopen_task("task_id_here")
    """
    try:
        api = get_api()

        logger.info(f"Reopening task {task_id}")

        success = api.uncomplete_task(task_id=task_id)

        if success:
            logger.info(f"Task {task_id} reopened successfully")
            return json.dumps({"success": True, "message": f"Task {task_id} reopened"}, indent=2)
        else:
            return json.dumps({"error": "Failed to reopen task"}, indent=2)

    except Exception as e:
        logger.error(f"Error reopening task {task_id}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def delete_task(task_id: str) -> str:
    """
    Delete a task from Todoist.

    This tool permanently deletes the specified task using the official Todoist Python SDK.
    This action cannot be undone.

    Parameters
    ----------
    task_id : str
        The ID of the task to delete (required)

    Returns
    -------
    str
        JSON string indicating success or containing error information

    Examples
    --------
    Delete a task:
        delete_task("task_id_here")
    """
    try:
        api = get_api()

        logger.info(f"Deleting task {task_id}")

        success = api.delete_task(task_id=task_id)

        if success:
            logger.info(f"Task {task_id} deleted successfully")
            return json.dumps({"success": True, "message": f"Task {task_id} deleted"}, indent=2)
        else:
            return json.dumps({"error": "Failed to delete task"}, indent=2)

    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_task(task_id: str) -> str:
    """
    Get a specific task by ID from Todoist.

    This tool retrieves detailed information about a specific task using the official Todoist Python SDK.

    Parameters
    ----------
    task_id : str
        The ID of the task to retrieve (required)

    Returns
    -------
    str
        JSON string containing the task information

    Examples
    --------
    Get a specific task:
        get_task("task_id_here")
    """
    try:
        api = get_api()

        logger.info(f"Fetching task {task_id}")

        task = api.get_task(task_id=task_id)
        result = task_to_dict(task)

        return json.dumps(result, indent=2, ensure_ascii=False, default=str)

    except Exception as e:
        logger.error(f"Error getting task {task_id}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def create_project(
    name: Annotated[str, Field(min_length=1, max_length=120)],
    description: Annotated[str, Field(max_length=1024)] | None = None,
    parent_id: str | None = None,
    color: str | None = None,
    is_favorite: bool | None = None,
) -> str:
    """
    Create a new project in Todoist.

    This tool creates a new project using the official Todoist Python SDK.

    Parameters
    ----------
    name : Annotated[str, Field(min_length=1, max_length=120)]
        The name of the new project to be created, note that this can be a maximum of 120 characters.
    description : Annotated[str, Field(max_length=1024)] | None = None
        The description of the new project, maximum 1024 characters.
    parent_id : str | None = None
        The ID of the parent project. If not set, project will be created at the root.
    color : str | None = None
        The color of the new project icon. If not set, project color will be set to the workspace default.
        Color details may be found here https://developer.todoist.com/api/v1/#tag/Colors
    is_favorite : bool | None = None
        Whether the new project should be marked as a favorite or not.

    Returns
    -------
    str
        JSON string containing the created project information

    Examples
    --------
    Create a basic project:
        create_project("home-improvement")

    Create a project with a specific color:
        create_task("school-work", color="olive_green")

    Create a project with a parent project:
        create_project("reading-list", parent_id="project-parent")
    """
    try:
        api = get_api()

        logger.info(f"Creating new project: {name}")
        project = api.add_project(
            name=name,
            description=description,
            parent_id=parent_id,
            color=color,
            is_favorite=is_favorite
        )
        result = project_to_dict(project)
        return json.dumps(result, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        logger.error(f"Error creating project {name}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_projects() -> str:
    """
    Retrieve all projects from Todoist.

    This tool fetches all projects in your Todoist account using the official Todoist Python SDK,
    including project metadata like name, color, and collaboration settings.

    Returns
    -------
    str
        JSON string containing the list of projects

    Examples
    --------
    Get all projects:
        get_projects()
    """
    try:
        api = get_api()

        logger.info("Fetching projects")

        projects_paginator = api.get_projects()
        formatted_projects = [project_to_dict(project) for project in list(projects_paginator)[0]]

        result = {
            "projects": formatted_projects,
            "count": len(formatted_projects)
        }

        logger.info(f"Retrieved {len(formatted_projects)} projects")
        return json.dumps(result, indent=2, ensure_ascii=False, default=str)

    except Exception as e:
        logger.error(f"Error getting projects: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_project(project_id: str) -> str:
    """
    Get a specific project by ID from Todoist.

    This tool retrieves detailed information about a specific project using the official Todoist Python SDK.

    Parameters
    ----------
    project_id : str
        The ID of the project to retrieve (required)

    Returns
    -------
    str
        JSON string containing the project information

    Examples
    --------
    Get a specific project:
        get_project("project_id_here")
    """
    try:
        api = get_api()

        logger.info(f"Fetching project {project_id}")

        project = api.get_project(project_id=project_id)
        result = project_to_dict(project)

        return json.dumps(result, indent=2, ensure_ascii=False, default=str)

    except Exception as e:
        logger.error(f"Error getting project {project_id}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_labels() -> str:
    """
    Retrieve all labels from Todoist.

    This tool fetches all labels in your Todoist account using the official Todoist Python SDK.

    Returns
    -------
    str
        JSON string containing the list of labels

    Examples
    --------
    Get all labels:
        get_labels()
    """
    try:
        api = get_api()

        logger.info("Fetching labels")

        labels_paginator = api.get_labels()
        formatted_labels = [label_to_dict(label) for label in list(labels_paginator)[0]]

        result = {
            "labels": formatted_labels,
            "count": len(formatted_labels)
        }

        logger.info(f"Retrieved {len(formatted_labels)} labels")
        return json.dumps(result, indent=2, ensure_ascii=False, default=str)

    except Exception as e:
        logger.error(f"Error getting labels: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_comments(task_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    """
    Get comments for a task or project from Todoist.

    This tool retrieves comments for either a specific task or project using the official Todoist Python SDK.

    Parameters
    ----------
    task_id : Optional[str]
        The ID of the task to get comments for
    project_id : Optional[str]
        The ID of the project to get comments for

    Returns
    -------
    str
        JSON string containing the comments

    Examples
    --------
    Get comments for a task:
        get_comments(task_id="task_id_here")

    Get comments for a project:
        get_comments(project_id="project_id_here")
    """
    try:
        api = get_api()

        if task_id:
            logger.info(f"Fetching comments for task {task_id}")
            comments_paginator = api.get_comments(task_id=task_id)
        elif project_id:
            logger.info(f"Fetching comments for project {project_id}")
            comments_paginator = api.get_comments(project_id=project_id)
        else:
            return json.dumps({"error": "Either task_id or project_id must be provided"}, indent=2)

        # Convert paginator to list
        comments = list(comments_paginator)

        # Convert comments to dictionaries
        formatted_comments = []
        for comment in comments[0]:
            formatted_comment = {
                "id": comment.id,
                "task_id": comment.task_id,
                "project_id": comment.project_id,
                "posted_at": comment.posted_at,
                "content": comment.content,
                "attachment": comment.attachment.to_dict() if comment.attachment else None
            }
            formatted_comments.append(formatted_comment)

        result = {
            "comments": formatted_comments,
            "count": len(formatted_comments)
        }

        logger.info(f"Retrieved {len(formatted_comments)} comments")
        return json.dumps(result, indent=2, ensure_ascii=False, default=str)

    except Exception as e:
        logger.error(f"Error getting comments: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


if __name__ == "__main__":
    """
    Entry point for running the MCP server.
    
    This will start the server and handle MCP protocol communication via stdio.
    The server will run until terminated.
    """
    logger.info("Starting Todoist MCP Server")

    try:
        get_api()
        logger.info("Todoist API initialized successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    mcp.run()
