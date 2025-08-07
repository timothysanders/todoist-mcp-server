#!/usr/bin/env python3
"""
Test script for the Todoist MCP Server

This script provides basic functionality tests for the Todoist MCP server
using the official Todoist Python SDK.

Usage:
    python test_todoist_server.py

Environment Variables:
    TODOIST_TOKEN: Your Todoist API bearer token (required)
"""

import os
import sys
import asyncio
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional - if not available, just use system environment variables
    pass

try:
    from todoist_mcp_server import get_api
except ImportError as e:
    print(f"Error: Could not import required modules: {e}")
    print("Make sure you have installed the required dependencies:")
    print("  pip install todoist-api-python mcp pydantic python-dotenv")
    sys.exit(1)


class TodoistTester:
    """
    Test harness for the Todoist MCP server functionality.

    This class provides methods to test various Todoist operations
    using the official Todoist Python SDK.
    """

    def __init__(self):
        """Initialize the tester with a Todoist API client."""
        try:
            self.api = get_api()
            print("✅ Todoist API client initialized successfully")
        except ValueError as e:
            print(f"❌ Error initializing API client: {e}")
            sys.exit(1)

    async def test_connection(self) -> bool:
        """
        Test basic connection to Todoist API.

        Returns
        -------
        bool
            True if connection is successful, False otherwise
        """
        try:
            print("\n🔄 Testing API connection...")
            projects = list(self.api.get_projects())
            print(f"✅ Connection successful! Found {len(projects)} projects")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    async def test_get_tasks(self) -> bool:
        """
        Test retrieving tasks.

        Returns
        -------
        bool
            True if task retrieval is successful, False otherwise
        """
        try:
            print("\n🔄 Testing task retrieval...")
            tasks = list(self.api.get_tasks())
            print(f"✅ Retrieved {len(tasks)} tasks")

            if tasks:
                print(f"   Sample task: '{tasks[0][0].content}'")

            return True
        except Exception as e:
            print(f"❌ Task retrieval failed: {e}")
            return False

    async def test_get_projects(self) -> bool:
        """
        Test retrieving projects.

        Returns
        -------
        bool
            True if project retrieval is successful, False otherwise
        """
        try:
            print("\n🔄 Testing project retrieval...")
            projects = list(self.api.get_projects())
            print(f"✅ Retrieved {len(projects)} projects")

            if projects:
                print(f"   Sample project: '{projects[0][0].name}'")

            return True
        except Exception as e:
            print(f"❌ Project retrieval failed: {e}")
            return False

    async def test_get_labels(self) -> bool:
        """
        Test retrieving labels.

        Returns
        -------
        bool
            True if label retrieval is successful, False otherwise
        """
        try:
            print("\n🔄 Testing label retrieval...")
            labels = list(self.api.get_labels())
            print(f"✅ Retrieved {len(labels)} labels")

            if labels:
                print(f"   Sample label: '{labels[0][0].name}'")

            return True
        except Exception as e:
            print(f"❌ Label retrieval failed: {e}")
            return False

    async def test_create_and_delete_task(self) -> bool:
        """
        Test creating and deleting a task.

        Returns
        -------
        bool
            True if both operations are successful, False otherwise
        """
        task_id = None
        try:
            print("\n🔄 Testing task creation...")

            # Create a test task
            task = self.api.add_task(
                content="Test task from MCP server",
                description="This is a test task created by the MCP server test script"
            )

            task_id = task.id

            if not task_id:
                print("❌ Task creation failed: No task ID returned")
                return False

            print(f"✅ Task created successfully with ID: {task_id}")

            print("🔄 Testing task deletion...")

            # Delete the test task
            success = self.api.delete_task(task_id=task_id)

            if success:
                print("✅ Task deleted successfully")
                return True
            else:
                print("❌ Task deletion failed")
                return False

        except Exception as e:
            print(f"❌ Task creation/deletion failed: {e}")

            # Try to clean up the task if it was created
            if task_id:
                try:
                    print("🔄 Attempting to clean up test task...")
                    self.api.delete_task(task_id=task_id)
                    print("✅ Test task cleaned up")
                except Exception as cleanup_error:
                    print(f"⚠️  Failed to clean up test task {task_id}: {cleanup_error}")

            return False

    async def test_filters(self) -> bool:
        """
        Test task filtering functionality.

        Returns
        -------
        bool
            True if filtering works, False otherwise
        """
        try:
            print("\n🔄 Testing task filters...")

            today_tasks = list(self.api.filter_tasks(query="today"))
            print(f"✅ Today filter: {len(today_tasks)} tasks")

            overdue_tasks = list(self.api.filter_tasks(query="overdue"))
            print(f"✅ Overdue filter: {len(overdue_tasks)} tasks")

            priority_tasks = list(self.api.filter_tasks(query="p1"))
            print(f"✅ Priority 1 filter: {len(priority_tasks)} tasks")

            return True

        except Exception as e:
            print(f"❌ Filter testing failed: {e}")
            return False

    async def test_task_operations(self) -> bool:
        """
        Test complete task lifecycle (create, update, complete, reopen, delete).

        Returns
        -------
        bool
            True if all operations are successful, False otherwise
        """
        task_id = None
        try:
            print("\n🔄 Testing complete task lifecycle...")

            print("   Creating task...")
            task = self.api.add_task(
                content="Lifecycle test task",
                description="Testing complete task lifecycle",
                priority=2
            )
            task_id = task.id
            print(f"   ✅ Task created: {task_id}")

            print("   Updating task...")
            update_success = self.api.update_task(
                task_id=task_id,
                content="Updated lifecycle test task",
                priority=3
            )
            if update_success:
                print("   ✅ Task updated successfully")
            else:
                print("   ❌ Task update failed")
                return False

            print("   Completing task...")
            complete_success = self.api.complete_task(task_id=task_id)
            if complete_success:
                print("   ✅ Task completed successfully")
            else:
                print("   ❌ Task completion failed")
                return False

            print("   Reopening task...")
            reopen_success = self.api.uncomplete_task(task_id=task_id)
            if reopen_success:
                print("   ✅ Task reopened successfully")
            else:
                print("   ❌ Task reopen failed")
                return False

            print("   Deleting task...")
            delete_success = self.api.delete_task(task_id=task_id)
            if delete_success:
                print("   ✅ Task deleted successfully")
                task_id = None
            else:
                print("   ❌ Task deletion failed")
                return False

            print("✅ Complete task lifecycle test passed")
            return True

        except Exception as e:
            print(f"❌ Task lifecycle test failed: {e}")

            if task_id:
                try:
                    print("🔄 Attempting to clean up test task...")
                    self.api.delete_task(task_id=task_id)
                    print("✅ Test task cleaned up")
                except Exception as cleanup_error:
                    print(f"⚠️  Failed to clean up test task {task_id}: {cleanup_error}")

            return False

    async def test_get_specific_task(self) -> bool:
        """
        Test retrieving a specific task by ID.

        Returns
        -------
        bool
            True if the test is successful, False otherwise
        """
        task_id = None
        try:
            print("\n🔄 Testing specific task retrieval...")

            task = self.api.add_task(content="Test task for retrieval")
            task_id = task.id

            retrieved_task = self.api.get_task(task_id=task_id)

            if retrieved_task and retrieved_task.id == task_id:
                print(f"✅ Successfully retrieved task: '{retrieved_task.content}'")

                self.api.delete_task(task_id=task_id)
                return True
            else:
                print("❌ Failed to retrieve the correct task")
                return False

        except Exception as e:
            print(f"❌ Specific task retrieval failed: {e}")

            if task_id:
                try:
                    self.api.delete_task(task_id=task_id)
                except (requests.exceptions.RequestException, ValueError, KeyError):
                    pass

            return False

    async def test_comments(self) -> bool:
        """
        Test retrieving comments for tasks and projects.

        Returns
        -------
        bool
            True if the test is successful, False otherwise
        """
        task_id = None
        try:
            print("\n🔄 Testing comments functionality...")

            task = self.api.add_task(content="Task for comment testing")
            task_id = task.id

            comments = list(self.api.get_comments(task_id=task_id))
            print(f"✅ Retrieved {len(comments)} comments for task")

            projects = list(self.api.get_projects())
            if projects:
                project_comments = list(self.api.get_comments(project_id=projects[0][0].id))
                print(f"✅ Retrieved {len(project_comments)} comments for project")

            self.api.delete_task(task_id=task_id)
            return True

        except Exception as e:
            print(f"❌ Comments test failed: {e}")

            if task_id:
                try:
                    self.api.delete_task(task_id=task_id)
                except (requests.exceptions.RequestException, ValueError, KeyError):
                    pass

            return False

    async def run_all_tests(self) -> bool:
        """
        Run all tests and return overall success status.

        Returns
        -------
        bool
            True if all tests pass, False if any test fails
        """
        print("🚀 Starting Todoist MCP Server Tests")
        print("=" * 50)

        tests = [
            ("Connection", self.test_connection),
            ("Get Tasks", self.test_get_tasks),
            ("Get Projects", self.test_get_projects),
            ("Get Labels", self.test_get_labels),
            ("Create/Delete Task", self.test_create_and_delete_task),
            ("Task Filters", self.test_filters),
            ("Task Lifecycle", self.test_task_operations),
            ("Specific Task Retrieval", self.test_get_specific_task),
            ("Comments", self.test_comments)
        ]

        results = []

        for test_name, test_func in tests:
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Test '{test_name}' crashed: {e}")
                results.append((test_name, False))

        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print("=" * 50)

        passed = 0
        total = len(results)

        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - {test_name}")
            if success:
                passed += 1

        print("-" * 50)
        print(f"Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Your Todoist MCP server is working correctly.")
            return True
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
            return False


