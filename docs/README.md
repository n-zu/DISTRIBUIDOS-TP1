# Bike Rides Analyzer - Docs

## Scope

El proyecto Bike Rides Analyzer consiste en el diseño y desarrollo de un sistema distribuido que analiza registros de viajes realizados con bicicletas en la red pública de grandes ciudades.
Los registros contienen información sobre la duración del viaje, estación de inicio y fin, y se complementa con datos de la ubicación y nombre de las estaciones, así como la cantidad de precipitaciones del día del viaje.

## Scenarios

### Requerimientos Funcionales

- Se solicita un sistema distribuido que analice los registros de viajes realizados con bicicletas de la red pública provista por grandes ciudades.
- Los registros cuentan con el tiempo de duración del viaje, estación de inicio y de fin.
- Se posee también lat., long. y nombre de las estaciones así como la cantidad de precipitaciones del día del viaje.
- Los registros se ingresan progresivamente, al recibirse de cada ciudad.
- Se debe obtener:
  - La duración promedio de viajes que iniciaron en días con precipitaciones >30mm
  - Los nombres de estaciones que al menos duplicaron la cantidad de viajes iniciados en ellas entre 2016 y el 2017.
  - Los nombres de estaciones de Montreal para la que el promedio de los ciclistas recorren más de 6km en llegar a ellas.

### Casos de Uso

- El usuario obtiene las estadísticas finales del sistema.

## Software Architecture

El sistema distribuido Bike Rides Analyzer estará compuesto por varios componentes que trabajarán juntos para procesar los registros de viajes realizados con bicicletas. A continuación, se describen los principales componentes de la arquitectura:

### Cliente

El cliente será el componente principal del sistema, encargado de coordinar el procesamiento distribuido de los registros de viajes. Su función será la de recibir los datos de clima y estaciones, repartir el trabajo entre los diferentes workers y recibir los resultados finales.

### Workers

Los workers serán los encargados de procesar los registros de viajes recibidos del cliente. Cada worker ejecutará el mismo proceso, consistente en enriquecer los datos de los viajes con información adicional sobre las estaciones y el clima y acumular los resultados parciales en un formato que permita calcular las estadísticas requeridas.

### Sink

El sink será el encargado de recibir los resultados parciales enviados por los workers y combinarlos en un único objeto que contendrá todas las estadísticas finales. Este componente enviará el resultado final al cliente para su posterior procesamiento y análisis.

### Middleware

Se utilizará un middleware específico para la comunicación entre los componentes del sistema.
Este middleware se encargará de la serialización y deserialización de los mensajes intercambiados entre los componentes, así como de la distribución de los mensajes entre los workers.
El middleware permite la comunicación utilizando patrones de request-reply, publish-subscribe y push-pull.

## Architectural Goals & Constraints

- El sistema debe estar optimizado para entornos multi-computadoras y soportar el incremento de los elementos de cómputo para escalar los volúmenes de información a procesar.
- La comunicación entre los componentes se realiza a través de un middleware específico que se adapta a las necesidades del sistema.
- El sistema debe proveer un mecanismo de graceful quit frente a señales SIGTERM.
- Recepción de registros de viajes progresivamente, a medida que se reciben de diferentes ciudades.
- El soporte de una única ejecución del procesamiento y el manejo de señales SIGTERM.

## Logical View

En esta sección se describirán las clases y estados relevantes del sistema, mostrando cómo se relacionan entre sí y cómo cumplen con los requerimientos funcionales y no funcionales.

### Classes

### States

### Flujo de datos

El siguiente DAG representa el flujo de datos del sistema:

![dataflow](diagrams/dataflow.png)

La información de los archivos de clima, estaciones y viajes puede ser agregada en un registro, mientras que la ciudad es un dato implícito de los archivos.

A partir de este registro podemos separar 3 ramas, una para cada estadística requerida.

A continuación, se plantea un modelo a partir del cual transformamos la información de un registro en un objeto que nos permita calcular las estadísticas requeridas.

![dataflow2](diagrams/dataflow2.png)

Se presenta el formato de objeto a partir del análisis previo:

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

> Es importante notar que una estación esta definida no solo por su nombre, sino también por la ciudad en la que se encuentra.

Podemos ver como esta información puede irse acumulando de manera independiente de manera paralela, y luego ser combinada en un único objeto que contenga la información de todas las estadísticas.

#### Pipeline

De ese modo, se define un pipeline que consiste de los siguientes pasos:

- **Enriquecer datos**: tomar datos de viaje y agregarle información relevante (precipitaciones, distancia, etc)
- **Formatear datos**: dar un formato a partir del cual podamos calcular las estadísticas relevantes
- **Agrupar datos**: juntar la información formateada en un único objeto que sera entregado al cliente

```mermaid
graph LR
A[Enriquecer datos] --> B[Formatear datos]
B --> C[Agrupar datos]
```

## Process View

En esta sección se describirán los flujos de secuencia y las actividades relevantes del sistema, mostrando cómo se cumplen con los requerimientos funcionales y no funcionales.

### Sequences

### Activities

![activity diagram](diagrams/activity.png)

Vemos en el diagrama la interacción entre los componentes del sistema.

- El cliente envía los datos de clima a todos los workers, utilizando un patron pub-sub.
- El cliente envía los datos de estaciones a todos los workers, utilizando un patron pub-sub.
- El cliente envía los datos de viaje a los workers de manera distribuida, utilizando un patron push-pull.
  - Los clientes procesan los datos según el [pipeline](#pipeline) definido previamente.
- Los workers envían los resultados parciales al sink, que los agrega en un único objeto y los envía al cliente.

## Development View

En esta sección se describirán los componentes y paquetes relevantes del sistema, mostrando cómo se organizan y cómo se cumplen con los requerimientos funcionales y no funcionales.

### Components

### Packets

## Physical View

La vista física muestra cómo los componentes del sistema se despliegan en la infraestructura de hardware. En nuestro caso, el sistema distribuido está diseñado para ser desplegado en un entorno multi-computadora.

### Deployment

![deployment diagram](diagrams/deployment.png)

Los nodos son desplegados de manera independiente, y se comunican entre sí a través de un middleware específico.

El middleware en cuestión se basa en [ZeroMQ](http://zeromq.org/), de modo que no tendremos un nodo centralizado que coordine la comunicación entre los nodos, sino que cada nodo se conectará a los demás nodos que necesite.

### Robustness

![robustness diagram](diagrams/robustness.png)

Como vemos en el diagrama que, se prevé el escalamiento de workers, a modo de incrementar el computo mediante un modelo de _Worker por Item_.

---

## OLD

Esquemas viejos donde se consideraban las siguientes opciones:

- El uso de rabbitmq: se descarto debido a que generaba gran dependecia y este seria cargado con todos los mensajes del sistema.
- Los archivos estaticos de _weather_ y _stations_ pueden ser levantados en memoria desde cualquier parte del sistema. Se aclaro luego que debe ser enviado por el cliente.
- Se hace una mezcla de _Worker por Filter_ y _Worker por Item_. Esto se descarto luego ya que se considero que el procesamiento de un dato es simple y justifica la comunicación con otra elemento de procesamiento; de modo que se simplifica el sistema.

![old_deployment](diagrams/old_deployment.svg)
![old_robustness](diagrams/old_robustness.png)
