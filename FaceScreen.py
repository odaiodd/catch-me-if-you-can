from datetime import datetime
import face_recognition
import cv2
import Client
import init_DB as DB
import numpy as np


KNOWN_DISTANCE = 25.0

class FaceScreen:

    def __init__(self, screen_id, ad_id):
        self.screen_id = screen_id
        self.ad_id = ad_id

    def check_exist(self, clients, cl):
        encodings = [np.array(c.encoding) for c in clients]
        if not clients:
            return False
        if (any(face_recognition.compare_faces(encodings, np.array(cl.encoding), tolerance=0.63))):
            return True
        return False

    def take_rgb_frame(self, input_video):
        ret, frame = input_video.read()
        frame = cv2.flip(frame, 1)
        return frame, frame[:, :, ::-1]

    def add_client(self, face_encodings, face_locations, clients, face_id, frame):
        if face_encodings:
            for i, encoding in enumerate(face_encodings):
                x, y, w, h = face_locations[i][0], face_locations[i][1], face_locations[i][2], face_locations[i][3]
                cl = Client.Client(face_id, self.screen_id, self.ad_id, encoding, datetime.now(), frame[x:w, h:y])
                if not self.check_exist(clients, cl):
                    clients.append(cl)
                    face_id += 1
        return clients, face_id

    def add_to_db(self, frame_number, clients, prev):
        if (frame_number == 15) and clients:
            for client in clients:
                if not self.check_exist(prev, client):
                    print("Good!")  # TODO: push the client to the DB
                    DB.add_to_table(client)
            prev = clients.copy()
            frame_number = 0
        return frame_number, clients, prev



    def draw_frame(self, face_locations, frame):
        if face_locations:
            for (top, right, bottom, left) in face_locations:
                # marker = find_marker(frame)
                # m = ((left, top), (right, bottom), marker[2])
                KNOWN_WIDTH = right - left
                focalLength = ((right * KNOWN_DISTANCE) / KNOWN_WIDTH)/10
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, f"""distance {"%.2f" % (focalLength * 2.54)} cm""", (left + 6, bottom - 6), font, 0.8,
                            (255, 255, 255), 1)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.imshow("Display window", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

    def start(self):
        frame_number, face_id, clients, prev, input_video = 0, 1, [], [], cv2.VideoCapture(0)

        while True:
            # Grab a single frame of video
            # print(frame_number)
            frame_number += 1
            frame, rgb_frame = self.take_rgb_frame(input_video)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            ## add faces from frame
            clients, face_id = self.add_client(face_encodings, face_locations, clients, face_id, frame)

            ## TODO calculate distance every loop!!!!!

            ## add to DB
            frame_number, clients, prev = self.add_to_db(frame_number, clients, prev)

            ## draw face on frame
            self.draw_frame(face_locations, frame)

        # All done!
        input_video.release()
        cv2.destroyAllWindows()



a = FaceScreen(1, 15)
a.start()
