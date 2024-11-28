# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport
from app.models import Favourite

def getAllImages(input=None):
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = transport.getAllImages(input)

    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for object in json_collection:
        card=translator.fromRequestIntoCard(object)
        images.append(card)


    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    #obtener los datos
    image_name=request.POST.get('name')
    image_url = request.POST.get('url')
    image_status = request.POST.get('status')
    image_last_location = request.POST.get('last_location')
    image_first_seen = request.POST.get('first_seen')

    #asignar usuario logeado
    user=request.user

    # Crear un nuevo favorito para este usuario
    fav = {
        'name': image_name,
        'url': image_url,
        'status': image_status,
        'last_location': image_last_location,
        'first_seen': image_first_seen,
        'user': user
    }

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:
        return []
    #obtener user logeado
    user=request.user

    favourite_list = Favourite.objects.filter(user=user) # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
    mapped_favourites = []

    for favourite in favourite_list:
            card = translator.fromFavouriteToCard(favourite) # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

    return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    favourite=Favourite.objects.get(id=favId)
    favourite.delete() # borramos un favorito por su ID.