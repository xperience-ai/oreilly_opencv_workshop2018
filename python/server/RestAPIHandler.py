#                          License Agreement
#                         3-clause BSD License
#
#       Copyright (C) 2018, Xperience.AI, all rights reserved.
#
# Third party copyrights are property of their respective owners.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   * Neither the names of the copyright holders nor the names of the contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# This software is provided by the copyright holders and contributors "as is" and
# any express or implied warranties, including, but not limited to, the implied
# warranties of merchantability and fitness for a particular purpose are disclaimed.
# In no event shall copyright holders or contributors be liable for any direct,
# indirect, incidental, special, exemplary, or consequential damages
# (including, but not limited to, procurement of substitute goods or services;
# loss of use, data, or profits; or business interruption) however caused
# and on any theory of liability, whether in contract, strict liability,
# or tort (including negligence or otherwise) arising in any way out of
# the use of this software, even if advised of the possibility of such damage.

import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import cgi
import json
import mimetypes as memetypes
import random
import string
import base64

class RestAPIHandler(BaseHTTPRequestHandler):
    def _get_action(self):
        npath = urlparse.urlsplit(self.path).path
        npath = npath[1:]
        path_elements = npath.split('/')
        return path_elements[0]

    def _get_image(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            print("Getting image file as form data")
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE":   self.headers['Content-Type']
                })
            return form["file"].file.read()
        else:
            print("Getting image file base64 encoded frame")
            raw_data_string = self.rfile.read(int(self.headers['Content-Length']))
            comma = raw_data_string.find(',')
            data_type = raw_data_string[:comma]
            image_string = raw_data_string[comma:]
            if data_type == "data:image/png;base64" or data_type == "data:image/jpeg;base64":
                return base64.standard_b64decode(image_string)
            else:
                print("Posted data with unsupported type %s" % data_type)

    def _get_name(self):
        args = urlparse.parse_qsl(urlparse.urlsplit(self.path).query)
        name = 'unknown'
        for key, val in args:
            if key == "name":
                name = val
        return name

    def _set_headers(self):
        action = self._get_action()
        if(action == "introduce" or action == "recognize"):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        else:
            self.send_error(404, "Oops!")

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        print("POST %s" % self.path)
        action = self._get_action()
        print('Action: %s' % action)

        name = ''
        image = self._get_image()
        if(image == None):
            print("Sent empty image!")
            return
        if(action == 'introduce'):
            name = self._get_name()
            print("Submitted name: \"%s\"" % name)
            self.recognizer.introduce(image, name)
        elif(action == 'recognize'):
            name = self.recognizer.recognize(image)
            print("Recognized: %s" % name)

        result = {"name": name}
        self.wfile.write(json.dumps(result))
        self.wfile.close()

def MakeHandlerClass(recognizer):
    class CustomHandler(RestAPIHandler, object):
        def __init__(self, *args, **kwargs):
            self.recognizer = recognizer
            super(CustomHandler, self).__init__(*args, **kwargs)

    return CustomHandler
