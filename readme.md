# Home Assistance Robot - Web Server Version
This version is a web server based on flask. Users can use HTTP Post command to upload images and get back the positions of the faces and the names after recognition.

## Function
### Faces Detection  
  The program can detect the position of faces in the image return the coordinate to the client. Multi-faces are supported.
  
### Faces Recognition  
  The program can recognize who are people in the images. 
  Multi-faces are supported. The labels are
  * `Stranger` if the faces hasn't been stored  
  * the name that people gave when they store the faces

### Faces Management  
  Users can save the face with specific name, and users can remove the existing faces.

## Install
### Run locally
* Install [face_recognition](https://github.com/ageitgey/face_recognition) package  

* Install [Flask](http://flask.pocoo.org/) package  
  Notes:
  * Check the language for non-Unicode programs is set to `English`. Sometimes the system unicode may cause some problem when you install the package
  * You may also need to install `flask-cors` package if you encounter the CORS error when you runs it locally.
      
* Run main.py

#### Run on Google App Engine


## How to use
### Face Detection
Send a HTTP POST to `http://your id or url/detect`, the format of send data should be like
```
send_data = {"img": img_data};
```
The img_data should be base64 format. It can be a RPG image or a Gray image. The structure of return data is as follows
```
return_data = {"face_pos": face_position}
```
The `face_position` is an array, the i-index of it is the i-index face's positions. 
```
face_position[i] = {top, left, bottom, right}
```

### Face Recognition  
Send a HTTP GET to `http://your id or url/detect`. The return is the faces' names in previous images, which means this step should be done after the face detection. The format of return data is
```
return_data = {"face_name", face_names}
```
The `face_names` is an array, the i-index of it is the i-index name string in the previous uploaded images. 


### Save Face
Send a HTTP POST to `http://your id or url/save`. THe format of send data should be like
```
send_data = {"img": img_data,
             "name": name,
             "mode": "add"};
```
The img_data is the image with base64 format, the name is the person's name in the img_data, the `mode` should be set to `"add"`. The return data is `True` or `False`



### Remove face
Send a HTTP POST to `http://your id or url/save`. THe format of send data should be like
```
send_data = {"name": name,
             "mode": "remove"};
```
The return data is `True` or `False`

    
Notes:  
I recommend you set the parameter to resize_frame=1, recognize_threshold=0.4, detect_interval=0