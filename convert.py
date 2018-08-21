import rawpy
import imageio
import os

RAW_EXT = 'ARW'
SEP = '.'


def convert_image(input_path, output_path):
    with rawpy.imread(input_path) as raw:
        rgb = raw.postprocess()
    print("Saving {}".format(output_path))
    imageio.imsave(output_path, rgb)


def convert_name(input_name, img_format):
    name, sep, ext = input_name.rpartition(SEP)
    output_name = name + sep + img_format
    return output_name


def convert_dir(input_dir, output_dir, img_format):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    input_names = os.listdir(input_dir)
    for input_name in input_names:
        name, sep, ext = input_name.rpartition(SEP)
        if ext != RAW_EXT:
            message = "Skipping {}".format(input_name)
            print(message)
            continue

        input_path = os.path.join(input_dir, input_name)

        output_name = name + sep + img_format
        output_path = os.path.join(output_dir, output_name)

        convert_image(input_path, output_path)


def main(args):
    convert_dir(
        args.input_dir,
        args.output_dir,
        args.format)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input_dir', help='Directory of images to convert.',
                        default='.')
    parser.add_argument('-o', '--output_dir', help='Output Directory',
                        default='out')
    parser.add_argument('-f', '--format', help='Image format.',
                        default='jpg')

    args = parser.parse_args()
    main(args)