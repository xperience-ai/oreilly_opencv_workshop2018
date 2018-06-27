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
import sys
import shutil
import uuid
import CommonRecognizer

class DumpingRecognizer(CommonRecognizer.AbstractRecognizer):
    def __init__(self):
        os.mkdir('introduce')
        os.mkdir('recognize')

    def introduce(self, image, user_name):
        image_name = str(uuid.uuid4()) + ".jpg"
        fname = os.path.join('introduce', image_name)
        fdst = open(fname, "wb")
        fdst.write(image)
        fdst.close()

        fdst_desc = open(fname + '.desc', "wt")
        fdst_desc.write(image_name)
        fdst_desc.close()

    def recognize(self, image):
        image_name = str(uuid.uuid4()) + ".jpg"
        fname = os.path.join('recognize', image_name)
        fdst = open(fname, "wb")
        fdst.write(image)
        fdst.close()
        return 'unknown'
