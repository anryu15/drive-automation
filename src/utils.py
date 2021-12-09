import cv2
import time
from config import IMAGE_DIR

#capture camera frame then make jpg image
def capture_camera(show=False, name=None):
    if name == None:
        print("must fill name")
        return
    capture = cv2.VideoCapture(0)
    loop_count = 0
    while (capture.isOpened()):
        ret, image = capture.read()
        if loop_count > 100:
            print("no capture found")
        if ret:
            cv2.imwrite(f"{IMAGE_DIR}/{name}.jpg", image)
            text = 'WIDTH={:.0f} HEIGHT={:.0f} FPS={:.0f}'.format(capture.get(cv2.CAP_PROP_FRAME_WIDTH),capture.get(cv2.CAP_PROP_FRAME_HEIGHT),capture.get(cv2.CAP_PROP_FPS))
            cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),1,4)
            capture.release ()
            if show:
                cv2.imshow('Frame', image)
                time.sleep(1)
                cv2.destroyAllWindows()
            break
        loop_count += 1
    return
