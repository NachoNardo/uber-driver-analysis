import sys
import unittest
from pathlib import Path


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    suite = unittest.defaultTestLoader.discover("tests/unit", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
