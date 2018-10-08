import unittest
import os

from unittest.mock import patch, call

from packer import DEFAULT_CONFIG, load_config, enhance_config, copy_files, exec_command, install_dependencies
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


# copy files
@patch('packer.ensure_directories')
@patch('shutil.copy')
class CopyFiles(unittest.TestCase):

    def test_case_1(self, copy_patch, ensure_directories_patch):
        copy_patch.return_value = 'ok'
        ensure_directories_patch.return_value = 'ok'
        copy_files(['foo.py'], '/bar', cwd = '', map_dirs = {})
        copy_patch.assert_called_with('foo.py', '/bar/foo.py')

    def test_case_2(self, copy_patch, ensure_directories_patch):
        copy_patch.return_value = 'ok'
        ensure_directories_patch.return_value = 'ok'
        copy_files(
                ['foo.py', 'bar.py', 'src/bla.py', 'src2/quux', 'src3/booz.py'], '/bar',
                cwd = '/mock_cwd', map_dirs = { "src": "./", "src2": "", "src3": "src_remapped" }
        )
        copy_patch.assert_has_calls([
            call('/mock_cwd/foo.py', '/bar/foo.py'),
            call('/mock_cwd/bar.py', '/bar/bar.py'),
            call('/mock_cwd/src/bla.py', '/bar/bla.py'),
            call('/mock_cwd/src2/quux', '/bar/quux'),
            call('/mock_cwd/src3/booz.py', '/bar/src_remapped/booz.py'),
        ])


# environments
@patch('packer.exec_command')
class InstallDependencies(unittest.TestCase):

    def test_case_1(self, test_patch):
        test_patch.return_value = 'ok'
        ret = install_dependencies({"environment": "node", "dependencies": ["foo", "baz"], "tempDir": "/bar"})
        test_patch.assert_called_with('npm install foo baz', cwd = '/bar', sync = False)


if __name__ == '__main__':
    unittest.main()
