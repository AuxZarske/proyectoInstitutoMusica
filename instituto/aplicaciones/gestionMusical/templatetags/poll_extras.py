from django import template
import base64

register = template.Library()

@register.filter(name='binary_to_image')
def encode_binary_data_to_image(binary):
     #ver porque el objeto binari no tiene atributo read, necesario para convertir

    
    binary = base64.b64encode(binary)
    cadena = str(binary)
    cadena = cadena[2:]

    total = len(cadena)
    cadena = cadena[:total - 1]
    return cadena
            # return your encoded binary, I would suggest base64.encode which is pretty simple