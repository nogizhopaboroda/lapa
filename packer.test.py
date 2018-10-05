import unittest
import os

from unittest.mock import patch

from packer import DEFAULT_CONFIG, load_config, enhance_config, exec_command, install_dependencies
import packer

cwd = os.getcwd()


# handle config

class LoadConfig(unittest.TestCase):
    def test_example_1(self):
        config = load_config(os.path.join(cwd, 'example/python/simple'))
        self.assertNotEqual(config, {})

    def test_example_2(self):
        config = load_config(os.path.join(cwd, 'example/node/lambda_plus_edge'))
        self.assertNotEqual(config, {})
        self.assertEqual(len(config), 2)

class EnhanceConfig(unittest.TestCase):
    def test_casts_list_of_configs(self):
        config = enhance_config({})
        self.assertEqual(type(config), list)

    def test_default_values(self):
        [config] = enhance_config({
            'tempDir': 'bar'
        })
        for prop, value in DEFAULT_CONFIG.items():
            self.assertEqual(config[prop], DEFAULT_CONFIG[prop])
        self.assertEqual(config['tempDir'], 'bar')

    def test_casts_list_of_needed_properties(self):
        [config] = enhance_config({
            'files': '*',
            'ignore': '*',
            'dependencies': 'all',
        })
        self.assertEqual(config['files'], ['*'])
        self.assertEqual(config['ignore'], ['*'])
        self.assertEqual(config['dependencies'], ['all'])


# environments
@patch('packer.exec_command')
class InstallDependencies(unittest.TestCase):

    def test_case_1(self, test_patch):
        test_patch.return_value = 'ok'
        ret = install_dependencies({"environment": "node", "dependencies": ["foo", "baz"], "tempDir": "/bar"})
        test_patch.assert_called_with('npm install foo baz', cwd = '/bar')


if __name__ == '__main__':
    unittest.main()
