#from django.shortcuts import get_list_or_404, render
from .models import Destino, Alojamiento, Desplazamiento, Paquete, Viaje, Foto
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.db.models import Q


def buscarViaje(request):
   dest = Destino.objects.all()
   context = {
        'destinos': dest,
    }
   plantilla = loader.get_template('viaje_search.html')
   return HttpResponse(plantilla.render(context, request))

# def vista2(request):
#     dest = Destino.objects.all()
#     alo = Alojamiento.objects.all()
#     desp = Desplazamiento.objects.all()
#     paq = Paquete.objects.all()
#     via = Viaje.objects.all()

#     context = {
#         'destinos': dest,
#         'alojamientos': alo,
#         'desplazamientos': desp,
#         'paquetes': paq,
#         'viajes': via,
#     }
#     plantilla = loader.get_template('viaje_vista2.html')
#     return HttpResponse(plantilla.render(context, request))

def vista3(request):
    dest = Destino.objects.all()
    alo = Alojamiento.objects.filter(destino__nombre=request.POST['destino'], nhabitaciones__gte=request.POST['viajeros']).prefetch_related('foto_set')
    despOrigen = Desplazamiento.objects.filter(origen__nombre=request.POST['origen'] , destino__nombre=request.POST['destino'])
    despDestino = Desplazamiento.objects.filter(origen__nombre=request.POST['destino'] , destino__nombre=request.POST['origen'])
    paq = Paquete.objects.filter(destino__nombre=request.POST['destino'])
    nHuespedes = request.POST['viajeros']
    salida = request.POST['salida']
    llegada = request.POST['llegada']

    print(despOrigen, despDestino)

    context = {
        'destinos': dest,
        'alojamientos': alo,
        'desplazamientosOrigen': despOrigen,
        'desplazamientosDestino': despDestino,
        'paquetes': paq,
        'nHuespedes': nHuespedes,
        'salida': salida,
        'llegada': llegada,
    }
    plantilla = loader.get_template('viaje_vista2.html')
    return HttpResponse(plantilla.render(context, request))

def home(request):
    # Lógica de la vista home
    return render(request, 'viaje_vista2.html')

def registrar(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../nuevologin')  # Utiliza reverse para generar la URL de la vista 'home'
    else:
        form = RegisterForm()
    return render(request, 'registrar.html', {'form': form})

def nuevologin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../nuevoViaje')  # Utiliza reverse para generar la URL de la vista 'home'
        else:
            print(password,username,user)
            return render(request, 'nuevologin.html')
    return render(request, 'nuevologin.html')

@login_required
def guardar_viaje(request):
    if request.method == 'GET':
        # Obtener los datos del formulario
        alojamiento_id = request.GET.get('alojamiento')
        desp_ida_id = request.GET.get('despIda')
        desp_vuelta_id = request.GET.get('despVuelta')
        n_huespedes = request.GET.get('nHuespedes')
        salida = request.GET.get('salida')
        llegada = request.GET.get('llegada')

        # Obtener el usuario logueado
        usuario = request.user

        # Crear una instancia del modelo Viaje con los datos recibidos y el usuario logueado
        viaje = Viaje(
            usuario=usuario,
            alojamiento_id=alojamiento_id,
            desplazamientoIda_id=desp_ida_id,
            desplazamientoVuelta_id=desp_vuelta_id,
            nHuespedes=n_huespedes,
            salida=salida,
            llegada=llegada
        )

        # Establecer valores adicionales en el modelo
        viaje.valor_adicional = "Valor adicional"

        # Guardar el viaje en la base de datos
        viaje.save()

        # Redirigir a una página de éxito o a otra vista
        return redirect('nombre_de_la_vista')

    return render(request, 'formulario.html')