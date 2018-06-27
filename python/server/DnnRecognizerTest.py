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

import unittest
import DnnRecognizer

class DnnRecognizerTest(unittest.TestCase):
    def test_EmptyBase(self):
        with open('files/lena.jpg', 'rb') as f:
            lena = f.read()
        recogn = DnnRecognizer.DnnRecognizer()
        who = recogn.recognize(lena)
        self.assertTrue(who, "unknown")

    def test_LenaSame(self):
        with open('files/lena.jpg', 'rb') as f:
            lena = f.read()
        recogn = DnnRecognizer.DnnRecognizer()
        recogn.introduce(lena, "Lena")
        who = recogn.recognize(lena)
        self.assertTrue(who, "Lena")

    def test_LenaAndLena(self):
        with open('files/lena.jpg','rb') as f:
            lena = f.read()
        with open('files/lena_other.jpg', 'rb') as f:
            lena_other = f.read()
        recogn = DnnRecognizer.DnnRecognizer()
        recogn.introduce(lena, "Lena")
        who = recogn.recognize(lena_other)
        self.assertTrue(who, "Lena")

    def test_LenaUnknownMessi(self):
        with open('files/lena.jpg','rb') as f:
            lena = f.read()
        with open('files/messi.jpg','rb') as f:
            messi = f.read()
        recogn = DnnRecognizer.DnnRecognizer()
        recogn.introduce(lena, "Lena")
        who = recogn.recognize(messi)
        self.assertTrue(who, "unknown")

    def test_LenaKnownMessi(self):
        with open('files/lena.jpg','rb') as f:
            lena = f.read()
        with open('files/lena_other.jpg', 'rb') as f:
            lena_other = f.read()
        with open('files/messi.jpg','rb') as f:
            messi = f.read()
        recogn = DnnRecognizer.DnnRecognizer()
        recogn.introduce(lena, "Lena")
        recogn.introduce(lena, "Messi")
        who = recogn.recognize(messi)
        self.assertTrue(who, "Messi")
        who = recogn.recognize(lena_other)
        self.assertTrue(who, "Lena")


if __name__ == '__main__':
    unittest.main()
