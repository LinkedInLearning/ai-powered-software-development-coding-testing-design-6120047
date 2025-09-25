import unittest
from integration_tests import TodoItem


class TestTodoItem(unittest.TestCase):
    """Unit tests for the TodoItem class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.todo = TodoItem("Test task")

    def test_init_with_title(self):
        """Test TodoItem initialization with a title."""
        todo = TodoItem("Buy groceries")
        self.assertEqual(todo.title, "Buy groceries")
        self.assertFalse(todo.completed)

    def test_init_with_empty_title(self):
        """Test TodoItem initialization with an empty title."""
        todo = TodoItem("")
        self.assertEqual(todo.title, "")
        self.assertFalse(todo.completed)

    def test_init_with_whitespace_title(self):
        """Test TodoItem initialization with whitespace-only title."""
        todo = TodoItem("   ")
        self.assertEqual(todo.title, "   ")
        self.assertFalse(todo.completed)

    def test_mark_complete(self):
        """Test marking a todo item as complete."""
        self.assertFalse(self.todo.completed)
        self.todo.mark_complete()
        self.assertTrue(self.todo.completed)

    def test_mark_complete_multiple_times(self):
        """Test calling mark_complete multiple times."""
        self.todo.mark_complete()
        self.assertTrue(self.todo.completed)
        
        # Calling mark_complete again should still be complete
        self.todo.mark_complete()
        self.assertTrue(self.todo.completed)

    def test_mark_incomplete(self):
        """Test marking a todo item as incomplete."""
        # First mark as complete
        self.todo.mark_complete()
        self.assertTrue(self.todo.completed)
        
        # Then mark as incomplete
        self.todo.mark_incomplete()
        self.assertFalse(self.todo.completed)

    def test_mark_incomplete_multiple_times(self):
        """Test calling mark_incomplete multiple times."""
        self.todo.mark_incomplete()
        self.assertFalse(self.todo.completed)
        
        # Calling mark_incomplete again should still be incomplete
        self.todo.mark_incomplete()
        self.assertFalse(self.todo.completed)

    def test_mark_complete_then_incomplete(self):
        """Test toggling between complete and incomplete states."""
        # Start incomplete
        self.assertFalse(self.todo.completed)
        
        # Mark complete
        self.todo.mark_complete()
        self.assertTrue(self.todo.completed)
        
        # Mark incomplete
        self.todo.mark_incomplete()
        self.assertFalse(self.todo.completed)
        
        # Mark complete again
        self.todo.mark_complete()
        self.assertTrue(self.todo.completed)

    def test_repr_incomplete(self):
        """Test string representation of incomplete todo item."""
        todo = TodoItem("Test task")
        expected = "[✗] Test task"
        self.assertEqual(repr(todo), expected)
        self.assertEqual(str(todo), expected)

    def test_repr_complete(self):
        """Test string representation of complete todo item."""
        todo = TodoItem("Test task")
        todo.mark_complete()
        expected = "[✓] Test task"
        self.assertEqual(repr(todo), expected)
        self.assertEqual(str(todo), expected)

    def test_repr_with_empty_title(self):
        """Test string representation with empty title."""
        todo = TodoItem("")
        expected = "[✗] "
        self.assertEqual(repr(todo), expected)

    def test_repr_with_special_characters(self):
        """Test string representation with special characters in title."""
        todo = TodoItem("Task with émojis 🎉 and symbols @#$%")
        expected = "[✗] Task with émojis 🎉 and symbols @#$%"
        self.assertEqual(repr(todo), expected)

    def test_repr_with_very_long_title(self):
        """Test string representation with very long title."""
        long_title = "A" * 1000
        todo = TodoItem(long_title)
        expected = f"[✗] {long_title}"
        self.assertEqual(repr(todo), expected)

    def test_multiple_instances_independence(self):
        """Test that multiple TodoItem instances are independent."""
        todo1 = TodoItem("Task 1")
        todo2 = TodoItem("Task 2")
        
        # Mark first as complete
        todo1.mark_complete()
        self.assertTrue(todo1.completed)
        self.assertFalse(todo2.completed)
        
        # Mark second as complete
        todo2.mark_complete()
        self.assertTrue(todo1.completed)
        self.assertTrue(todo2.completed)
        
        # Mark first as incomplete
        todo1.mark_incomplete()
        self.assertFalse(todo1.completed)
        self.assertTrue(todo2.completed)

    def test_title_modification(self):
        """Test that title can be modified after creation."""
        todo = TodoItem("Original title")
        self.assertEqual(todo.title, "Original title")
        
        # Modify title
        todo.title = "Modified title"
        self.assertEqual(todo.title, "Modified title")
        
        # String representation should reflect new title
        expected = "[✗] Modified title"
        self.assertEqual(repr(todo), expected)

    def test_completed_state_modification(self):
        """Test that completed state can be modified directly."""
        todo = TodoItem("Test task")
        self.assertFalse(todo.completed)
        
        # Modify completed state directly
        todo.completed = True
        self.assertTrue(todo.completed)
        
        # String representation should reflect new state
        expected = "[✓] Test task"
        self.assertEqual(repr(todo), expected)


if __name__ == '__main__':
    unittest.main()
