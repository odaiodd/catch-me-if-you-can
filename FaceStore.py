import face_recognition
import cv2
import numpy as np
import init_DB as DB
from Client import Client


class FaceStore:

    def __init__(self, store_id, ad_id):
        self.store_id = store_id
        self.ad_id = ad_id
        self.known_faces_users = []
        self.matches = []
        self.matches_ids = []

    def start(self):
        input_video, frame_number = cv2.VideoCapture(0), 0

        while True:
            frame, frame_number, rgb_frame = self.get_frame(input_video, frame_number)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # get clients and faces from db
            frame_number = self.get_faces_from_db(frame_number)

            ##put maches in db
            self.put_match_in_db(face_encodings)

            # draw on screen
            self.draw_on_screen(face_locations, frame, face_encodings)

        # All done!
        input_video.release()
        cv2.destroyAllWindows()

    def get_faces_from_db(self, frame_number):
        clients_list = []
        if frame_number == 12:
            for element in DB.storage.my_DB.find():
                clients_list.append(
                    Client(element["face_id"], element["screen_id"], element["ad_id"], element["encoding"],
                           element['time'], element['image']))
            self.known_faces_users = clients_list.copy()
            frame_number = 0
        return frame_number

    def get_frame(self, input_video, frame_number):
        ret, frame = input_video.read()
        frame_number += 1
        return frame, frame_number, frame[:, :, ::-1]

    def put_match_in_db(self, face_encodings):
        if face_encodings:
            for user in self.known_faces_users:
                match = face_recognition.compare_faces(face_encodings, np.array(user.encoding), tolerance=0.55)
                if any(match):
                    if user.id not in self.matches_ids:
                        self.matches_ids.append(user.id)
                        self.matches.append(user)
                        ## put client in db
                        DB.storage_stores.add_my_db(user.id, user.ads_id, self.store_id, np.array(user.img), user.time)

    def draw_on_screen(self, face_locations, frame, face_encodings):
        if face_locations:
            known_faces_encodings = [user.encoding for user in self.matches]
            for i, (top, right, bottom, left) in enumerate(face_locations):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
                match = face_recognition.compare_faces(known_faces_encodings, face_encodings[i], tolerance=0.55)
                # print(match)
                index = [i for i, x in enumerate(match) if x]
                if len(match) > 0:
                    if (any(match)):
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, f"user {self.matches[index[0]].id}", (left + 6, bottom - 6), font, 0.5,
                                    (255, 255, 255), 1)

                cv2.namedWindow('Display window', cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Display window", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass


a = FaceStore(1, 37)
a.start()
