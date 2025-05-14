import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

sys.path.append("src")

from model.kmeans_logic import Kmeans
from model.errors.kmeans_error import KmeansError
from model.result_model import ClusteringResult
from controller.results_controller import ResultsController

class ConsoleUI:
    def __init__(self):
        """Inicializa la interfaz de usuario y el controlador de resultados."""
        self.results_controller = ResultsController()
        self.results_controller.create_table()
        self.current_results = None
        self.centroid_centers = None
    
    def clear_screen(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Muestra el menú principal de la aplicación."""
        self.clear_screen()
        print("\n===== SISTEMA DE CLUSTERING K-MEANS =====")
        print("1. Ejecutar nuevo análisis de clustering")
        print("2. Ver resultados guardados")
        print("3. Modificar resultado")
        print("4. Eliminar resultado")
        print("5. Salir")
        
        option = input("\nSeleccione una opción (1-5): ")
        
        options = {
            "1": self.run_clustering_analysis,
            "2": self.view_saved_results,
            "3": self.modify_results_menu,
            "4": self.delete_results_menu,
            "5": self.exit_program
        }
        
        if option in options:
            options[option]()
        else:
            input("Opción no válida. Presione Enter para continuar...")
        
        # Volver al menú principal si no se ha salido del programa
        if option != "5":
            self.display_menu()
    
    def run_clustering_analysis(self):
        """Ejecuta un nuevo análisis de clustering K-means y guarda automáticamente el resultado."""
        self.clear_screen()
        print("\n===== EJECUTAR NUEVO ANÁLISIS DE CLUSTERING =====")
        
        file_path = input("Ingresa la ruta del dataset (CSV): ")
        try:
            num_centroids = int(input("Ingresa el número de centroides: "))
            max_iterations = int(input("Ingresa el número máximo de iteraciones: "))
            title = input("Ingresa un título para este análisis: ")  # Pedir título al inicio
        except ValueError:
            input("Error: Los valores ingresados deben ser numéricos. Presione Enter para continuar...")
            return
        
        try:
            # Procesar el archivo CSV
            dataset = self.process_file_path(file_path)
            
            # Intentar utilizar las columnas predefinidas
            try:
                filtered_dataset = dataset[["GDP_per_capita", "life_expectancy", "literacy_rate"]]
            except KeyError:
                print("El dataset no contiene las columnas predefinidas.")
                alternative_columns = self.suggest_alternative_columns(dataset)
                if alternative_columns:
                    filtered_dataset = dataset[alternative_columns]
                else:
                    input("No se pudieron encontrar columnas adecuadas. Presione Enter para continuar...")
                    return
            
            # Ejecutar el algoritmo K-means
            try:
                kmeans = Kmeans(filtered_dataset, num_centroids, max_iterations)
                self.centroid_centers, updated_dataset = kmeans.k_means_logic()
                self.current_results = updated_dataset
                
                # Visualizar los resultados
                self.visualize_clusters(updated_dataset, self.centroid_centers)
                
                # Guardar automáticamente en la base de datos
                self.save_results_to_db(title, num_centroids, max_iterations)
                
            except KmeansError as e:
                print(f"Error en el algoritmo K-means: {str(e)}")
                input("Presione Enter para continuar...")
                
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            input("Presione Enter para continuar...")
    
    def process_file_path(self, file_path):
        """Procesa la ruta del archivo CSV y devuelve un DataFrame."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"El archivo {file_path} no existe.")
        
        return pd.read_csv(path)
    
    def suggest_alternative_columns(self, dataset):
        """Sugiere columnas alternativas del dataset."""
        numeric_columns = dataset.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) < 3:
            print("No hay suficientes columnas numéricas para realizar el clustering.")
            return None
        
        print("\nColumnas numéricas disponibles:")
        for i, col in enumerate(numeric_columns):
            print(f"{i+1}. {col}")
        
        try:
            selected_columns = []
            print("\nSeleccione 3 columnas para el análisis (ingrese los números separados por comas):")
            selections = input().split(',')
            
            for sel in selections:
                idx = int(sel.strip()) - 1
                if 0 <= idx < len(numeric_columns):
                    selected_columns.append(numeric_columns[idx])
            
            if len(selected_columns) != 3:
                print("Debe seleccionar exactamente 3 columnas.")
                return None
            
            return selected_columns
            
        except ValueError:
            print("Entrada inválida.")
            return None
    
    def visualize_clusters(self, dataset, centroid_centers):
        """Visualiza los clusters en gráficos 3D y 2D."""
        # Convertir lista de listas a array NumPy si es necesario
        if isinstance(centroid_centers, list):
            centroid_centers_np = np.array(centroid_centers)
        else:
            centroid_centers_np = centroid_centers
        
        # Obtener nombres de las columnas
        feature_names = dataset.columns.tolist()
        feature_names.remove("assigned_cluster")
        
        # Gráfico 3D
        figure_3d = plt.figure(figsize=(10, 8))
        axis_3d = figure_3d.add_subplot(111, projection="3d")
        
        scatter = axis_3d.scatter(
            dataset[feature_names[0]],
            dataset[feature_names[1]],
            dataset[feature_names[2]],
            c=dataset["assigned_cluster"],
            cmap="viridis",
            s=100,
        )
        
        axis_3d.scatter(
            centroid_centers_np[:, 0],
            centroid_centers_np[:, 1],
            centroid_centers_np[:, 2],
            c="blue",
            marker="X",
            s=250,
            linewidths=2,
            edgecolors="black",
        )
        
        axis_3d.set_xlabel(feature_names[0])
        axis_3d.set_ylabel(feature_names[1])
        axis_3d.set_zlabel(feature_names[2])
        plt.title("Gráfico 3D de Clusters")
        plt.colorbar(scatter, label="Cluster")
        plt.show()
        
        # Gráficos 2D
        feature_pairs = [
            (feature_names[0], feature_names[1]),
            (feature_names[0], feature_names[2]),
            (feature_names[1], feature_names[2]),
        ]
        
        figure_2d, axis_2d_array = plt.subplots(1, 3, figsize=(18, 5))
        
        for axis_2d, (feature_x, feature_y) in zip(axis_2d_array, feature_pairs):
            sc = axis_2d.scatter(
                dataset[feature_x],
                dataset[feature_y],
                c=dataset["assigned_cluster"],
                cmap="viridis",
                s=100,
            )
            
            axis_2d.scatter(
                centroid_centers_np[:, feature_names.index(feature_x)],
                centroid_centers_np[:, feature_names.index(feature_y)],
                c="blue",
                marker="X",
                s=250,
                linewidths=2,
                edgecolors="black",
            )
            
            axis_2d.set_xlabel(feature_x)
            axis_2d.set_ylabel(feature_y)
            axis_2d.grid(True)
        
        plt.suptitle("Gráficos 2D: Comparación de Características y Clusters")
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
    
    def save_results_to_db(self, title, n_clusters, used_iterations):
        """Guarda automáticamente los resultados del clustering en la base de datos."""
        print("Guardando...")
        if self.current_results is None or self.centroid_centers is None:
            print("No hay resultados para guardar.")
            return
        
        try:
            # Guardar cada punto de datos
            for idx, row in self.current_results.iterrows():
                coordinates = row.drop("assigned_cluster").values.tolist()
                cluster_result = ClusteringResult(
                    title=title,
                    n_clusters=n_clusters,
                    used_iterations=used_iterations,
                    coordinates=coordinates,
                    assigned_cluster=int(row["assigned_cluster"]),
                    is_centroid=False,
                    centroid_label=None
                )
                self.results_controller.insert_result(cluster_result)
            
            # Guardar los centroides
            for i, centroid in enumerate(self.centroid_centers):
                centroid_result = ClusteringResult(
                    title=title,
                    n_clusters=n_clusters,
                    used_iterations=used_iterations,
                    coordinates=centroid,
                    assigned_cluster=i,
                    is_centroid=True,
                    centroid_label=f"Centroide {i+1}"
                )
                self.results_controller.insert_result(centroid_result)
            
            print(f"\nAnálisis '{title}' guardado exitosamente en la base de datos.")
            
        except Exception as e:
            print(f"Error al guardar los resultados: {str(e)}")
        
        input("Presione Enter para continuar...")
    
    def view_saved_results(self):
        """Muestra los resultados guardados y permite seleccionar uno para ver detalles."""
        self.clear_screen()
        print("\n===== RESULTADOS GUARDADOS =====")
        
        try:
            results = self.results_controller.list_all_titles()
            
            if not results:
                print("No hay resultados guardados.")
                input("Presione Enter para continuar...")
                return
            
            # Mostrar listado numerado de títulos
            print("\nSeleccione un resultado para ver detalles:")
            for i, result in enumerate(results):
                print(f"{i+1}. {result['title']}")
            
            # Opción para volver al menú principal
            print(f"{len(results)+1}. Volver al menú principal")
            
            try:
                selection = int(input("\nIngrese el número del resultado: "))
                
                if selection == len(results) + 1:
                    return  # Volver al menú principal
                
                if 1 <= selection <= len(results):
                    selected_id = results[selection-1]['id']
                    self.display_result_details(selected_id)
                else:
                    print("Selección inválida.")
                    input("Presione Enter para continuar...")
            
            except ValueError:
                print("Entrada inválida.")
                input("Presione Enter para continuar...")
                
        except Exception as e:
            print(f"Error al mostrar resultados: {str(e)}")
            input("Presione Enter para continuar...")
    
    def display_result_details(self, result_id):
        """Muestra los detalles de un resultado específico."""
        self.clear_screen()
        print("\n===== DETALLES DEL RESULTADO =====")
        
        try:
            # Obtener información del resultado seleccionado
            points = self.results_controller.get_points_by_title_id(result_id)
            centroids = self.results_controller.get_centroids_by_title_id(result_id)
            
            if not points or not centroids:
                print("No se encontraron datos para este resultado.")
                input("Presione Enter para continuar...")
                return
            
            # Mostrar información general
            title = points[0].title if points else "Desconocido"
            n_clusters = points[0].n_clusters if points else 0
            used_iterations = points[0].used_iterations if points else 0
            
            print(f"Título: {title}")
            print(f"Número de clusters: {n_clusters}")
            print(f"Iteraciones utilizadas: {used_iterations}")
            print(f"Puntos totales: {len(points)}")
            print(f"Centroides: {len(centroids)}")
            
            # Menú de opciones para este resultado
            print("\nOpciones:")
            print("1. Visualizar clusters")
            print("2. Ver datos de puntos")
            print("3. Ver datos de centroides")
            print("4. Volver al listado")
            
            option = input("\nSeleccione una opción (1-4): ")
            
            if option == "1":
                self.visualize_saved_result(points, centroids)
            elif option == "2":
                self.display_points_data(points)
            elif option == "3":
                self.display_centroids_data(centroids)
            elif option == "4":
                self.view_saved_results()
            else:
                print("Opción inválida.")
                input("Presione Enter para continuar...")
                self.display_result_details(result_id)
                
        except Exception as e:
            print(f"Error al mostrar detalles: {str(e)}")
            input("Presione Enter para continuar...")
            self.view_saved_results()
    
    def visualize_saved_result(self, points, centroids):
        """Visualiza un resultado guardado."""
        try:
            # Preparar datos para visualización
            # Crear DataFrame con puntos
            data = []
            feature_names = []
            
            # Determinar nombres de características basados en la longitud de coordenadas
            coord_length = len(points[0].coordinates)
            for i in range(coord_length):
                feature_names.append(f"Feature_{i+1}")
                
            # Agregar puntos al DataFrame
            for point in points:
                row = {}
                for i, coord in enumerate(point.coordinates):
                    row[feature_names[i]] = coord
                row["assigned_cluster"] = point.assigned_cluster
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # Preparar centroides
            centroid_coords = []
            for centroid in centroids:
                centroid_coords.append(centroid.coordinates)
            
            centroid_centers_np = np.array(centroid_coords)
            
            # Visualizar usando la función existente
            self.visualize_clusters(df, centroid_centers_np)
            
        except Exception as e:
            print(f"Error al visualizar: {str(e)}")
            input("Presione Enter para continuar...")
        
        self.view_saved_results()
    
    def display_points_data(self, points):
        """Muestra los datos de los puntos del resultado."""
        self.clear_screen()
        print("\n===== DATOS DE PUNTOS =====")
        
        # Determinar cuántos puntos mostrar por página
        points_per_page = 10
        total_pages = (len(points) + points_per_page - 1) // points_per_page
        current_page = 1
        
        while True:
            self.clear_screen()
            print(f"\n===== DATOS DE PUNTOS (Página {current_page}/{total_pages}) =====")
            
            start_idx = (current_page - 1) * points_per_page
            end_idx = min(start_idx + points_per_page, len(points))
            
            for i in range(start_idx, end_idx):
                point = points[i]
                print(f"\nPunto {i+1}:")
                print(f"Coordenadas: {point.coordinates}")
                print(f"Cluster asignado: {point.assigned_cluster}")
            
            print("\nOpciones:")
            if current_page > 1:
                print("A. Página anterior")
            if current_page < total_pages:
                print("S. Página siguiente")
            print("V. Volver")
            
            option = input("\nSeleccione una opción: ").upper()
            
            if option == "A" and current_page > 1:
                current_page -= 1
            elif option == "S" and current_page < total_pages:
                current_page += 1
            elif option == "V":
                break
            else:
                input("Opción inválida. Presione Enter para continuar...")
        
        self.view_saved_results()
    
    def display_centroids_data(self, centroids):
        """Muestra los datos de los centroides del resultado."""
        self.clear_screen()
        print("\n===== DATOS DE CENTROIDES =====")
        
        for i, centroid in enumerate(centroids):
            print(f"\nCentroide {i+1}:")
            print(f"Etiqueta: {centroid.centroid_label}")
            print(f"Coordenadas: {centroid.coordinates}")
            print(f"ID del cluster: {centroid.assigned_cluster}")
        
        input("\nPresione Enter para volver...")
        self.view_saved_results()
    
    def modify_results_menu(self):
        """Menú para seleccionar y modificar un resultado existente."""
        self.clear_screen()
        print("\n===== MODIFICAR RESULTADOS =====")
        
        # Listar resultados disponibles para modificar
        try:
            results = self.results_controller.list_all_titles()
            
            if not results:
                print("No hay resultados disponibles para modificar.")
                input("Presione Enter para continuar...")
                return
            
            # Mostrar listado numerado de títulos
            print("\nSeleccione el resultado que desea modificar:")
            for i, result in enumerate(results):
                print(f"{i+1}. {result['title']}")
            
            # Opción para volver al menú principal
            print(f"{len(results)+1}. Volver al menú principal")
            
            try:
                selection = int(input("\nIngrese el número del resultado: "))
                
                if selection == len(results) + 1:
                    return  # Volver al menú principal
                
                if 1 <= selection <= len(results):
                    selected_id = results[selection-1]['id']
                    self.modify_result(selected_id)
                else:
                    print("Selección inválida.")
                    input("Presione Enter para continuar...")
            
            except ValueError:
                print("Entrada inválida.")
                input("Presione Enter para continuar...")
            
        except Exception as e:
            print(f"Error al listar resultados: {str(e)}")
            input("Presione Enter para continuar...")
    
    def modify_result(self, result_id):
        """Modifica un resultado específico."""
        self.clear_screen()
        print("\n===== MODIFICAR RESULTADO =====")
        
        try:
            # Verificar si existe el resultado
            existing_result = self.results_controller.get_result_by_id(result_id)
            if not existing_result:
                print(f"No se encontró el resultado seleccionado.")
                input("Presione Enter para continuar...")
                return
            
            print(f"\nResultado actual: {existing_result.title}")
            
            # Solicitar nuevos valores manteniendo los actuales como default
            print("\nIngrese los nuevos valores (deje en blanco para mantener los actuales):")
            
            title = input(f"Título [{existing_result.title}]: ")
            title = title if title else existing_result.title
            
            n_clusters_input = input(f"Número de clusters [{existing_result.n_clusters}]: ")
            n_clusters = int(n_clusters_input) if n_clusters_input else existing_result.n_clusters
            
            used_iterations_input = input(f"Número de iteraciones utilizadas [{existing_result.used_iterations}]: ")
            used_iterations = int(used_iterations_input) if used_iterations_input else existing_result.used_iterations
            
            coordinates_current = ", ".join(map(str, existing_result.coordinates))
            coordinates_input = input(f"Coordenadas [{coordinates_current}]: ")
            coordinates = [float(x.strip()) for x in coordinates_input.split(',')] if coordinates_input else existing_result.coordinates
            
            assigned_cluster_input = input(f"Cluster asignado [{existing_result.assigned_cluster}]: ")
            assigned_cluster = int(assigned_cluster_input) if assigned_cluster_input else existing_result.assigned_cluster
            
            is_centroid_input = input(f"¿Es un centroide? (s/n) [{'s' if existing_result.is_centroid else 'n'}]: ").lower()
            is_centroid = is_centroid_input == 's' if is_centroid_input else existing_result.is_centroid
            
            centroid_label = existing_result.centroid_label
            if is_centroid:
                centroid_label_input = input(f"Etiqueta del centroide [{centroid_label or ''}]: ")
                centroid_label = centroid_label_input if centroid_label_input else centroid_label
            
            # Crear el objeto actualizado
            updated_result = ClusteringResult(
                title=title,
                n_clusters=n_clusters,
                used_iterations=used_iterations,
                coordinates=coordinates,
                assigned_cluster=assigned_cluster,
                is_centroid=is_centroid,
                centroid_label=centroid_label,
                id=result_id
            )
            
            # Actualizar en la base de datos
            success = self.results_controller.update_result(result_id, updated_result)
            if success:
                print(f"Resultado actualizado exitosamente.")
            else:
                print(f"No se pudo actualizar el resultado.")
            
        except ValueError as e:
            print(f"Error de formato: {str(e)}")
        except Exception as e:
            print(f"Error al modificar resultado: {str(e)}")
        
        input("Presione Enter para continuar...")
    
    def delete_results_menu(self):
        """Menú para seleccionar y eliminar un resultado."""
        self.clear_screen()
        print("\n===== ELIMINAR RESULTADOS =====")
        
        # Listar resultados disponibles para eliminar
        try:
            results = self.results_controller.list_all_titles()
            
            if not results:
                print("No hay resultados disponibles para eliminar.")
                input("Presione Enter para continuar...")
                return
            
            # Mostrar listado numerado de títulos
            print("\nSeleccione el resultado que desea eliminar:")
            for i, result in enumerate(results):
                print(f"{i+1}. {result['title']}")
            
            # Opción para volver al menú principal
            print(f"{len(results)+1}. Volver al menú principal")
            
            try:
                selection = int(input("\nIngrese el número del resultado: "))
                
                if selection == len(results) + 1:
                    return  # Volver al menú principal
                
                if 1 <= selection <= len(results):
                    selected_id = results[selection-1]['id']
                    selected_title = results[selection-1]['title']
                    
                    # Confirmar eliminación
                    confirm = input(f"¿Está seguro que desea eliminar '{selected_title}'? (s/n): ").lower()
                    if confirm == 's':
                        success = self.results_controller.delete_result(selected_id)
                        if success:
                            print(f"Resultado eliminado exitosamente.")
                        else:
                            print(f"No se pudo eliminar el resultado.")
                    else:
                        print("Operación cancelada.")
                else:
                    print("Selección inválida.")
            
            except ValueError:
                print("Entrada inválida.")
            
            input("Presione Enter para continuar...")
            
        except Exception as e:
            print(f"Error al listar resultados: {str(e)}")
            input("Presione Enter para continuar...")
    
    def exit_program(self):
        """Sale del programa."""
        print("\n¡Gracias por usar el Sistema de Clustering K-means!")
        sys.exit(0)


if __name__ == "__main__":
    ui = ConsoleUI()
    ui.display_menu()