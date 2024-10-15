from django.http import JsonResponse

def leer_lpn(request):
    from .lpn_cubi import qr_webcam
    data=''
    data= qr_webcam()
    print(data)
    #data = {'lpn': '710090749000005122525'}
    return JsonResponse(data)


#from dimensionador_app_web.dimensionar_app import dimens
def dimensionar(request):
    #from box_estimator_app import BoxEstimator
    #from lpn_cubi import main_dimensionador
    from .lpn_cubi import main_dimensionador
    data=''
    data = main_dimensionador()
    print(data)
    #data = {
    #    'largo': '189.0',
    #    'ancho': '29.0',
    #    'altura': '18.0',
    #    'peso': '10',
    #    'infoAdicional': 'Información adicional'
    #}
    return JsonResponse(data)
