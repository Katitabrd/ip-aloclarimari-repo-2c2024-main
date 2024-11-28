# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from django.http import HttpRequest
from ..transport import transport
from app.models import Favourite
from ...layers.services import services
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
def saveFavourite(user, name, url, status, last_location, first_seen):
    # Crear un nuevo objeto Favourite y guardarlo en la base de datos
    fav = Favourite(
        user=user,  # Usa el usuario autenticado directamente
        name=name,
        url=url,
        status=status,
        last_location=last_location,
        first_seen=first_seen
    )
    fav.save()  # Guarda el objeto en la base de datos

    return fav
    

# usados desde el template 'favourites.html'
def getAllFavouritesByUser(user):
    

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