# Bike Rides Analyzer

> TP1 de Sistemas Distribuidos - Middleware y Coordinación de Procesos

## Requerimientos Funcionales

Sistema distribuido que analiza los registros de viajes realizados con bicicletas de la red pública provista por grandes ciudades ([public-bike-sharing-in-north-america](https://www.kaggle.com/datasets/jeanmidev/public-bike-sharing-in-north-america)).

Se ingresan registros de viaje progresivamente al sistema, al finalizar la ejecución el cliente recibe los siguientes resultados:

- La duración promedio de viajes que iniciaron en días con precipitaciones >30mm
- Los nombres de estaciones que al menos duplicaron la cantidad de viajes iniciados en ellas entre 2016 y el 2017.
- Los nombres de estaciones de Montreal para la que el promedio de los ciclistas recorren más de 6km en llegar a ellas.

El sistema esta pensado para entornos multi-computadoras, soportando el incremento de los elementos de cómputo para escalar los volúmenes de información a procesar

## Ejecución

Dentro del directorio `src` ejecutar:

- `make up` para levantar el sistema en docker
- `make down` para bajar el sistema

## Documentación

Puede encontrarse el documento de arquitectura 4+1 en el directorio [docs](/docs/README.md)
