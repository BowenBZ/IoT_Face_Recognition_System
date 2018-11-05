# Home Assistance Robot
This robot is designed to help older people get a 
smarter house with low cost.

## Function
#### Face Detection
* Store Your Faces  
  When the program runs, people can press
  * key `s` to store and restore their faces
  * key `r` to remove the faces with specific name   
  
* Faces Detection  
  The program can detect faces in the camera and use
  square the around the faces. Multi-faces are supported.
  
* Faces Recognition  
  The camera can recognize who are in the camera. 
  Multi-faces are supported.The labels will be given
  near the square. The labels are
  * `Unknown` if the faces hasn't been stored  
  * the name that people gave when they store the faces

#### IoT Control
* Send Message to mobiles  
  When strangers come to the house, a message
  via Facebook Messager is given to their
  mobiles.
  
* Unlock Control  
  When the house owner get back home, an unlock key
  image will be shown in the screen.

## Install
#### Software Requirments
* Install [face_recognition](https://github.com/ageitgey/face_recognition) package  
  To install this package in Windows
    * if you already have the `cmake` compiler environment,
        you can use following command to install the package
        ```
        pip install dlib
        pip install face_recognition
        ```
    * if you don't have the `camke` compiler environment, you can
    go to [here](https://pypi.org/simple/dlib/) to download the
    dlb.whl file and install it with `pip`. Later you can use
        ```
        pip install face_recognition
        ```
        to install `face_recognition` package.
        
    I personal recommend you can use the `virtualenv` to create a virtual 
    python environment, [instruction](http://maxlai.cc/2018/08/24/windows-python36-quickly-install-face-recognition/) is here. 

* IFTTT settings
    * Signup an account in [IFTTT](https://IFTTT.com) 
      website.
    * Go to `MyApplets` - `New Applet` - `this`, choose the `Webhooks` - `Revice a web request`, and give the 
      event name and click `Create trigger`.
    * choose `that` - `Face Messenger` - `Send Message`, 
      and type what you want to send to your mobile, then click
      `Create Action - Finish`. 
    * Go back to the homepage and go to `MyApplets` - `Services` - `Webhooks` 
    - `Documentation`
     copy the link to the parameter of `url_stranger` in `home_assistance_robot.py`
      
* Use `PyCharm` to open this project, make sure that your
  interpreter was set to the right path of your path and `dlib`, `face_recogniton`
  were already installed.   
   
* Run home_assistance_robot.py
 

#### Hardware Requirements
* A PC with python environment 
* A Camera connected to the PC
* A Mobile with Facebook Messenger

## Structure and Parameters
* main.py  
  The entry of all the functions. Use the `FaceProcess` class
  from the `ImageProcess.py` file.
  
* ImageProcess.py  
  Has the class of `FaceProcess`, can handle the function of 
  camera detection and recognition.  
  You can set the parameters, the parameters are as following:
  * resize_frame  
    Resize the frame when handle the frame. Vary from 0 to 1.
  * recognize_threshold   
    The threshold to recognize people. Vary from 0 to 1.
  * recognize_mode  
    0 means to recognize when the number of faces change; 1 
    means to recognize every detect_interval frames. 
  * detect_interval  
    handle the image every detect_interval frames. Has no function
    if recognize_mode is set to 0
  * person_store_number  
    the number of images to store in the database
  * filename=filename  
    the .csv file name  
    
  Notes:  
  I recommend you set the parameter to recognize_mode=1, detect_interval=2.
  If it runs very slowly, you can set the parameter to recognize_mode=0.