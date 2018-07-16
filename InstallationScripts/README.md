# Installation Scripts for OpenCV

This repository contains the installation scripts for OpenCV version `3.4.1` and `master` branch.

## Installing OpenCV in Ubuntu 16

The script for installing OpenCV in Ubuntu 16.04 is present in Ubuntu 16 folder. To run the script, enter the following command in terminal:

`./installOpenCV.sh`

**To test the installation, commands will be displayed at the end of installation.**

**NOTE**: You will be required to enter your password during the installation for `sudo` commands.

## Installing OpenCV in Ubuntu 18

The script for installing OpenCV in Ubuntu 18.04 is present in Ubuntu 18 folder. To run the script, enter the following command in terminal:

`./installOpenCV.sh`

**To test the installation, commands will be displayed at the end of installation.**

**NOTE**: You will be required to enter your password during the installation for `sudo` commands.

## Installing OpenCV in Windows

The script for installing OpenCV in Windows is present in Windows folder. The detailed procedure is as follows:

1) Install [Anaconda 3](https://www.anaconda.com/download/#windows), [Visual Studio 2015](https://visualstudio.microsoft.com/vs/older-downloads/), [Git for Windows](https://git-scm.com/download/win) and [CMake](https://cmake.org/download/). **Make sure you download the correct version (64 bit or 32 bit)**. Also, make sure that you put Anaconda 3, CMake, and Git in your `PATH` during installation.

2) Press `Start`, type `Command Line` and press `Enter`. 

3) Type `python main.py` and press `Enter`. Select appropriate OpenCV version. Default version is 3.4.1

4) Type `installOpenCV.bit` and press `Enter`.

5) Remove `runScript.bat`: `del runScript.bat`.

6) Type `python modifyBatchScript.py` and press `Enter`.

7) Type `finalScript.bat` and press `Enter`.

8) Press `Start`, type `Environment variables` and click on `Edit the system environment variables`. In the popup window, click on `Environment Variables`.

9) In `System Variables`, click on `Path`, and then click on `Edit`. Add the complete path to the directory where OpenCV was installed. This can be found at as:

`<Complete path to the directory where installation scripts are present>\openCV-<version you selected (3.4.1 or master)\build\install\x64\vc14\bin`

Click `OK` to save. **Do NOT close the Environment Variables window.**

10) In `User variables`, click on `New`, under `Variable name:`, enter `OPENCV_DIR` and under `Variable value:`, enter the path to the `install` directory of OpenCV. This will be:

`<Complete path to the directory where installation scripts are present>\openCV-<version you selected (3.4.1 or master)\build\install`

11) Click on `OK`, and click on `OK` to close `Environment Variables` window.

12) To test your installation, press `Start`, enter `Command Line`, and type:

`activate OpenCV-<version you selected (3.4.1 or master)>-py2`
`ipython`
`import cv2`
`cv2.__version__`

This should output the version you selected (`3.4.1` or `4.0.0-pre` for master).

