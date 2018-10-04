import unittest
import os

from packer import DEFAULT_CONFIG, load_config, enhance_config
import packer

cwd = os.getcwd()


class LoadConfig(unittest.TestCase):
    def test_example_1(self):
        config = load_config(os.path.join(cwd, 'example/python/simple'))
        self.assertNotEqual(config, {})

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

if __name__ == '__main__':
    unittest.main()
