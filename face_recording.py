import numpy as np
import face_recognition as fr
import cv2
from datetime import datetime

def face():

    video_capture = cv2.VideoCapture(0)

    nandini_image = fr.load_image_file("photos/nandini.jpg")
    nandini_face_encoding = fr.face_encodings(nandini_image)[0]

    dishant_image = fr.load_image_file("photos/DISHANT.jpg")
    dishant_face_encoding = fr.face_encodings(dishant_image)[0]

    shruti_image = fr.load_image_file("photos/SHRUTI.jpg")
    shruti_face_encoding = fr.face_encodings(shruti_image)[0]

    noopur_image = fr.load_image_file("photos/NOOPUR.jpg")
    noopur_face_encoding = fr.face_encodings(noopur_image)[0]

    anand_image = fr.load_image_file("photos/ANAND G.jpg")
    anand_face_encoding = fr.face_encodings(anand_image)[0]

    aditi_image = fr.load_image_file("photos/ADITI.jpg")
    aditi_face_encoding = fr.face_encodings(aditi_image)[0]

    radhika_image = fr.load_image_file("photos/RADHIKA.jpg")
    radhika_face_encoding = fr.face_encodings(radhika_image)[0]

    known_face_encondings = [
        nandini_face_encoding,
        dishant_face_encoding,
        shruti_face_encoding,
        noopur_face_encoding,
        anand_face_encoding,
        aditi_face_encoding,
        radhika_face_encoding
    ]

    known_face_names = [
        "NANDINI",
        "DISHANT",
        "SHRUTI",
        "NOOPUR",
        "ANAND",
        "ADITI",
        "RADHIKA"
    ]
        
        

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'recordings/{datetime.now().strftime("%H-%M-%S")}.avi', fourcc,20.0,(640,480))


    while True: 
            
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        cv2.putText(frame, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,255,255), 2)
        out.write(frame)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = fr.compare_faces(known_face_encondings, face_encoding)

            name = "Unknown"

            face_distances = fr.face_distance(known_face_encondings, face_encoding)

            best_match_index = np.argmin(face_distances)

            if True in matches:
                best_match_index = matches.index(True)
                name = known_face_names[best_match_index]
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Facerecognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()