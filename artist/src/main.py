import argparse
import random
from src.art_net import NumpyArtGenerator
from src.file_util import save_numpy_image

seed_min = 0
seed_max = 2147483647
layers_min = 0
layers_max = 50
width_min = 0
width_max = 20
default_resolution = (1920, 1080)
output_directory = "images"


def single_img_generation(args):
    if args.seed is None:
        args.seed = random.randint(seed_min, seed_max)
    if args.layers is None:
        args.layers = random.randint(layers_min, layers_max)
    if args.width is None:
        args.width = random.randint(width_min, width_max)

    if args.resolution is None:
        args.resolution = default_resolution
    else:
        args.resolution = tuple(args.resolution)

    generator = NumpyArtGenerator(args.resolution, args.seed, args.layers, args.width, args.activation)
    numpy_image = generator.run(args.verbose)

    filename = str(generator) + ".jpg"
    save_numpy_image(numpy_image, filename, output_directory)


def batch_img_generation(args):
    if args.resolution is None:
        args.resolution = default_resolution
    else:
        args.resolution = tuple(args.resolution)

    for i in range(args.number_of_images):
        print(f"Generating image {i+1}/{args.number_of_images}")
        args.seed = random.randint(seed_min, seed_max)
        args.layers = random.randint(layers_min, layers_max)
        args.width = random.randint(width_min, width_max)

        generator = NumpyArtGenerator(args.resolution, args.seed, args.layers, args.width, args.activation)
        numpy_image = generator.run(args.verbose)

        filename = str(generator) + ".jpg"
        save_numpy_image(numpy_image, filename, output_directory)


def setup_arg_parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    single_parser = subparsers.add_parser('single', description="Generate a single image.")
    single_parser.add_argument("-v", "--verbose", action='store_true', help="Increased verbosity. Outputs details about the current image being generated.")
    single_parser.add_argument("-s", "--seed", type=int, help="Seed value used by numpy random. Default is a random int between " + str(seed_min) + " - " + str(seed_max))
    single_parser.add_argument("-l", "--layers", type=int, help="Number of hidden layers. Default is a random int between " + str(layers_min) + " - " + str(layers_max))
    single_parser.add_argument("-w", "--width", type=int, help="Number of perceptrons in each hidden layer. Default is a random int between " + str(width_min) + " - " + str(width_max))
    single_parser.add_argument("-r", '--resolution', nargs=2, type=int, help="Resolution of output image. Default is " + str(default_resolution))
    single_parser.add_argument("-a", "--activation", default="tanh", help="Activation function used in every hidden layer. Activation functions can be found in the numpy_activation file.")
    single_parser.set_defaults(func=single_img_generation)

    batch_parser = subparsers.add_parser('batch', description="Generate multiple images with random neural network settings.")
    batch_parser.add_argument('number_of_images', type=int, help="Number of images to generate.")
    batch_parser.add_argument("-v", "--verbose", action='store_true', help="Increased verbosity. Outputs details about the current image being generated.")
    batch_parser.add_argument("-r", '--resolution', nargs=2, type=int, help="Resolution of output image. Default is " + str(default_resolution))
    batch_parser.add_argument("-a", "--activation", default="tanh", help="Activation function used in every hidden layer. Activation functions can be found in the numpy_activation file.")
    batch_parser.set_defaults(func=batch_img_generation)

    return parser

if __name__ == "__main__":
    parser = setup_arg_parse()
    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()

