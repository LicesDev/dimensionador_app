import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr_code(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qr_codes = decode(gray_img)
    return [qr.data.decode('utf-8') for qr in qr_codes]