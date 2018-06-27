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
#include <stdlib.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

enum FilterType
{
    PREVIEW,
    CANNY,
    BLUR,
    ZOOM
};

int main(int argc, char ** argv)
{
    FilterType filter = PREVIEW;
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

    cv::Mat frame;
    cv::Mat result;
    bool alive = true;
    while(alive)
    {
        source >> frame;
        if(frame.empty())
            break;

        switch(filter)
        {
            case PREVIEW:
                result = frame;
            break;
            case CANNY:
                cv::Canny(frame, result, 80, 90);
            break;
            case BLUR:
                cv::blur(frame, result, cv::Size(5,5));
            break;
            case ZOOM:
                cv::resize(frame, result, cv::Size(frame.cols*2, frame.rows*2));
            break;
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
            case 'c':
            case 'C':
                filter = CANNY;
            break;
            case 'b':
            case 'B':
                filter = BLUR;
            break;
            case 'p':
            case 'P':
                filter = PREVIEW;
            break;
            case 'z':
            case 'Z':
                filter = ZOOM;
            break;
        }
    }

    return 0;
}
