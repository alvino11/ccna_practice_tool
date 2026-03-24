import unittest
import os
from main import get_validated_input, safe_load_json


class TestCCNAProject(unittest.TestCase):
    """
    Unit tests for core utility functions used in the CCNA Practice Tool.
    These tests focus on validating input handling and file-loading resilience.
    """

    # ---------- Tests for safe_load_json ----------

    def test_safe_load_json_missing_file(self):
        """
        Verify that safe_load_json returns fallback data
        when the specified file does not exist.

        This ensures the application does not crash and
        instead uses a safe default configuration.
        """
        fallback = {"limit": 10}

        result = safe_load_json("non_existent_file.json", fallback)

        self.assertEqual(result, fallback)

    def test_safe_load_json_corrupted_file(self):
        """
        Ensure fallback data is returned when the JSON file is corrupted
        and cannot be parsed.
        """
        temp_file = "corrupt.json"

        # Create intentionally invalid JSON content
        with open(temp_file, "w") as f:
            f.write("{ invalid json... ")

        fallback = {"status": "default"}

        result = safe_load_json(temp_file, fallback)

        self.assertEqual(result, fallback)

        # Clean up temporary file after test execution
        if os.path.exists(temp_file):
            os.remove(temp_file)

# ---------- Tests for get_validated_input ----------

if __name__ == '__main__':
    unittest.main()