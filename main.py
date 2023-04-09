import logging
import cv2
import asyncio
from Objects.Event import Event
from datetime import datetime
from Services import detect_faces, simple_detect_faces

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='{"dtTimeStamp": "%(asctime)s", "level": "%(levelname)s", '
                           '"function": "%(funcName)s()", "msg": "%(message)s"}')
log = logging.getLogger()


def capture_video(args, event):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = simple_detect_faces(frame)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.rectangle(frame, (0, 10), (370, 30), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), (0, 30), font, 1.0,
                    (255, 255, 255), 1)
        cv2.imshow('Capturing', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # click q to stop capturing
            break
        #
    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == '__main__':
    log.info("starting...")
    event = Event(datetime.now(), "Demo")
    asyncio.run(event.update("new status", datetime.now(), "Hello world"))
    import sys
    sys.exit(capture_video(sys.argv, event))
