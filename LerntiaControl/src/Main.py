import cv2

print("Welcome to LerntiaControl!")
print("OpenCV Version: ", cv2.__version__, '\n')

cap = cv2.VideoCapture(0)

while True:
    # capture frame
    ret, frame = cap.read()

    # display frame
    cv2.imshow('[LerntiaControl] Mouse control by tracking eyes and face gestures', frame)

    # if 'q' button pressed => release camera handle and close
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break


