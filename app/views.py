# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.layers.utilities.card import Card

def index_page(request):
    return render(request, 'index.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si el usuario es válido, lo autenticamos y redirigimos a la página principal
            login(request, user)
            return redirect('home')  # O la vista a la que desees redirigir al usuario

        else:
            # Si las credenciales son incorrectas
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return redirect('login')  # Redirige de nuevo al formulario de login

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()
    favourite_list = []
    if request.user.is_authenticated:
        #Si el usuario se logea, se obtienen los favoritos
        favourite_list=services.getAllFavouritesByUser(request.user)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '').strip()

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images=services.getAllImages()
        filtered_images = [img for img in images if search_msg.lower() in img.name.lower()]
        return render (request, 'search.html', {'images':filtered_images, 'query':search_msg})
        
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method=='POST':
        image_name=request.POST.get('name')
        image_url=request.POST.get('url')
        image_status=request.POST.get('status')
        image_last_location=request.POST.get('last_location')
        image_first_seen=request.POST.get('first_seen')
        #llamar al servicio de guardado
        services.saveFavourite(request.user, image_name, image_url, image_status, image_last_location, image_first_seen)

        return redirect('home') #redirige a la página principal

@login_required
def deleteFavourite(request):
    if request.method=='POST':
        image_name=request.POST.get('name')
        #llamar al servicio de eliminado
        services.deleteFavourite(request.user, image_name)

        return redirect('home')

@login_required
def exit(request):
    pass