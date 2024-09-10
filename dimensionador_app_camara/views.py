from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import cv2
from pyzbar.pyzbar import decode

#ACA PEGAR VIDEO
def gen_frames():
    camera = cv2.VideoCapture(2) 
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                print(f"QR encontrado: {qr_data}")
                yield f"data: {qr_data}\n\n"  # Enviar datos SSE solo cuando se detecte un QR

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
def qr_webcam():
    consolidado_qr=[]
    camera = cv2.VideoCapture(0)   
    det = cv2.QRCodeDetector()
    for barcode in decode(camera.getCvFrame()):
        myData = barcode.data.decode('utf-8')
        if myData != "":
            consolidado_qr.append(myData)
            break
            #cv2.imshow("video", videoFrame.getCvFrame())
        if len(consolidado_qr)>1:
                break
        consolidado_qr={"QR":[myData]}
    return consolidado_qr
       

def video_feed(request):
    return StreamingHttpResponse(qr_webcam(), content_type='multipart/x-mixed-replace; boundary=frame')

def sse_view(request):
    return StreamingHttpResponse(gen_frames(), content_type='text/event-stream')
