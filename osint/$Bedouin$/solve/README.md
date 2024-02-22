# \$Bedouin\$

El reto nos pide identificar a una persona y origen/destino de un vuelo.

Analizando la imagen podemos identificar AA (American Airlines), pero no es suficiente. Es importante darse cuenta de que la foto no tiene metadatos útiles, por lo que aunque identifiquemos el aeropuerto origen el destino va a ser imposible con sólo esta información, ya que no hay posibilidad de filtrar por fecha (la descripción del reto es muy poco detallada en cúando sale el vuelo).

Llegados a este punto, la otra pista que tenemos es "Razz was here". 

Haciendo busquedas generales por keywords como bitcoin y hacker junto con razz, rápidamente salen muchos resultados de "Heather Morgan".

![Duck duck go query](./ddg_search.png)

En la mayoría de los artículos mencionan su nombre completo así como su nombre de rapper (en el reto se hace referencia a un "nombre artístico"), que es el que tendremos que usar en la flag final: Razzlekhan.

También nos piden el usuario que usa en las redes sociales activas. Haciendo una búsqueda por Instagram sólo salen cuentas privadas o públicas que se ve claramente que no es esta persona. Por el contrario, buscando en Twitter por su nombre o por "Razzlekhan" sale rápidamente una cuenta: @HeatherReyhan.

Sólo nos faltaría una parte de la flag, que es el origen y destino del vuelo de la foto. En el reto se especifica que la foto la subió a una de sus redes sociales meses antes del hack. Con una búsqueda rápida se puede saber que el hack ocurrió en agosto de 2016, por lo que tenemos que buscar unos meses antes (por ejemplo, desde enero) y, si no lo encontramos, ir más atrás.

Importante: La búsqueda avanzada de Twitter es la opción más obvia, pero hay que tener cuidado ya que si filtramos por fotos y vídeos el máximo son 50, y es probable que no encontremos la foto. Si directamente buscamos desde el perfil no nos saltamos resultados ;).

Buscando entre las fotos encontramos el siguiente tweet del 19 de abril 2016:

[https://twitter.com/HeatherReyhan/status/722418484529930244](https://twitter.com/HeatherReyhan/status/722418484529930244)

> "Goodbye #SFO! #Nairobi here I come! ✈️🐐😎💃🏻"

El aeropuerto origen es claramente SFO. Para encontrar el destino, una búsqueda rápida en google indica que en Nairobi sólo hay dos aeropuertos, y el que mayoritariamente recibe vuelos internacionales es el Aeropuerto Internacional Jomo Kenyatta, o en código IATA, NBO.

Flag: **HackOn{SFO_NBO_HeatherReyhan_Razzlekhan}**
