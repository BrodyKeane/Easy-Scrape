import unittest

def run_tests():
    test_dir = '.'
    suite = unittest.defaultTestLoader.discover(test_dir)
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    run_tests()
