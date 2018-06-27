//                          License Agreement
//                         3-clause BSD License
//
//       Copyright (C) 2018, Xperience.AI, all rights reserved.
//
// Third party copyrights are property of their respective owners.
//
// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
//   * Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//   * Redistributions in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//
//   * Neither the names of the copyright holders nor the names of the contributors
//     may be used to endorse or promote products derived from this software
//     without specific prior written permission.
//
// This software is provided by the copyright holders and contributors "as is" and
// any express or implied warranties, including, but not limited to, the implied
// warranties of merchantability and fitness for a particular purpose are disclaimed.
// In no event shall copyright holders or contributors be liable for any direct,
// indirect, incidental, special, exemplary, or consequential damages
// (including, but not limited to, procurement of substitute goods or services;
// loss of use, data, or profits; or business interruption) however caused
// and on any theory of liability, whether in contract, strict liability,
// or tort (including negligence or otherwise) arising in any way out of
// the use of this software, even if advised of the possibility of such damage.

package ai.xperience.samples.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Base64;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

public abstract class CommonHttpHandler implements HttpHandler {

    protected byte[] getImageFromBody(HttpExchange exchange) {
        StringBuilder stringBuilder = new StringBuilder();
        InputStream in = exchange.getRequestBody();
        if (in != null) {
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(in));
            char[] charBuffer = new char[256];
            int bytesRead = -1;
            try {
                while ((bytesRead = bufferedReader.read(charBuffer)) > 0) {
                    stringBuilder.append(charBuffer, 0, bytesRead);
                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        } else {
            stringBuilder.append("");
        }

        String body = stringBuilder.toString();
        String[] splited = body.split(",");

        // TODO: Add data type check

        Base64.Decoder dec = Base64.getDecoder();
        byte[] image = dec.decode(splited[1].toString());

        return image;
    }
};
