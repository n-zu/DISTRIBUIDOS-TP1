# Bike Rides Analyzer

> TP1 de Sistemas Distribuidos - Middleware y Coordinación de Procesos

## Requerimientos Funcionales

- Se solicita un sistema distribuido que analice los registros de viajes realizados con bicicletas de la red pública provista por grandes ciudades.
- Los registros cuentan con el tiempo de duración del viaje, estación de inicio y de fin.
- Se posee también lat., long. y nombre de las estaciones así como la cantidad de precipitaciones del día del viaje.
- Los registros se ingresan progresivamente, al recibirse de cada ciudad.
- Se debe obtener:
  - La duración promedio de viajes que iniciaron en días con precipitaciones >30mm
  - Los nombres de estaciones que al menos duplicaron la cantidad de viajes iniciados en ellas entre 2016 y el 2017.
  - Los nombres de estaciones de Montreal para la que el promedio de los ciclistas recorren más de 6km en llegar a ellas.

## Requerimientos No Funcionales

- Para construir una simulación realista se define la serie de datos: [public-bike-sharing-in-north-america](https://www.kaggle.com/datasets/jeanmidev/public-bike-sharing-in-north-america)
- Considerar el uso de la librería **haversine** para calcular distancias.
- El sistema debe estar optimizado para entornos multi-computadoras
- Se debe soportar el incremento de los elementos de cómputo para escalar los volúmenes de información a procesar
- De ser necesaria una comunicación basada en grupos, se requiere
- la definición de un middleware
- Se debe soportar una única ejecución del procesamiento y proveer graceful quit frente a señales SIGTERM.

## \_temp

- **Diagramas Principales**

  - robustez
  - despliegue
  - actividades

- **Datos**:

  - Viajes: Ingresados por cliente
  - Clima / Estaciones:
    - Ingresados por cliente
    - Datos estáticos
      - Cargados en memoria
      - Storage de consulta externo

- **Pipeline**:
  - **Enriquecer datos**: tomar datos de viaje y agregarle información relevante (precipitaciones, distancia, etc)
  - **Formatear datos**: dar un formato a partir del cual podamos calcular las estadísticas relevantes
  ```json
  {
    "viajes_con_precipitaciones_mayor_a_30mm": {
      "duracion_total": 0,
      "viajes": 0
    },
    "cantidad_de_viajes": {
      "estacion1": [2016, 2017],
      "estacion2": [2016, 2017]
    },
    "estaciones_montreal": {
      "estacion1": {
        "tiempo_en_llegar_total": 0,
        "cantidad_de_viajes": 0
      },
      "estacion2": {}
    }
  }
  ```
  - **Agrupar datos**: juntar la información formateada en un único objeto
