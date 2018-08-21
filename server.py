import os
from flask import Flask, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
from convert import convert_image, convert_name

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
IMAGE_FORMAT = 'jpg'

app = Flask(__name__)
CORS(app)                               # Allow CORS (Cross Origin Requests)


def setup():
    if not os.path.exists(INPUT_DIR):
        os.mkdir(INPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)


@app.route('/output/<path>')
def output(path):
    return send_from_directory(OUTPUT_DIR, path)


@app.route('/', methods=['GET', 'POST'])
def upload():
    """
    Handles uploads.
    """
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join(INPUT_DIR, filename)
            file.save(input_path)
            output_name = convert_name(filename, IMAGE_FORMAT)
            output_path = os.path.join(OUTPUT_DIR, output_name)
            convert_image(input_path, output_path)
            return redirect(url_for(
                'output',
                path=output_name))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def main(args):
    setup()
    app.run(
        host='0.0.0.0',
        port=args.port,
        threaded=False,
        debug=args.debug,
        ssl_context=args.ssl)


if(__name__ == "__main__"):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        help="Port that the server will run on.",
        type=int,
        default=8002)
    parser.add_argument(
        '-d',
        '--debug',
        help="Whether or not to run in debug mode.",
        default=True,
        action='store_true')
    parser.add_argument(
        '-s',
        '--ssl',
        help="Whether or not to run with HTTPS",
        default=None,
        action='store_const',
        const='adhoc')

    args = parser.parse_args()
    main(args)
