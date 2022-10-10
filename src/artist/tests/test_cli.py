import argparse
import unittest
import sys
import src

from src.main import setup_arg_parse


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.cli_parser = setup_arg_parse()


    def test_parser_single_no_flags(self):
        args = self.cli_parser.parse_args(['single'])

        self.assertFalse(args.verbose)
        self.assertIsNone(args.seed)
        self.assertIsNone(args.layers)
        self.assertIsNone(args.width)
        self.assertIsNotNone(args.func)
        self.assertEqual(args.activation, "tanh")


    def test_parser_single_verbosity(self):
        args = self.cli_parser.parse_args(['single', '-v'])
        self.assertTrue(args.verbose)

    
    def test_parser_single_seed(self):
        seed = 999
        args = self.cli_parser.parse_args(['single', '-s', str(seed)])
        self.assertEqual(args.seed, seed)


    def test_parser_single_set_layers(self):
        layers = 500
        args = self.cli_parser.parse_args(['single', '-l', str(layers)])
        self.assertEqual(args.layers, layers)


    def test_parser_single_set_width(self):
        width = 20
        args = self.cli_parser.parse_args(['single', '-w', str(width)])
        self.assertEqual(args.width, width)

    
    def test_parser_single_custom_resolution(self):
        resolution = [33, 66]
        args = self.cli_parser.parse_args(['single', '-r', str(resolution[0]), str(resolution[1])])
        self.assertEqual(args.resolution, resolution)

    
    def test_parser_single_activation(self):
        activation = "sech"
        args = self.cli_parser.parse_args(['single', '-a', activation])
        self.assertEqual(args.activation, activation)


    def test_parser_batch_n(self):
        n = 10
        args = self.cli_parser.parse_args(['batch', str(n)])
        self.assertEqual(args.number_of_images, n)

    
    def test_parser_batch_verbosity(self):
        args = self.cli_parser.parse_args(['batch', '10', '-v'])
        self.assertTrue(args.verbose)

    
    def test_parser_batch_resolution(self):
        resolution = [100, 50]
        args = self.cli_parser.parse_args(['single', '-r', str(resolution[0]), str(resolution[1])])
        self.assertEqual(args.resolution, resolution)

    
    def test_parser_batch_activation(self):
        activation = "sigmoid"
        args = self.cli_parser.parse_args(['batch', '10', '-a', activation])
        self.assertEqual(args.activation, activation)



if __name__ == '__main__':
    unittest.main()