async def main():
    """
    Main function to run the tests.
    """
    token = os.getenv("TODOIST_TOKEN")
    if not token:
        print("❌ Error: TODOIST_TOKEN environment variable is not set")
        print("\nTo run these tests:")
        print("1. Get your API token from https://app.todoist.com/app/settings/integrations/developer")
        print("2. Either:")
        print("   a) Create a .env file with: TODOIST_TOKEN=your_token_here")
        print("   b) Set the environment variable: export TODOIST_TOKEN='your_token_here'")
        print("3. Run this script again")
        sys.exit(1)

    tester = TodoistTester()
    success = await tester.run_all_tests()

    if success:
        print("\n🎯 Next steps:")
        print("1. Your server is ready to use with Claude Desktop")
        print("2. Add the server configuration to claude_desktop_config.json")
        print("3. Restart Claude Desktop")
        print("4. Try asking Claude to:")
        print("   - 'Show me my tasks for today'")
        print("   - 'Create a task to buy groceries'")
        print("   - 'List all my projects'")
        print("   - 'What are my overdue tasks?'")
        sys.exit(0)
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check your TODOIST_TOKEN is valid")
        print("2. Verify your internet connection")
        print("3. Ensure you have the required Python packages:")
        print("   pip install todoist-api-python mcp pydantic python-dotenv")
        print("4. Review any error messages above")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)