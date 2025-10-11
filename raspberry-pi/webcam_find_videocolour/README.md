# webcam_find_videocolour
small python script to get the color of a certain pixel in the video frame
<br>
Required python packages:<br>
1. Numpy<br>
2. OpenCV<br>
<br>
<br>
What this script does:<br>
The script looks for the pixel in the middle of the webcam video frame,<br>
gets the RGB color data from that pixel and "converts" it to the nearest<br>
color name (either from the WebColor-Standard or the ImageMagick-Standard)<br>
<br>
If you want a different pixel to be scanned for the color-data change these lines<br>
in "webcam_find_videocolor.py" to whatever height/width coordinates you fancy:<br>
mid_w=int(cap.get(cv.CAP_PROP_FRAME_WIDTH)/2) # get middle of width<br>
mid_h=int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)/2) # get middle of height<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
Sources:<br>
WebColor-Names: http://www.w3schools.com/html/html_colornames.asp<br>
ImageMagick-Names: http://www.imagemagick.org/script/color.php<br>
rgb to names: https://gist.github.com/yuyay/0d037d3543405fb4c30120eb5b0f648f<br>
openCV (they get a link here as soon as they finally fix the exposure-bug)<br>
