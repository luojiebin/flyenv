#!/usr/bin/env python
import unittest
import os

from flyenv import flyenv


class FakeArgs(object):

    def __init__(self, pairs=[], keys=[], key=None):
        self.pairs = pairs
        self.keys = keys
        self.key = key


class FlyenvTestCase(unittest.TestCase):

    def call_flyenv(self, args):
        parser = flyenv.get_parser()
        args = parser.parse_args()
        return flyenv.flyenv(args)

    def setUp(self):
        self.inital_env = {}
        self.inital_env['apple'] = 1
        self.inital_env['pear'] = 2
        self.inital_env['orange'] = 3
        self.inital_env['banana'] = 4
        self.inital_env['watermelon'] = ''
        with open(flyenv.ENV_FILE, 'w') as f:
            for key, val in self.inital_env.items():
                f.write('{key}={val}\n'.format(key=key, val=val))

    def tearDown(self):
        pass
        # os.remove(flyenv.ENV_FILE)

    def test_set_one_env(self):
        pairs = ['a=b']
        args = FakeArgs(pairs=pairs)
        flyenv.set(args)
        file_pairs = flyenv._parse_file(flyenv.ENV_FILE)
        self.assertEqual(os.environ.get('a'), 'b',
                         'setted environment variable not found by os.environ')

        self.assertIn('a', file_pairs,
                      'setted environment variable not found in file')
        self.assertEqual(file_pairs['a'], 'b',
                         'environment variable value not corrent in file')

    def test_set_multiple_env(self):
        pairs = ['a=b', 'c=e', 'd=f']
        args = FakeArgs(pairs=pairs)
        flyenv.set(args)
        file_pairs = flyenv._parse_file(flyenv.ENV_FILE)

        self.assertEqual(os.environ.get('a'), 'b',
                         'setted environment variable not found by os.environ')
        self.assertEqual(os.environ.get('c'), 'e',
                         'setted environment variable not found by os.environ')
        self.assertEqual(os.environ.get('d'), 'f',
                         'setted environment variable not found by os.environ')

        self.assertIn('a', file_pairs,
                      'setted environment variable not found in file')
        self.assertIn('c', file_pairs,
                      'setted environment variable not found in file')
        self.assertIn('d', file_pairs,
                      'setted environment variable not found in file')

        self.assertEqual(file_pairs['a'], 'b',
                         'environment variable value not corrent in file')
        self.assertEqual(file_pairs['c'], 'e',
                         'environment variable value not corrent in file')
        self.assertEqual(file_pairs['d'], 'f',
                         'environment variable value not corrent in file')

    def test_unset_one_env(self):
        args = FakeArgs(keys=['apple'])
        flyenv.unset(args)
        file_pairs = flyenv._parse_file(flyenv.ENV_FILE)

        self.assertEqual(file_pairs.get('apple'), '')

    def test_unset_multiple_env(self):
        args = FakeArgs(keys=['apple', 'orange', 'pear'])
        flyenv.unset(args)
        file_pairs = flyenv._parse_file(flyenv.ENV_FILE)

        self.assertEqual(file_pairs['apple'], '',
                         'unsetted environment variable should has empty value')
        self.assertEqual(file_pairs['orange'], '',
                         'unsetted environment variable should has empty value')
        self.assertEqual(file_pairs['pear'], '',
                         'unsetted environment variable should has empty value')

    def test_delete_one_env(self):
        args = FakeArgs(keys=['apple'])
        flyenv.delete(args)
        file_pairs = flyenv._parse_file(flyenv.ENV_FILE)

        self.assertNotIn('apple', file_pairs)

    def test_delete_multiple_env(self):
        args = FakeArgs(keys=['apple', 'orange', 'pear'])
        flyenv.delete(args)
        file_pairs = flyenv._parse_file(flyenv.ENV_FILE)

        self.assertNotIn('apple', file_pairs,
                         'deleteted environment variable still in file')
        self.assertNotIn('orange', file_pairs,
                         'deleteted environment variable still in file')
        self.assertNotIn('pear', file_pairs,
                         'deleteted environment variable still in file')

    def test_get(self):
        args = FakeArgs(key='apple')

        self.assertEqual(flyenv._get(args), '1',
                         'get command get the wrong value')

    def test__list_env(self):
        args = FakeArgs()
        wanted_pairs = ['apple=1', 'banana=4',
                        'orange=3', 'pear=2', 'watermelon=']
        list_pairs = flyenv._list_env(args)

        self.assertListEqual(wanted_pairs, list_pairs,
                             'list envrironment variables not correct')

    def test_require_env(self):
        args = FakeArgs()
        wanted_env = ['watermelon']

        self.assertListEqual(wanted_env,
                             flyenv._required_environment_variable(args),
                             'require environment variables not correct')

    def test_clear_env(self):
        args = FakeArgs()
        flyenv.clear(args)
        pairs = flyenv._parse_file(flyenv.ENV_FILE)

        for val in pairs.values():
            self.assertEqual(
                val, '', "cleared environment variables's value should be empty string")

    def test_load_env(self):
        args = FakeArgs()
        flyenv.load(args)
        for key, val in self.inital_env.items():
            self.assertEqual(os.environ.get(key, None), str(val),
                             'env file not load correctly, want: {}, given: {}'.format(val, os.environ.get(key, None)))


if __name__ == '__main__':
    unittest.main()
