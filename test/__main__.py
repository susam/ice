import unittest
suite = unittest.defaultTestLoader.discover('.')
unittest.TextTestRunner(verbosity=2).run(suite)
