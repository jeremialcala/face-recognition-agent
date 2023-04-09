import face_recognition
import numpy as np
import cv2
import asyncio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from Objects.Face import Face, LandMark


known_face_encodings = []
known_face_names = []


def do_match(face_encodings, event):
    face_name = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        if len(matches) == 0:
            face = Face(eventId=event.get_id())
            face_name.append(str(face.get_face_id()))
            known_face_encodings.append(face_encoding)
            known_face_names.append(str(face.get_face_id()))
            asyncio.run(face.save_face())
        else:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                face_name.append(known_face_names[best_match_index])

    return face_name


def detect_faces(frame, event):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    fac_image = Image.fromarray(frame)
    names = do_match(face_encodings, event)

    for (top, right, bottom, left), name in zip(face_locations, names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        box = (left - 20, top - 30, right + 20, bottom + 20)
        area = fac_image.crop(box)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return frame


def simple_detect_faces(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Scale back up face locations since the frame we detected inwas scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        box = (left - 20, top - 30, right + 20, bottom + 20)
        area = Image.fromarray(frame[:, :, ::-1]).crop(box)

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    return frame
