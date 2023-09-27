# This software is licensed under the Creative Commons
# Attribution-NonCommercial 4.0 International License.
# To view a copy of this license, visit
# https://creativecommons.org/licenses/by-nc/4.0/
import urllib.parse


def url_encode_string(input_string):
    encoded_string = urllib.parse.quote(input_string)
    return encoded_string


def create_data_url(file_type: str, file_format: str, base64: bool, data: str, url_encode_data: bool):
    if base64:
        return "data:" + file_type + "/" + file_format + ";base64," + data
    else:
        if url_encode_data:
            return "data:" + file_type + "/" + file_format + "," + url_encode_string(data)
        else:
            return "data:" + file_type + "/" + file_format + "," + data
