import face_recognition
import cv2
import numpy as np
from subprocess import Popen

p = Popen(["/snap/bin/vlc", "Nike.mp4"])

# Open the input movie file
input_video = cv2.VideoCapture(0)
length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

known_faces = []

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

frames = []
id = 1

while True:
    # Grab a single frame of video
    ret, frame = input_video.read()

    frame_number += 1

    if frame_number % 4 != 0:
        continue

    # Quit when the input video file ends
    if not ret:
        break
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    print(type(face_encodings))

    name_indices = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        if not match:
            for en in face_encodings:
                known_faces.append(en)
                name = "user" + str(id)
                print(name)
                id = id + 1
                face_names.append(name)
                name_indices.append(len(face_names) - 1)

        elif any(match) == False:
            known_faces.append(face_encoding)
            name = "user" + str(id)
            print(name)
            id = id + 1
            face_names.append(name)
            name_indices.append(len(face_names) - 1)

        else:
            for i in range(len(match)):
                if match[i]:
                    name_indices.append(i)
                    break

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, name_indices):
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, face_names[name], (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    cv2.namedWindow('Display window', 300)
    cv2.imshow("Display window", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# All done!
input_video.release()
cv2.destroyAllWindows()
