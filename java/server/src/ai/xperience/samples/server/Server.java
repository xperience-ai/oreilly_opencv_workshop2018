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

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

public class Server {

    public static void main(String[] args) throws Exception {
        System.loadLibrary("opencv_java341");

        double[] mean = {.0, .0, .0, .0};
        DnnRecognizer recognizer = new DnnRecognizer("../../data/openface.nn4.small2.v1.t7",
                                                     mean,
                                                     1./255);
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);

        server.createContext("/introduce", new IntroduceHandler(recognizer));
        server.createContext("/recognize", new RecognizeHandler(recognizer));
        server.setExecutor(null); // creates a default executor
        server.start();
    }

    static class IntroduceHandler extends CommonHttpHandler
    {
        public IntroduceHandler(DnnRecognizer _recognizer)
        {
            recognizer = _recognizer;
        }

        public void handle(HttpExchange exchange) throws IOException
        {
            System.out.println("Introduce handle");
            String name = "";
            String query = exchange.getRequestURI().getQuery();
            System.out.println("HTTP query:" + query);
            for (String param : query.split("&")) {
                String[] entry = param.split("=");
                if (entry.length > 1) {
                    if (entry[0].equals("name"))
                    name = entry[1];
                }
            }

            System.out.println("Introduced name: " + name);

            byte[] image = getImageFromBody(exchange);
            recognizer.introduce(image, name);
            String response = "{\"name\": \"" + name + "\"}";
            System.out.println("Response: " + response);
            Headers hdrs = exchange.getResponseHeaders();
            hdrs.add("Access-Control-Allow-Origin", "*");
            hdrs.add("Content-type", "application/json");
            exchange.sendResponseHeaders(200, response.length());
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }

        protected DnnRecognizer recognizer;
    }

    static class RecognizeHandler extends CommonHttpHandler
    {
        public RecognizeHandler(DnnRecognizer _recognizer)
        {
            recognizer = _recognizer;
        }

        public void handle(HttpExchange exchange) throws IOException
        {
            System.out.println("Recognize handle");
            byte[] image = getImageFromBody(exchange);
            String name = recognizer.recognize(image);
            System.out.println("Recognized name: " + name);
            String response = "{\"name\": \"" + name + "\"}";
            Headers hdrs = exchange.getResponseHeaders();
            hdrs.add("Access-Control-Allow-Origin", "*");
            hdrs.add("Content-type", "application/json");
            exchange.sendResponseHeaders(200, response.length());
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }

        protected DnnRecognizer recognizer;
    }
}
