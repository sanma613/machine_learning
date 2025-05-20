# Segmentación Socioeconómica de Países usando K-Means Clustering

**Autores:**

- María Isabel Zuluaga Quintero
- Santiago Machado Serna

**Interfaz Gráfica:**

- Kevin Sebastián Cifuentes
- Sebastián Valencia Valencia

## 🧠 Descripción del Proyecto

Este proyecto implementa el algoritmo **K-Means Clustering** en Python utilizando **pandas** y **numpy**. K-Means es una técnica de aprendizaje no supervisado que permite agrupar datos en clusters según su similitud multidimensional.

El proyecto está enfocado en la segmentación socioeconómica de países utilizando indicadores clave como:

- PIB per cápita
- Esperanza de vida
- Tasa de alfabetización

Esta herramienta puede aplicarse en diversas áreas como:

- Segmentación de clientes en marketing
- Reconocimiento de patrones en grandes conjuntos de datos
- Análisis socioeconómico y geopolítico de países
- Identificación de comportamientos similares en poblaciones diversas

## 🗂️ Estructura del Proyecto

```
machine_learning/
├── src/
│   ├── model/
│   │   ├── kmeans_logic.py              # Algoritmo K-Means
│   │   ├── errors/
│   │   │   └── kmeans_error.py          # Manejo de errores específicos
│   │   └── result_model.py              # Modelo de resultados para BD
│   ├── controller/
│   │   └── results_controller.py        # Controlador para interactuar con BD
│   ├── view/
│   │   ├── console/
│   │   │   └── kmeans_console_view.py   # Interfaz de consola
│   │   └── gui/
│   │       └── kmeans_gui.py            # Interfaz gráfica
├── tests/
│   └── kmeans_test.py                     # Pruebas unitarias
├── casos_prueba.xlsx                    # Documentación de casos de prueba
├── datos_prueba.csv                     # Dataset de prueba
├── secret_config.py                     # Configuración de conexión a BD (no incluido en repo)
├── estructura.txt                       # Descripción de la estructura del proyecto
├── requirements.txt                    # Configuración del proyecto
└── README.md                            # Este archivo
```

## ⚙️ Instalación

### 1. Requisitos previos

- Python 3.6 o superior
- PostgreSQL (recomendamos usar Neon como servicio en la nube)

### 2. Clonar el repositorio

```sh
git clone https://github.com/sanma613/machine_learning.git
cd machine_learning
```

### 3. Instalar dependencias

```sh
pip install -r requirements.txt
```

## 🛠️ Configuración de la Base de Datos (PostgreSQL con Neon)

Este proyecto utiliza PostgreSQL como base de datos, preferentemente a través de **Neon**, un servicio de PostgreSQL serverless en la nube.

### 1. Crear cuenta y base de datos en Neon

1. Regístrate en [https://neon.tech](https://neon.tech)
2. Crea un nuevo proyecto
3. Dentro del proyecto, crea una base de datos (por ejemplo, `kmeans_db`)
4. Habilita el pooler de conexiones para mejorar el rendimiento
5. Obtén la cadena de conexión (Connection String) desde tu panel de control

### 2. Crear archivo `secret_config.py`

Este archivo contiene la URL de conexión a tu base de datos PostgreSQL. **¡Importante! No subas este archivo al repositorio.**

```python
# secret_config.py
DB_URL = "postgresql://usuario:contraseña@ep-nombre-proyecto-id-pooler.region.aws.neon.tech/nombre_db?sslmode=require"
```

Reemplaza los valores en la URL con los proporcionados por Neon:

- `usuario`: Nombre de usuario (normalmente nombre_db_owner)
- `contraseña`: Contraseña generada por Neon
- `nombre-proyecto-id`: ID único de tu proyecto en Neon
- `region`: Región donde está alojada tu BD (ej. us-east-1)
- `nombre_db`: Nombre de tu base de datos

### 3. Estructura de la base de datos

El programa creará automáticamente las tablas necesarias en la primera ejecución. No necesitas crear manualmente ninguna tabla.

## 🚀 Ejecución del Programa

### Interfaz de Consola

```sh
python src/view/console/kmeans_console_view.py
```

La interfaz de consola te permitirá:

- Cargar un dataset CSV
- Configurar parámetros del algoritmo K-Means
- Ejecutar el análisis de clustering
- Visualizar los resultados mediante gráficos
- Guardar los resultados en la base de datos
- Consultar, modificar o eliminar resultados previos

### Interfaz Gráfica (GUI)

```sh
python src/view/gui/kmeans_gui.py
```

La interfaz gráfica ofrece una experiencia más intuitiva para:

- Cargar y visualizar el dataset
- Configurar parámetros del algoritmo
- Visualizar resultados con gráficos interactivos 2D y 3D
- Guardar resultados y generar informes

## 📊 Uso del Dataset

### Formato Requerido

El programa espera un archivo CSV con las siguientes columnas:

- `GDP_per_capita`: PIB per cápita (numérico)
- `life_expectancy`: Esperanza de vida en años (numérico)
- `literacy_rate`: Tasa de alfabetización en porcentaje (numérico)

Si tu CSV tiene diferentes nombres de columnas, el programa te permitirá seleccionar columnas alternativas.

### Dataset de Prueba

Incluimos el archivo `datos_prueba.csv` con datos socioeconómicos de varios países para que puedas probar el sistema inmediatamente.

## 🧪 Pruebas Unitarias

Para ejecutar las pruebas unitarias:

```sh
python -m unittest tests/kmeans_test.py
```

Las pruebas cubren:

- **3 casos normales**: Verificación del comportamiento estándar
- **3 casos extraordinarios**: Manejo de situaciones límite
- **4 casos de error**: Validación de manejo de excepciones

## ⚙️ Proceso K-Means Implementado

1. **Normalización de datos**: Escalado de variables para evitar sesgos por diferentes unidades
2. **Inicialización de centroides**: Selección aleatoria de K puntos iniciales
3. **Asignación de clusters**: Asignar cada punto al centroide más cercano según distancia euclidiana
4. **Recálculo de centroides**: Actualizar la posición de cada centroide como la media de sus puntos asignados
5. **Iteración**: Repetir pasos 3 y 4 hasta convergencia o número máximo de iteraciones
6. **Visualización**: Generación de gráficos 2D y 3D para interpretar resultados

## 🔐 Notas sobre Seguridad

- El archivo `secret_config.py` contiene credenciales de conexión a la base de datos y **nunca debe compartirse públicamente**
- Está incluido en `.gitignore` para evitar subirlo accidentalmente
- Para entornos de producción, considera usar variables de entorno en lugar de archivos de configuración

## 📝 Recomendaciones de Uso

- Comienza con el dataset de prueba `datos_prueba.csv` para familiarizarte con el sistema
- Experimenta con diferentes valores de K (número de clusters) para encontrar la segmentación óptima
- Valores típicos para número máximo de iteraciones: entre 50 y 300
- Analiza los gráficos generados para interpretar las características de cada cluster
- Para datasets grandes, considera aumentar el número máximo de iteraciones
- Verifica que tus archivos CSV no contengan valores nulos ni datos no numéricos en las columnas de análisis

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Haz fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Realiza tus cambios
4. Ejecuta las pruebas para verificar que todo funciona correctamente
5. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
6. Haz push a la rama (`git push origin feature/amazing-feature`)
7. Abre un Pull Request
