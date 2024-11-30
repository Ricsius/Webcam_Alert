import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread

IMAGES_PATH = "images"
video = cv2.VideoCapture(0)
first_frame = None
status_list = []
count = 1

def clean_images_directory():
    images = glob.glob(f"{IMAGES_PATH}/*.png")

    for image in images:
        os.remove(image)

time.sleep(1)

while True:
    status = False
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        fake_object = cv2.contourArea(contour) < 5000

        if fake_object:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if rectangle.any():
            cv2.imwrite(f"{IMAGES_PATH}/{count}.png", frame)
            
            status = True
            count += 1
            all_images = glob.glob(f"{IMAGES_PATH}/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]
    
    status_list.append(status)
    status_list = status_list[-2:]
    object_exited_view = status_list[0] and not status_list[1]
    
    if object_exited_view:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        email_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):

        break

video.release()

cleaning_thread = Thread(target=clean_images_directory)
cleaning_thread.daemon = True
cleaning_thread.start()