from io import StringIO
import unittest
import bspentreader

class TestBspEntReader(unittest.TestCase):
    
    def test_read_entities(self):
        raw = '{\n"classname" "func_test"\n"origin" "32 32 72"\n"key" "value"\n}'
        expected = {
            "classname": "func_test",
            "origin": "32 32 72",
            "key": "value"
        }

        actual = bspentreader.read_entities(StringIO(raw))
        self.assertDictEqual(actual[0], expected)

    def test_read_entities_linebreak(self):
        raw = '{\n"classname" "func_test"\n"origin" "32 32 72"\n"key" "value"\n"_light" "255 255 128\r\n200"\n}'
        expected = {
            "classname": "func_test",
            "origin": "32 32 72",
            "key": "value",
            "_light": "255 255 128\r\n200"
        }

        actual = bspentreader.read_entities(StringIO(raw))
        self.assertDictEqual(actual[0], expected)

if __name__ == '__main__':
    unittest.main()
