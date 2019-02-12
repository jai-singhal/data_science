import unittest
import os

def analyzeTest(filname):
    with open(filname, "r") as f:
        return sum(1 for _ in f)

class TestAnalyzerTool(unittest.TestCase):
    def setUp(self):
        self.filename = "test_analyzer.txt"
        with open(self.filename, "w") as f:
            f.write("Now we are engaged in a great civil war.\n"
                    "testing whether that nation\n"
                    "or any nation so convinced and so dedicated,\n"
                    "can long endure")
        print("setUp")
        
    def tearDown(self):
        try:
            os.remove(self.filename)
        except OSError:
            pass
        print("tearDown")

    def test_function_runs(self):
        analyzeTest(self.filename)
    
    def test_line_counts(self):
        self.assertEqual(analyzeTest(self.filename), 4)

    def test_no_such_file(self):
        with self.assertRaises(IOError):
            analyzeTest("foobar.txt")

    def test_no_delettion(self):
        self.assertTrue(os.path.exists(self.filename))

if __name__ == "__main__":
    unittest.main()
