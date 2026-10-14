import json
import unittest
from catalog_store import ROWS, page

class CatalogTests(unittest.TestCase):
    def test_all_records_exactly_once(self):
        offset, ids, calls = 0, [], 0
        while offset is not None:
            result = page(offset)
            self.assertLessEqual(len(json.dumps(result, ensure_ascii=False).encode('utf-8')), 4096)
            ids.extend(row['id'] for row in result['items'])
            offset = result['next_cursor']
            calls += 1
            self.assertLess(calls, 1000)
        self.assertEqual(ids, [r['id'] for r in ROWS])
        self.assertEqual(ids[-1], 'Q1000')

    def test_invalid_offsets(self):
        for value in [-1, 1001]:
            with self.assertRaises(ValueError): page(value)

    def test_last_record(self):
        self.assertEqual(page(999)['items'][0]['name'], 'Active checking accounts')

if __name__ == '__main__': unittest.main()
