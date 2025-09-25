import unittest
import os
import csv
import tempfile
import shutil
from unittest.mock import patch, mock_open
from expense_tracker import load_expenses, CSV_FILE


class TestLoadExpenses(unittest.TestCase):
    """Unit tests for the load_expenses function."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.original_csv_file = CSV_FILE
        # Change to test directory to avoid conflicts with real CSV file
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up after each test method."""
        # Clean up any test files
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        # Return to original directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # Remove test directory
        shutil.rmtree(self.test_dir)

    def test_load_expenses_file_not_exists(self):
        """Test load_expenses when CSV file does not exist."""
        # Ensure file doesn't exist
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        
        result = load_expenses()
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_load_expenses_empty_file(self):
        """Test load_expenses with an empty CSV file."""
        # Create empty CSV file
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            pass
        
        result = load_expenses()
        self.assertEqual(result, [])

    def test_load_expenses_file_with_header_only(self):
        """Test load_expenses with CSV file containing only headers."""
        # Create CSV file with headers only
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
        
        result = load_expenses()
        self.assertEqual(result, [])

    def test_load_expenses_single_expense(self):
        """Test load_expenses with a single expense record."""
        # Create CSV file with one expense
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': 'Coffee', 'amount': '3.50', 'category': 'Food'})
        
        result = load_expenses()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Coffee')
        self.assertEqual(result[0]['amount'], '3.50')
        self.assertEqual(result[0]['category'], 'Food')

    def test_load_expenses_multiple_expenses(self):
        """Test load_expenses with multiple expense records."""
        # Create CSV file with multiple expenses
        test_data = [
            {'name': 'Coffee', 'amount': '3.50', 'category': 'Food'},
            {'name': 'Gas', 'amount': '45.00', 'category': 'Transportation'},
            {'name': 'Movie', 'amount': '12.00', 'category': 'Entertainment'}
        ]
        
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerows(test_data)
        
        result = load_expenses()
        self.assertEqual(len(result), 3)
        
        # Check that all expenses are loaded correctly
        for i, expected_expense in enumerate(test_data):
            self.assertEqual(result[i]['name'], expected_expense['name'])
            self.assertEqual(result[i]['amount'], expected_expense['amount'])
            self.assertEqual(result[i]['category'], expected_expense['category'])

    def test_load_expenses_with_special_characters(self):
        """Test load_expenses with special characters in data."""
        # Create CSV file with special characters
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': 'Café & Restaurant', 'amount': '25.50', 'category': 'Food & Dining'})
            writer.writerow({'name': 'Movie "The Avengers"', 'amount': '15.00', 'category': 'Entertainment'})
        
        result = load_expenses()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Café & Restaurant')
        self.assertEqual(result[0]['category'], 'Food & Dining')
        self.assertEqual(result[1]['name'], 'Movie "The Avengers"')

    def test_load_expenses_with_unicode_characters(self):
        """Test load_expenses with Unicode characters."""
        # Create CSV file with Unicode characters
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': 'Sushi 🍣', 'amount': '30.00', 'category': 'Food'})
            writer.writerow({'name': 'Café', 'amount': '4.50', 'category': 'Food'})
        
        result = load_expenses()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Sushi 🍣')
        self.assertEqual(result[1]['name'], 'Café')

    def test_load_expenses_with_empty_fields(self):
        """Test load_expenses with empty fields in CSV data."""
        # Create CSV file with empty fields
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': '', 'amount': '10.00', 'category': 'Food'})
            writer.writerow({'name': 'Coffee', 'amount': '', 'category': 'Food'})
            writer.writerow({'name': 'Gas', 'amount': '20.00', 'category': ''})
        
        result = load_expenses()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['name'], '')
        self.assertEqual(result[0]['amount'], '10.00')
        self.assertEqual(result[1]['amount'], '')
        self.assertEqual(result[2]['category'], '')

    def test_load_expenses_with_whitespace(self):
        """Test load_expenses with leading/trailing whitespace in data."""
        # Create CSV file with whitespace
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': '  Coffee  ', 'amount': '  3.50  ', 'category': '  Food  '})
        
        result = load_expenses()
        self.assertEqual(len(result), 1)
        # Note: CSV reader preserves whitespace, so we expect it to be there
        self.assertEqual(result[0]['name'], '  Coffee  ')
        self.assertEqual(result[0]['amount'], '  3.50  ')
        self.assertEqual(result[0]['category'], '  Food  ')

    def test_load_expenses_with_quoted_fields(self):
        """Test load_expenses with quoted fields containing commas."""
        # Create CSV file with quoted fields
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': 'Pizza, Soda, and Chips', 'amount': '15.99', 'category': 'Food & Drinks'})
        
        result = load_expenses()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Pizza, Soda, and Chips')
        self.assertEqual(result[0]['category'], 'Food & Drinks')

    def test_load_expenses_file_permission_error(self):
        """Test load_expenses when file exists but cannot be read."""
        # Create a file and then make it unreadable
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': 'Test', 'amount': '10.00', 'category': 'Test'})
        
        # Make file unreadable (this might not work on all systems)
        try:
            os.chmod(CSV_FILE, 0o000)
            with self.assertRaises(PermissionError):
                load_expenses()
        except (OSError, PermissionError):
            # If we can't make the file unreadable, skip this test
            self.skipTest("Cannot make file unreadable on this system")
        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(CSV_FILE, 0o644)
            except OSError:
                pass

    def test_load_expenses_encoding_handling(self):
        """Test load_expenses with different encoding scenarios."""
        # Test with UTF-8 BOM - the load_expenses function uses utf-8 encoding
        # The BOM will be included in the first field name, which is expected behavior
        with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': 'Test', 'amount': '10.00', 'category': 'Test'})
        
        result = load_expenses()
        self.assertEqual(len(result), 1)
        
        # The BOM will be included in the first field name, so we check for that
        first_row = result[0]
        # The field name will be '\ufeffname' due to BOM
        bom_name_key = '\ufeffname'
        self.assertIn(bom_name_key, first_row)
        self.assertEqual(first_row[bom_name_key], 'Test')
        self.assertEqual(first_row['amount'], '10.00')
        self.assertEqual(first_row['category'], 'Test')

    def test_load_expenses_return_type(self):
        """Test that load_expenses always returns a list."""
        # Test with no file
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        result = load_expenses()
        self.assertIsInstance(result, list)
        
        # Test with empty file
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            pass
        result = load_expenses()
        self.assertIsInstance(result, list)
        
        # Test with data
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            writer.writerow({'name': 'Test', 'amount': '10.00', 'category': 'Test'})
        result = load_expenses()
        self.assertIsInstance(result, list)

    def test_load_expenses_large_file(self):
        """Test load_expenses with a large number of records."""
        # Create CSV file with many records
        num_records = 1000
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'amount', 'category'])
            writer.writeheader()
            for i in range(num_records):
                writer.writerow({
                    'name': f'Expense {i}',
                    'amount': f'{i}.00',
                    'category': f'Category {i % 10}'
                })
        
        result = load_expenses()
        self.assertEqual(len(result), num_records)
        
        # Check first and last records
        self.assertEqual(result[0]['name'], 'Expense 0')
        self.assertEqual(result[-1]['name'], f'Expense {num_records - 1}')


if __name__ == '__main__':
    unittest.main()
