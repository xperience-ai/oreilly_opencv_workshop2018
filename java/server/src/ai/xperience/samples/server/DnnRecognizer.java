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

import java.util.ArrayList;
import org.opencv.core.*;
import org.opencv.imgcodecs.*;
import org.opencv.dnn.*;

public class DnnRecognizer
{
    public DnnRecognizer(String model_path, double[] model_mean, double model_scale)
    {
        model = Dnn.readNetFromTorch(model_path);
        mean = new Scalar(model_mean[0], model_mean[1], model_mean[2], model_mean[3]);
        scale = model_scale;
        known_faces = new ArrayList<DnnRecognizer.Person>();
    }

    public void introduce(byte[] frame_data, String name)
    {
        Mat frame = new Mat(frame_data.length, 1, CvType.CV_8UC1);
        frame.put(0, 0, frame_data);
        Mat face = Imgcodecs.imdecode(frame, Imgcodecs.IMREAD_COLOR);
        Person p = new Person();
        p.name = name;
        p.descriptor = face2vec(face);
        known_faces.add(p);
    }

    public String recognize(byte[] frame_data)
    {
        Mat frame = new Mat(frame_data.length, 1, CvType.CV_8UC1);
        frame.put(0, 0, frame_data);
        Mat face = Imgcodecs.imdecode(frame, Imgcodecs.IMREAD_COLOR);
        Mat descriptor = face2vec(face);
        String bestMatchName = "unknown";
        double bestMatchScore = .5;
        for (Person p : known_faces)
        {
            double score = descriptor.dot(p.descriptor);
            if (score > bestMatchScore)
            {
                bestMatchScore = score;
                bestMatchName = p.name;
            }
        }
        return bestMatchName;
    }

    protected Mat face2vec(Mat face)
    {
        Size size = new Size(96, 96);
        Mat blob = Dnn.blobFromImage(face, scale, size, mean, false, false);
        model.setInput(blob);
        return model.forward();
    }

    class Person
    {
        public String name;
        public Mat descriptor;
    };

    protected Net model;
    protected Scalar mean;
    protected double scale;
    protected ArrayList<Person> known_faces;
}
