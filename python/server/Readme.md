Dependencies
============

1. Python 2.7.x
2. OpenCV 3.4.1 Python bindings with DNN nmodule enabled
3. Numpy

Start SerVer Locally
====================

The server is stared in interactive mode with port 8080 by default:

    $ ./server.py

Start Server in Docker
======================

    $ cd ..
    $ docker build --tag server .
    $ docker run -it -p 8080:8080 server

Test Server
===========

In other console:

    $ ~/Projects/Xperience/oreilly_opencv_workshop2018/python-server$ curl -F 'file=@./files/lena.jpg' http://localhost:8080/introduce?name=Lena
    {"status": 200, "data": {"name": "Lena"}, "success": true}
    $ ~/Projects/Xperience/oreilly_opencv_workshop2018/python-server$ curl -F 'file=@./files/lena.jpg' http://localhost:8080/recognize
    {"status": 200, "data": {"name": "Lena"}, "success": true}
    $ ~/Projects/Xperience/oreilly_opencv_workshop2018/python-server$ curl -F 'file=@./files/messi.jpg' http://localhost:8080/introduce?name=Messi
    {"status": 200, "data": {"name": "Messi"}, "success": true}
    $ ~/Projects/Xperience/oreilly_opencv_workshop2018/python-server$ curl -F 'file=@./files/lena_other.jpg' http://localhost:8080/recognize
    {"status": 200, "data": {"name": "Lena"}, "success": true}
    $ ~/Projects/Xperience/oreilly_opencv_workshop2018/python-server$ curl -F 'file=@./files/messi.jpg' http://localhost:8080/recognize
    {"status": 200, "data": {"name": "Messi"}, "success": true}
