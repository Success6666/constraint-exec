"""Small executable contracts for the Sol interaction regression suite."""
from __future__ import annotations

FIXTURES = {
    "ratio-fix": {
        "source": '''SENTINEL = "user edit: keep me"

def ratio(part, total):
    return part / total
''',
        "tests": '''import unittest
import app
class Contract(unittest.TestCase):
    def test_zero(self): self.assertEqual(app.ratio(3, 0), 0.0)
    def test_normal(self): self.assertEqual(app.ratio(3, 4), 0.75)
    def test_negative(self): self.assertEqual(app.ratio(-2, 4), -0.5)
    def test_user_edit(self): self.assertEqual(app.SENTINEL, "user edit: keep me")
''',
    },
    "persistent-todo": {
        "source": '''import json
from pathlib import Path

SENTINEL = "user edit: keep me"

def save_items(path, items):
    pass

def load_items(path):
    return []
''',
        "tests": '''import unittest
import tempfile
from pathlib import Path
import app
class Contract(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "nested" / "todo.json"
            items = [{"id": 1, "title": "买牛奶", "done": False}]
            app.save_items(p, items)
            self.assertEqual(app.load_items(p), items)
            self.assertEqual(app.load_items(p), items)
            app.save_items(p, [])
            self.assertEqual(app.load_items(p), [])
    def test_missing(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(app.load_items(Path(d) / "absent.json"), [])
    def test_bad_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.json"; p.write_text("invalid")
            with self.assertRaises(ValueError): app.load_items(p)
    def test_user_edit(self): self.assertEqual(app.SENTINEL, "user edit: keep me")
''',
    },
    "csv-summary": {
        "source": '''SENTINEL = "user edit: keep me"

def summarize(text):
    return {}
''',
        "tests": '''import unittest
import app
class Contract(unittest.TestCase):
    def test_sum(self):
        text = 'category,amount\\nfood,2.5\\nfood,1.5\\ntravel,-1\\n,9\\nfood,invalid\\n"a,b",3\\nfood,\\n'
        self.assertEqual(app.summarize(text), {"food": 4.0, "travel": -1.0, "a,b": 3.0})
    def test_empty(self): self.assertEqual(app.summarize("category,amount\\n"), {})
    def test_unicode(self): self.assertEqual(app.summarize("category,amount\\n餐饮,3\\n"), {"餐饮": 3.0})
    def test_user_edit(self): self.assertEqual(app.SENTINEL, "user edit: keep me")
''',
    },
    "stable-dedup": {
        "source": '''SENTINEL = "user edit: keep me"

def dedup(values):
    return list(set(values))
''',
        "tests": '''import unittest
import app
class Contract(unittest.TestCase):
    def test_order(self): self.assertEqual(app.dedup([3, 1, 3, 2, 1]), [3, 1, 2])
    def test_empty(self): self.assertEqual(app.dedup([]), [])
    def test_unicode(self): self.assertEqual(app.dedup(["牛奶", "面包", "牛奶"]), ["牛奶", "面包"])
    def test_immutable(self):
        x = [2, 1, 2]; app.dedup(x); self.assertEqual(x, [2, 1, 2])
    def test_user_edit(self): self.assertEqual(app.SENTINEL, "user edit: keep me")
''',
    },
}
