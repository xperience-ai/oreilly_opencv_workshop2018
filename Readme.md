Intro
=====

The repo contains OpenCV setup instructions, source code and other materials needed for OpenCV workshop.
The workshop covers the same set of computer vision use cases implemented with
OpenCV using different technologies. The workshop is designed for Windows,
Linux (Ubuntu 16.04 recommended) or Mac OS.

Use cases:
 - Preview from camera;
 - Base image processing techniques;
 - Face detection with DNN or Cascades depending on target performance;
 - Face recognition using DNN.

Languages and stacks:
 - C++;
 - Java 8 and higher;
 - Java for Android;
 - JavaScript.

Folders content:

  - `cxx` C++ implementation for all samples;
  - `data` DNN models and other data files;
  - `java/Android*` Java implementation of samples;
  - `java/server` Java implementation of REST service for face recognition
  - `js` Java Script implementation of samples (requires Java or Python server
    for face recognition functionality);
  - `python` Python implementation of samples;
  - `python/server` Python implementation of REST service for face recognition;
  - `python-template` Initial samples skeleton for hands-on session.

Prerequisites for C++
=====================

 1. C++11 compatible compiler: GCC 5.x for Unix and Microsoft Visual Studio 2015
    or newer for Windows.
 2. CMake: <https://cmake.org/download/>

Prerequisites for Python
========================

 1. Python 2.7.x or Python 3.5.x installed on your system;
 2. For Windows and Mac OS numpy and opencv-python packages installed with pip:

    $ pip install opencv_python==3.4.1

 3. For Linux numpy package installed with your system package manager:

    $ sudo apt-get install python-numpy

    And OpenCV 3.4.1 built from sources with Python support. See **TBD link**

Prerequisites for Java (advanced)
=================================

 1. Oracle JDK 8 or OpenJDK 8 for you platform.
 2. Gradle build tool for your platform

Prerequisites for Android (advanced)
====================================

 1. Android Studio
 2. Android SDK for you target platform

Python Bootstrap
================

If you are running Windows on Mac OS you do not need to warry, pip has done
everything for you.

For Linux users:

 1. Extract pre-built OpenCV archive
 2. Add OpenCV libraries to `LD_LIBRARY_PATH`:

    $ export LD_LIBRARY_PATH=<path_to_extracted_opencv>/lib

 3. Add OpenCV Python bindings to `PYTHONPATH`:

    $ export PYTHONPATH=<opencv_distro>/lib/python<version>/dist-packages:$PYTHONPATH

Python Samples
==============

Python samples do not require extra steps, just run it:

    $ cd <sample_folder>
    $ python <sample_name>.py
