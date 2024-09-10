from django.http import JsonResponse

def leer_lpn(request):
    data = {'lpn': '7100907490000051225251'}
    return JsonResponse(data)

def dimensionar(request):
    data = {
        'largo': '18.0',
        'ancho': '29.0',
        'altura': '18.0',
        'peso': '10',
        'infoAdicional': 'Información adicional'
    }
    return JsonResponse(data)
