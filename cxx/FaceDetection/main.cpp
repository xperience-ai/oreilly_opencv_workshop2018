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

#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/dnn.hpp>

const size_t inWidth = 300;
const size_t inHeight = 300;
const double inScaleFactor = 1.0;
const float confidenceThreshold = 0.5;
const cv::Scalar meanVal(104.0, 177.0, 123.0);

const std::string modelConfiguration = "../data/deploy.prototxt";
const std::string modelBinary = "../data/res10_300x300_ssd_iter_140000_fp16.caffemodel";

int main(int argc, char ** argv)
{
    int cameraIdx = -1;
    std::string fileName = "";
    if (argc == 1)
    {
        cameraIdx = 0;
    }
    else if(isdigit(argv[1][0]))
    {
        cameraIdx = atoi(argv[1]);
    }
    else
    {
        fileName = std::string(argv[1]);
    }

    cv::VideoCapture source;
    if(cameraIdx >= 0)
    {
        source.open(cameraIdx);
    }
    else
    {
        source.open(fileName);
    }

    if(source.isOpened())
    {
        std::cout << "Video stream opened!" << std::endl \
            << "width=" << source.get(cv::CAP_PROP_FRAME_WIDTH) << std::endl \
            << "height=" << source.get(cv::CAP_PROP_FRAME_HEIGHT) << std::endl;
    }
    else
    {
        std::cout << "Error opening video stream!" << std::endl;
        return -1;
    }

    cv::dnn::Net net = cv::dnn::readNetFromCaffe(modelConfiguration, modelBinary);

    cv::Mat frame;
    cv::Mat result;
    bool alive = true;
    while(alive)
    {
        source >> frame;
        if(frame.empty())
            break;

        cv::Mat inputBlob = cv::dnn::blobFromImage(frame, inScaleFactor,
                                                   cv::Size(inWidth, inHeight), meanVal, false, false);
        net.setInput(inputBlob, "data");
        cv::Mat detection = net.forward("detection_out");

        std::vector<double> layersTimings;
        double freq = cv::getTickFrequency() / 1000;
        double time = net.getPerfProfile(layersTimings) / freq;

        cv::Mat detectionMat(detection.size[2], detection.size[3], CV_32F, detection.ptr<float>());

        frame.copyTo(result);

        std::ostringstream ss;
        ss << "FPS: " << 1000/time << " ; time: " << time << " ms";
        cv::putText(result, ss.str(), cv::Point(20,20), 0, 0.5, cv::Scalar(0,0,255));

        for(int i = 0; i < detectionMat.rows; i++)
        {
            float confidence = detectionMat.at<float>(i, 2);

            if(confidence > confidenceThreshold)
            {
                int xLeftBottom = std::max(0, static_cast<int>(detectionMat.at<float>(i, 3) * result.cols));
                int yLeftBottom = std::max(0, static_cast<int>(detectionMat.at<float>(i, 4) * result.rows));
                int xRightTop = std::min(result.cols-1, static_cast<int>(detectionMat.at<float>(i, 5) * result.cols));
                int yRightTop = std::min(result.rows-1, static_cast<int>(detectionMat.at<float>(i, 6) * result.rows));

                cv::Rect object(xLeftBottom, yLeftBottom,
                                xRightTop - xLeftBottom,
                                yRightTop - yLeftBottom);

                cv::rectangle(result, object, cv::Scalar(0, 255, 0));

                ss.str("");
                ss << confidence;
                std::string conf(ss.str());
                std::string label = "Face: " + conf;
                int baseLine = 0;
                cv::Size labelSize = cv::getTextSize(label, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
                cv::rectangle(result, cv::Rect(cv::Point(xLeftBottom, yLeftBottom - labelSize.height),
                                     cv::Size(labelSize.width, labelSize.height + baseLine)),
                                     cv::Scalar(255, 255, 255), cv::FILLED);
                cv::putText(result, label, cv::Point(xLeftBottom, yLeftBottom),
                        cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0,0,0));
            }
        }

        cv::imshow("Camera Filters", result);

        char c = (char)cv::waitKey(30);
        switch(c)
        {
            case 'q':
            case 'Q':
            case 27:
                alive = false;
            break;
        }
    }

    return 0;
}
