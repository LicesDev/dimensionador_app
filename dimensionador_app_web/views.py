from django.shortcuts import render
from django.http import JsonResponse
from .models import Dimensiones

def Home(request):
    return render(request, 'home/home.html')


def guardar_dimensiones(request):
    if request.method == 'POST':
        lpn = request.POST.get('lpn')
        largo = request.POST.get('largo')
        alto = request.POST.get('alto')
        ancho = request.POST.get('ancho')
        fecha = request.POST.get('fecha')

        if lpn and largo and alto and ancho:
            dimensiones = Dimensiones(lpn=lpn, largo=largo, alto=alto, ancho=ancho, fecha=fecha)
            dimensiones.save()
            print('GUARDO')
            return JsonResponse({'status': 'success', 'message': 'Dimensiones guardadas correctamente'})
        else:
            print('NO GUARDO')
            return JsonResponse({'status': 'error', 'message': 'Error al guardar las dimensiones'})

    return render(request, 'home/home.html')