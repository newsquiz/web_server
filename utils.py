import os
import uuid
import random
from flask import jsonify
from datetime import datetime
from configs import constants


def generate_filename():
    fname = uuid.uuid5(uuid.NAMESPACE_OID, str(datetime.now()))
    return str(fname).replace('-', '')


def generate_numid():
    numid = ""
    for i in range(5):
        numid += str(random.randint(0, 9))
    return numid


def get_save_path(filename):
    datetime_str = str(datetime.now()).replace('.', '_')
    date_str = datetime_str.split(' ')[0]
    save_path = os.path.join(constants.STATIC_FOLDER, date_str)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_path = os.path.join(save_path, filename)
    return image_path


def save_bi_image(image, filename):
    image_path = get_save_path(filename)
    image.save(image_path)
    return image_path


def validate_data(data, all_fields, required_fields):
    is_valid = True
    validated_data = {}
    for field in all_fields:
        if field not in data:
            if field in required_fields:
                is_valid = False
        else:
            validated_data[field] = data[field]
    return is_valid, validated_data


def response(code, message, data=None):
    if data is None:
        return jsonify({'error': {'code': code, 'message': message}}), code
    else:
        return jsonify({'error': {'code': code, 'message': message}, 'data': data}), code
