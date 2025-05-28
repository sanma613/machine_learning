import psycopg2 as pg
from typing import Optional, List, Dict
import sys
from contextlib import contextmanager

sys.path.append(".")
sys.path.append("src")
sys.path.append('model')
import SecretConfig
from src.model.result_model import ClusteringResult

class ResultsController:
    def __init__(self):
        """Inicializa la conexión a la base de datos utilizando la URL de conexión de SecretConfig."""
        self.db_host = SecretConfig.PGHOST
        self.db_database = SecretConfig.PGDATABASE
        self.db_user = SecretConfig.PGUSER
        self.db_password = SecretConfig.PGPASSWORD
        self.db_port = SecretConfig.PGPORT

    @contextmanager
    def _connect(self):
        """Método privado para gestionar la conexión a la base de datos de forma segura."""
        connection = None
        try:
            connection = pg.connect(
                database=self.db_database,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            yield connection
        except pg.Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    def create_table(self):
        """Crea la tabla 'clustering_results' si no existe."""
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                with open("sql/create_results_table.sql", "r") as file:
                    cursor.execute(file.read())
                connection.commit()
                cursor.close()
        except pg.Error as e:
            print(f"Error al crear la tabla: {e}")
            raise

    def delete_table(self):
        """Elimina la tabla 'clustering_results' si existe."""
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                with open("sql/delete_results_table.sql", "r") as file:
                    cursor.execute(file.read())
                connection.commit()
                cursor.close()
        except pg.Error as e:
            print(f"Error al eliminar la tabla: {e}")
            raise

    def create_result(self, clustering_result: ClusteringResult) -> bool:
        """Crea un nuevo resultado en la tabla 'clustering_results' y retorna True si tiene éxito."""
        if not isinstance(clustering_result, ClusteringResult):
            raise TypeError("El parámetro debe ser una instancia de ClusteringResult")

        try:
            inserted_id = self.insert_result(clustering_result)
            return inserted_id is not None
        except pg.Error as e:
            print(f"Error al crear el resultado: {e}")
            raise

    def insert_result(self, clustering_result: ClusteringResult) -> int:
        """Inserta un nuevo resultado en la tabla 'clustering_results' y retorna el ID generado."""
        if not isinstance(clustering_result, ClusteringResult):
            raise TypeError("El parámetro debe ser una instancia de ClusteringResult")
            
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                result = clustering_result.to_dict()

                query = """
                INSERT INTO clustering_results (
                    title,
                    n_clusters,
                    used_iterations,
                    coordinates,
                    assigned_cluster,
                    is_centroid,
                    centroid_label
                ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                """

                cursor.execute(query, (
                    result["title"],
                    result["n_clusters"],
                    result["used_iterations"],
                    result["coordinates"],
                    result["assigned_cluster"],
                    result["is_centroid"],
                    result["centroid_label"]
                ))

                # Obtener el ID generado
                inserted_id = cursor.fetchone()[0]
                connection.commit()
                cursor.close()
                
                return inserted_id
        except pg.Error as e:
            print(f"Error al insertar resultado: {e}")
            raise

    def get_result_by_id(self, result_id: int) -> Optional[ClusteringResult]:
        """Obtiene un resultado específico por su ID."""
        if not isinstance(result_id, int) or result_id <= 0:
            raise ValueError("El ID debe ser un número entero positivo")
            
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                query = """
                SELECT id, title, n_clusters, used_iterations, coordinates,
                       assigned_cluster, is_centroid, centroid_label
                FROM clustering_results
                WHERE id = %s
                """
                cursor.execute(query, (result_id,))
                row = cursor.fetchone()
                cursor.close()

                if row:
                    return ClusteringResult(
                        id=row[0],
                        title=row[1],
                        n_clusters=row[2],
                        used_iterations=row[3],
                        coordinates=row[4],
                        assigned_cluster=row[5],
                        is_centroid=row[6],
                        centroid_label=row[7]
                    )
                return None
        except pg.Error as e:
            print(f"Error al obtener resultado por ID: {e}")
            raise

    def update_result(self, result_id: int, clustering_result: ClusteringResult):
        """Actualiza un resultado existente en la tabla."""
        if not isinstance(result_id, int) or result_id <= 0:
            raise ValueError("El ID debe ser un número entero positivo")
        if not isinstance(clustering_result, ClusteringResult):
            raise TypeError("El parámetro debe ser una instancia de ClusteringResult")
            
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                
                # Verificar si el resultado existe
                cursor.execute("SELECT id FROM clustering_results WHERE id = %s", (result_id,))
                if cursor.fetchone() is None:
                    raise ValueError(f"No existe un resultado con el ID {result_id}")
                
                new_data = clustering_result.to_dict()
                query = """
                UPDATE clustering_results SET
                    title = %s,
                    n_clusters = %s,
                    used_iterations = %s,
                    coordinates = %s,
                    assigned_cluster = %s,
                    is_centroid = %s,
                    centroid_label = %s
                WHERE id = %s
                """

                cursor.execute(query, (
                    new_data["title"],
                    new_data["n_clusters"],
                    new_data["used_iterations"],
                    new_data["coordinates"],
                    new_data["assigned_cluster"],
                    new_data["is_centroid"],
                    new_data["centroid_label"],
                    result_id
                ))
                
                connection.commit()
                cursor.close()
                return cursor.rowcount > 0
        except pg.Error as e:
            print(f"Error al actualizar resultado: {e}")
            raise

    def delete_result(self, result_id: int) -> bool:
        """Elimina un resultado de la tabla por su ID."""
        if not isinstance(result_id, int) or result_id <= 0:
            raise ValueError("El ID debe ser un número entero positivo")
            
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM clustering_results WHERE id = %s", (result_id,))
                deleted = cursor.rowcount > 0
                connection.commit()
                cursor.close()
                return deleted
        except pg.Error as e:
            print(f"Error al eliminar resultado: {e}")
            raise

    def list_all_titles(self) -> List[Dict]:
        """Devuelve una lista de todos los resultados con sus IDs y títulos."""
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT id, title FROM clustering_results ORDER BY id")
                rows = cursor.fetchall()
                cursor.close()
                return [{"id": row[0], "title": row[1]} for row in rows]
        except pg.Error as e:
            print(f"Error al listar títulos: {e}")
            raise

    def obtener_cursor(self):
        """Crea la conexión a la base de datos y retorna un cursor para hacer consultas."""
        try:
            connection = pg.connect(
                database=self.db_database,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            cursor = connection.cursor()
            return cursor, connection
        except pg.Error as e:
            print(f"Error al obtener el cursor: {e}")
            raise