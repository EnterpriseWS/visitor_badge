import os
import json
import base64
from datetime import datetime
from flask import Flask, jsonify, request
from urllib import parse
from typing import Dict
from PIL import Image, ImageFile
from io import BytesIO
import platform
import badge_factory
ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)
RETURN_CODE_SUCCESS = 0
RETURN_CODE_FAILURE = 1
RETURN_CODE = 'code'
RETURN_MSG = 'msg'
RETURN_MSG_SUCCESS = 'successful push'
RETURN_MSG_FAILURE = 'push failed'
IMG_FOLDER = ''
if platform.system() == 'Linux':
    IMG_FOLDER = 'images/'
elif platform.system() == 'Windows':
    IMG_FOLDER = 'C:\\SourceCode\\Python\\brother_ql_800\\images\\'


@app.route('/print', methods=['POST'])
def post_upload_mips_gate_record():
    return_code = RETURN_CODE_FAILURE
    return_msg = RETURN_MSG_FAILURE
    response = {RETURN_CODE: return_code, RETURN_MSG: return_msg}
    try:
        filepath = ''
        req_info = decode_input(json.loads(request.data))
        image_base64 = req_info['checkPic']
        print(f'->> Got visitor photo ({image_base64[:10]})...')
        image_decoded = base64.b64decode(parse.unquote(image_base64))
        # print('->> Creating badge...')
        badge_image = badge_factory.create_badge(req_info['name'],
                                                 datetime.now().strftime('%m/%d/%Y'),
                                                 image_decoded)
        print(f'->> Created badge with {len(badge_image)} bytes...')
        image_buffer = BytesIO(badge_image)
        with Image.open(image_buffer) as fil_image:
            filepath = IMG_FOLDER + req_info['name'] \
                       + datetime.now().strftime('_%Y%m%d_%H%M%S') \
                       + '.png'
            print('->> Saving badge image...')
            fil_image.save(filepath, 'PNG')

        print_command = 'brother_ql -m QL-800 -p ' + \
                        'usb://0x04f9:0x209b/000J0Z257065 ' + \
                        'print ' + filepath + ' -l 62'
        print('->> Printed visitor badge...')
        os.system(print_command)
        response[RETURN_CODE] = RETURN_CODE_SUCCESS
        response[RETURN_MSG] = RETURN_MSG_SUCCESS
        return jsonify(response)
    except Exception as ex:
        print(ex)
        response[RETURN_MSG] = ex
        return jsonify(response), 400


def decode_input(json_input: json) -> Dict:
    dict_input = {}
    for item in json_input:
        dict_input[item] = parse.unquote_plus(json_input[item])
    return dict_input


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
