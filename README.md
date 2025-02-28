Creado por: Mariaisabel Zuluaga Quintero, Santiago Machado Serna

# Segmentación Socioeconómica de Países usando K-Means Clustering

## Descripción

Este proyecto implementa el algoritmo **K-Means** en Python utilizando **pandas** y **numpy**. Es una técnica de aprendizaje automático no supervisado que permite agrupar datos en clusters según sus similitudes. Se aplica en segmentación de clientes, reconocimiento de patrones y compresión de datos.

## 📥 Entradas

- **dataset**:  
  DataFrame de pandas con datos numéricos. Cada fila representa un punto de datos y cada columna una característica.

- **num_centroids**:  
  Entero positivo que define el número de clusters (debe ser menor o igual al número de muestras).

- **max_i**:  
  Entero positivo que indica el número máximo de iteraciones antes de detenerse.

## 📤 Salidas

- **Coordenadas de los centroides refinados**:  
  Lista de tuplas con los centroides finales.

- **Dataset modificado** que incluye:
  - Datos normalizados para `GDP_per_capita`, `life_expectancy` y `literacy_rate`.
  - Columna `assigned_cluster`: Índice del cluster asignado a cada punto de datos.

---

## Proceso de K-Means: Resumen

1. **Inicialización:**  
   Se seleccionan aleatoriamente `k` centroides a partir de los datos.

2. **Asignación de clusters:**  
   Cada punto se asigna al centroide más cercano, formando clusters según la similitud.

3. **Actualización de centroides:**  
   Se recalcula el centroide de cada cluster como la media de los puntos que lo conforman.

4. **Iteración:**  
   Se repiten los pasos de asignación y actualización hasta que los centroides se estabilizan o se alcanza el número máximo de iteraciones.

---

## Instalación

1. **Requisitos Previos**

   - Python 3.6 o superior
   - Poetry para las dependencias

2. **Clonar el repositorio**

   ```sh
   git clone https://github.com/sanma613/machine_learning
   cd machine_learning
   ```

---

## Recomendaciones

- En el repositorio se incluye un archivo con datos de prueba. Se recomienda utilizarlo para verificar el funcionamiento del algoritmo y comprender la estructura esperada del dataset.

- Si deseas usar o crear tu propio dataset, asegúrate de incluir las columnas `GDP_per_capita`, `life_expectancy` y `literacy_rate`, ya que son fundamentales para el análisis y la correcta ejecución del modelo.

- Antes de ejecutar el algoritmo, revisa que todos los datos sean numéricos y no contengan valores nulos o inconsistencias que puedan afectar el rendimiento del clustering.

- Para obtener resultados más precisos, experimenta con diferentes valores de `num_centroids` y `max_i`, ajustándolos según la distribución de los datos.

- Visualiza los resultados mediante gráficos para analizar la distribución de los clusters y validar la segmentación realizada por el modelo.
