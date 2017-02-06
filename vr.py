# NOTE: make sure you run the "auto-off.sh" script before running this file.
# It turns off all of the auto settings of the microsoft lifecam that interfere
# with image processing 
import cv2
import numpy
import math


class GripPipeline:
    """
    An OpenCV pipeline generated by GRIP.
    """
    
    def __init__(self):
        """initializes all values to presets or None if need to be set
        """

        self.__hsv_threshold_hue = [40.46762589928058, 74.02730375426621]
        self.__hsv_threshold_saturation = [18.345323741007192, 135.33276450511946]
        self.__hsv_threshold_value = [43.00872861033209, 117.92662116040955]

        self.hsv_threshold_output = None


    def process(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        self.__hsv_threshold_input = source0
        (self.hsv_threshold_output) = self.__hsv_threshold(self.__hsv_threshold_input, self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)


    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))



# setup the camera 
#Capture = cv2.VideoCapture(0)
#Capture.set(10, 0.1);
#Capture.set(11, 0.1);
#Capture.set(12, 0.1);

# setup the GRIP pipeline 
pipe = GripPipeline()


# this processes images until the esc is pressed. 
while True:
    # setup/reset the number of contours detected 
    cntsDetected=0;
    
    # get the image to be processed from the webcam 
    frame = cv2.imread("./ImgCap/img5.jpg")
    #ret_vaule, frame = Capture.read();

    # retrieve the ratio of the image from the webcam    
    ratio = frame.shape[0];

    # run the image through the GRIP generated pipeline 
    pipe.process(frame);

    # find all the contours from the threashold mask generated by the pipeline 
    cnts = cv2.findContours(pipe.hsv_threshold_output.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[0]


    # This loops through all the detected shapes (contours), checking each
    # one to tell if it is one of the gear goal retangles.
    for c in cnts:
            # this simplifies the detected contours to a more processable state
            peri = cv2.arcLength(c, True)
	    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
	    
            # check if the contours have between 4 and 6 vertices
            # NOTE: Yes, a pure rectangle only has 4 vertices. This had to be changed
            # to detect contours with 6 vertices also because sometimes it would drop
            # the rectangles we wanted to detect. I assume this was due to the the
            # simlification step not being perfect.
	    if len(approx) >= 4 and len(approx) <= 6 :
                # once a rectangle is detected get its approximated dimensions 
                (x, y, w, h) = cv2.boundingRect(approx)
                # calculate the ratio of its height to its width
		hw = h / float(w)

                # This checks if the calculated ratio is within the ratio
                # of the target (filters out extraneous rectangles).
		if hw >= 1.4 and hw <= 2.9:
                    # add to the total number of rectangles found 
                    cntsDetected = cntsDetected + 1;

                    # put the moment of the proper contour in its variable
                    if cntsDetected == 1:
                        cntOneMoment = cv2.moments(c)
                    elif cntsDetected == 2:
                        cntTwoMoment = cv2.moments(c)

                    # this puts the contours and their centers on the image 
                    m = cv2.moments(c)
                    cv2.circle(frame, (int(m['m10']/m['m00']), int(m['m01']/m['m00'])), 1, (0,0,255))
                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                    

    # check if the right number of contours are detected. If so calculate the
    # center of the two rectangles and draw that point on the image 
    if cntsDetected == 2:
        cXone = int(cntOneMoment['m10']/cntOneMoment['m00'])
        cYone = int(cntOneMoment['m01']/cntOneMoment['m00'])
        cXtwo = int(cntTwoMoment['m10']/cntTwoMoment['m00'])
        cYtwo = int(cntTwoMoment['m01']/cntTwoMoment['m00'])

        XcenterGoal = int((cXone + cXtwo) / 2)
        YcenterGoal = int((cYone + cYtwo) / 2)

        cv2.circle(frame, (int(XcenterGoal), int(YcenterGoal)), 1, (0,255,0),2)
        
    else:
        cv2.putText(frame, str(cntsDetected) +" detected", (5,470),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8 , (0,128,255),2)


    # show the image on the gui and check if the esc key has been pressed     
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) == 27:
           break;

    

cv2.destroyAllWindows(); # destroy the image window 





    

