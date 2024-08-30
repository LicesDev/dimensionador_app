from django.shortcuts import render
from .camara import capture_image
from .utils import read_qr_code

def scan_qr(request):
    image = capture_image()
    qr_codes = read_qr_code(image)
    return render(request, 'scanner/scan_result.html', {'qr_codes': qr_codes})