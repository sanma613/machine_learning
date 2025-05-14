import unittest
import sys
sys.path.append("src")

from controller.results_controller import ResultsController
from model.result_model import ClusteringResult

class TestResultsController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Test Fixture: Se ejecuta al inicio de las pruebas para crear la tabla """
        cls.controller = ResultsController()
        cls.controller.delete_table()  # Elimina la tabla antes de empezar
        cls.controller.create_table()  # Crea la tabla antes de empezar
        print("Test Fixture: Tabla creada exitosamente")

    @classmethod
    def tearDownClass(cls):
        """ Se ejecuta al finalizar todas las pruebas """
        # Opcional: Limpiar la tabla al finalizar
        cls.controller.delete_table()
        print("Test Fixture: Tabla eliminada al finalizar")

    # =============================================
    # 3 CASOS DE PRUEBA PARA INSERTAR
    # =============================================
    
    def test_insert_1(self):
        """ Caso de prueba 1: Insertar un resultado con centroide """
        result = ClusteringResult(
            title="Inserción Test 1",
            n_clusters=3,
            used_iterations=10,
            coordinates=[0.1, 0.2, 0.3],
            assigned_cluster=1,
            is_centroid=True,
            centroid_label="A"
        )

        # Insertar en la base de datos
        inserted_id = self.controller.insert_result(result)
        
        # Verificar que se haya asignado un ID
        self.assertIsNotNone(inserted_id)
        self.assertGreater(inserted_id, 0)
        
        # Buscar el resultado insertado para verificar
        result_inserted = self.controller.get_result_by_id(inserted_id)
        
        # Verificar que los datos sean iguales
        self.assertEqual(result_inserted.title, "Inserción Test 1")
        self.assertEqual(result_inserted.n_clusters, 3)
        self.assertEqual(result_inserted.used_iterations, 10)
        self.assertEqual(result_inserted.coordinates, [0.1, 0.2, 0.3])
        self.assertEqual(result_inserted.assigned_cluster, 1)
        self.assertTrue(result_inserted.is_centroid)
        self.assertEqual(result_inserted.centroid_label, "A")
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id)

    def test_insert_2(self):
        """ Caso de prueba 2: Insertar un resultado sin centroide """
        result = ClusteringResult(
            title="Inserción Test 2",
            n_clusters=5,
            used_iterations=7,
            coordinates=[0.4, 0.5, 0.6],
            assigned_cluster=2,
            is_centroid=False,
            centroid_label=None
        )

        # Insertar en la base de datos
        inserted_id = self.controller.insert_result(result)
        
        # Verificar que se haya asignado un ID
        self.assertIsNotNone(inserted_id)
        self.assertGreater(inserted_id, 0)
        
        # Buscar el resultado insertado para verificar
        result_inserted = self.controller.get_result_by_id(inserted_id)
        
        # Verificar que los datos sean iguales
        self.assertEqual(result_inserted.title, "Inserción Test 2")
        self.assertEqual(result_inserted.n_clusters, 5)
        self.assertEqual(result_inserted.used_iterations, 7)
        self.assertEqual(result_inserted.coordinates, [0.4, 0.5, 0.6])
        self.assertEqual(result_inserted.assigned_cluster, 2)
        self.assertFalse(result_inserted.is_centroid)
        self.assertIsNone(result_inserted.centroid_label)
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id)

    def test_insert_3(self):
        """ Caso de prueba 3: Insertar un resultado con coordenadas más largas """
        result = ClusteringResult(
            title="Inserción Test 3",
            n_clusters=8,
            used_iterations=15,
            coordinates=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
            assigned_cluster=0,
            is_centroid=True,
            centroid_label="X"
        )

        # Insertar en la base de datos
        inserted_id = self.controller.insert_result(result)
        
        # Verificar que se haya asignado un ID
        self.assertIsNotNone(inserted_id)
        self.assertGreater(inserted_id, 0)
        
        # Buscar el resultado insertado para verificar
        result_inserted = self.controller.get_result_by_id(inserted_id)
        
        # Verificar que los datos sean iguales
        self.assertEqual(result_inserted.title, "Inserción Test 3")
        self.assertEqual(result_inserted.n_clusters, 8)
        self.assertEqual(result_inserted.used_iterations, 15)
        self.assertEqual(result_inserted.coordinates, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
        self.assertEqual(result_inserted.assigned_cluster, 0)
        self.assertTrue(result_inserted.is_centroid)
        self.assertEqual(result_inserted.centroid_label, "X")
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id)

    # =============================================
    # 3 CASOS DE PRUEBA PARA MODIFICAR
    # =============================================
    
    def test_update_1(self):
        """ Caso de prueba 1: Modificar un resultado (título y coordenadas) """
        # Crear un resultado para posteriormente modificarlo
        result = ClusteringResult(
            title="Resultado a Modificar 1",
            n_clusters=3,
            used_iterations=5,
            coordinates=[0.1, 0.2, 0.3],
            assigned_cluster=1,
            is_centroid=False,
            centroid_label=None
        )
        
        # Insertar el resultado para obtener un ID
        inserted_id = self.controller.insert_result(result)
        
        # Crear el objeto con datos modificados
        modified_result = ClusteringResult(
            title="Resultado Modificado 1",  # Título modificado
            n_clusters=3,  # Igual
            used_iterations=5,  # Igual
            coordinates=[0.5, 0.6, 0.7],  # Coordenadas modificadas
            assigned_cluster=1,  # Igual
            is_centroid=False,  # Igual
            centroid_label=None  # Igual
        )
        
        # Actualizar el resultado en la base de datos
        self.controller.update_result(inserted_id, modified_result)
        
        # Obtener el resultado actualizado
        updated_result = self.controller.get_result_by_id(inserted_id)
        
        # Verificar que se hayan aplicado las modificaciones
        self.assertEqual(updated_result.title, "Resultado Modificado 1")
        self.assertEqual(updated_result.coordinates, [0.5, 0.6, 0.7])
        
        # Los demás campos deben permanecer igual
        self.assertEqual(updated_result.n_clusters, 3)
        self.assertEqual(updated_result.used_iterations, 5)
        self.assertEqual(updated_result.assigned_cluster, 1)
        self.assertFalse(updated_result.is_centroid)
        self.assertIsNone(updated_result.centroid_label)
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id)

    def test_update_2(self):
        """ Caso de prueba 2: Modificar un resultado (convertir a centroide) """
        # Crear un resultado para posteriormente modificarlo
        result = ClusteringResult(
            title="Resultado a Modificar 2",
            n_clusters=4,
            used_iterations=8,
            coordinates=[0.2, 0.3, 0.4],
            assigned_cluster=2,
            is_centroid=False,
            centroid_label=None
        )
        
        # Insertar el resultado para obtener un ID
        inserted_id = self.controller.insert_result(result)
        
        # Crear el objeto con datos modificados
        modified_result = ClusteringResult(
            title="Resultado Modificado 2",  # Título modificado
            n_clusters=4,  # Igual
            used_iterations=8,  # Igual
            coordinates=[0.2, 0.3, 0.4],  # Igual
            assigned_cluster=2,  # Igual
            is_centroid=True,  # Modificado a centroide
            centroid_label="C"  # Añadido etiqueta de centroide
        )
        
        # Actualizar el resultado en la base de datos
        self.controller.update_result(inserted_id, modified_result)
        
        # Obtener el resultado actualizado
        updated_result = self.controller.get_result_by_id(inserted_id)
        
        # Verificar que se hayan aplicado las modificaciones
        self.assertEqual(updated_result.title, "Resultado Modificado 2")
        self.assertTrue(updated_result.is_centroid)
        self.assertEqual(updated_result.centroid_label, "C")
        
        # Los demás campos deben permanecer igual
        self.assertEqual(updated_result.n_clusters, 4)
        self.assertEqual(updated_result.used_iterations, 8)
        self.assertEqual(updated_result.coordinates, [0.2, 0.3, 0.4])
        self.assertEqual(updated_result.assigned_cluster, 2)
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id)

    def test_update_3(self):
        """ Caso de prueba 3: Modificar un resultado (cambiar todos los campos) """
        # Crear un resultado para posteriormente modificarlo
        result = ClusteringResult(
            title="Resultado a Modificar 3",
            n_clusters=2,
            used_iterations=6,
            coordinates=[0.3, 0.4, 0.5],
            assigned_cluster=0,
            is_centroid=True,
            centroid_label="Y"
        )
        
        # Insertar el resultado para obtener un ID
        inserted_id = self.controller.insert_result(result)
        
        # Crear el objeto con todos los datos modificados
        modified_result = ClusteringResult(
            title="Resultado Completamente Nuevo",  # Modificado
            n_clusters=6,  # Modificado
            used_iterations=12,  # Modificado
            coordinates=[0.8, 0.9, 1.0],  # Modificado
            assigned_cluster=3,  # Modificado
            is_centroid=False,  # Modificado
            centroid_label=None  # Modificado
        )
        
        # Actualizar el resultado en la base de datos
        self.controller.update_result(inserted_id, modified_result)
        
        # Obtener el resultado actualizado
        updated_result = self.controller.get_result_by_id(inserted_id)
        
        # Verificar que todos los campos se hayan modificado
        self.assertEqual(updated_result.title, "Resultado Completamente Nuevo")
        self.assertEqual(updated_result.n_clusters, 6)
        self.assertEqual(updated_result.used_iterations, 12)
        self.assertEqual(updated_result.coordinates, [0.8, 0.9, 1.0])
        self.assertEqual(updated_result.assigned_cluster, 3)
        self.assertFalse(updated_result.is_centroid)
        self.assertIsNone(updated_result.centroid_label)
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id)

    # =============================================
    # 3 CASOS DE PRUEBA PARA BUSCAR
    # =============================================
    
    def test_search_1(self):
        """ Caso de prueba 1: Buscar un resultado por ID """
        # Crear e insertar un resultado para luego buscarlo
        result = ClusteringResult(
            title="Resultado para Búsqueda 1",
            n_clusters=3,
            used_iterations=10,
            coordinates=[0.1, 0.2, 0.3],
            assigned_cluster=1,
            is_centroid=True,
            centroid_label="A"
        )
        
        # Insertar y obtener el ID
        inserted_id = self.controller.insert_result(result)
        
        # Buscar el resultado por su ID
        found_result = self.controller.get_result_by_id(inserted_id)
        
        # Verificar que se encontró el resultado correcto
        self.assertIsNotNone(found_result)
        self.assertEqual(found_result.title, "Resultado para Búsqueda 1")
        self.assertEqual(found_result.n_clusters, 3)
        self.assertEqual(found_result.used_iterations, 10)
        self.assertEqual(found_result.coordinates, [0.1, 0.2, 0.3])
        self.assertEqual(found_result.assigned_cluster, 1)
        self.assertTrue(found_result.is_centroid)
        self.assertEqual(found_result.centroid_label, "A")
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id)

    def test_search_2(self):
        """ Caso de prueba 2: Buscar un resultado no existente (debe devolver None) """
        # Buscar un ID que seguramente no existe (un número muy alto)
        non_existent_id = 99999
        found_result = self.controller.get_result_by_id(non_existent_id)
        
        # Verificar que el resultado es None (no encontrado)
        self.assertIsNone(found_result)

    def test_search_3(self):
        """ Caso de prueba 3: Insertar varios resultados y buscar uno específico """
        # Crear e insertar varios resultados
        result1 = ClusteringResult(
            title="Múltiple Búsqueda 1",
            n_clusters=2,
            used_iterations=5,
            coordinates=[0.1, 0.2, 0.3],
            assigned_cluster=0,
            is_centroid=False,
            centroid_label=None
        )
        
        result2 = ClusteringResult(
            title="Múltiple Búsqueda 2",
            n_clusters=3,
            used_iterations=7,
            coordinates=[0.4, 0.5, 0.6],
            assigned_cluster=1,
            is_centroid=True,
            centroid_label="B"
        )
        
        result3 = ClusteringResult(
            title="Múltiple Búsqueda 3",
            n_clusters=4,
            used_iterations=9,
            coordinates=[0.7, 0.8, 0.9],
            assigned_cluster=2,
            is_centroid=False,
            centroid_label=None
        )
        
        # Insertar los resultados y guardar sus IDs
        id1 = self.controller.insert_result(result1)
        id2 = self.controller.insert_result(result2)
        id3 = self.controller.insert_result(result3)
        
        # Buscar el segundo resultado específicamente
        found_result = self.controller.get_result_by_id(id2)
        
        # Verificar que se encontró el resultado correcto
        self.assertIsNotNone(found_result)
        self.assertEqual(found_result.title, "Múltiple Búsqueda 2")
        self.assertEqual(found_result.n_clusters, 3)
        self.assertEqual(found_result.used_iterations, 7)
        self.assertEqual(found_result.coordinates, [0.4, 0.5, 0.6])
        self.assertEqual(found_result.assigned_cluster, 1)
        self.assertTrue(found_result.is_centroid)
        self.assertEqual(found_result.centroid_label, "B")
        
        # Limpiar: eliminar todos los registros creados
        self.controller.delete_result(id1)
        self.controller.delete_result(id2)
        self.controller.delete_result(id3)

    # =============================================
    # 3 CASOS DE PRUEBA PARA ELIMINAR
    # =============================================
    
    def test_delete_1(self):
        """ Caso de prueba 1: Eliminar un resultado existente """
        # Crear e insertar un resultado para luego eliminarlo
        result = ClusteringResult(
            title="Resultado para Eliminar 1",
            n_clusters=3,
            used_iterations=10,
            coordinates=[0.1, 0.2, 0.3],
            assigned_cluster=1,
            is_centroid=False,
            centroid_label=None
        )
        
        # Insertar y obtener el ID
        inserted_id = self.controller.insert_result(result)
        
        # Confirmar que existe antes de eliminar
        before_delete = self.controller.get_result_by_id(inserted_id)
        self.assertIsNotNone(before_delete)
        
        # Eliminar el resultado
        deleted = self.controller.delete_result(inserted_id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(deleted)
        
        # Intentar buscar el resultado eliminado (debe ser None)
        after_delete = self.controller.get_result_by_id(inserted_id)
        self.assertIsNone(after_delete)

    def test_delete_2(self):
        """ Caso de prueba 2: Eliminar un resultado no existente """
        # Intentar eliminar un resultado con un ID que no existe
        non_existent_id = 99999
        deleted = self.controller.delete_result(non_existent_id)
        
        # Verificar que el método devuelve False (no eliminado)
        self.assertFalse(deleted)

    def test_delete_3(self):
        """ Caso de prueba 3: Insertar, eliminar y volver a insertar con el mismo título """
        # Crear e insertar un primer resultado
        result1 = ClusteringResult(
            title="Resultado para Reinserción",
            n_clusters=3,
            used_iterations=10,
            coordinates=[0.1, 0.2, 0.3],
            assigned_cluster=1,
            is_centroid=False,
            centroid_label=None
        )
        
        # Insertar y obtener el ID
        inserted_id1 = self.controller.insert_result(result1)
        
        # Eliminar el resultado
        deleted = self.controller.delete_result(inserted_id1)
        self.assertTrue(deleted)
        
        # Crear un nuevo resultado con el mismo título
        result2 = ClusteringResult(
            title="Resultado para Reinserción",  # Mismo título que el anterior
            n_clusters=5,  # Diferente
            used_iterations=15,  # Diferente
            coordinates=[0.4, 0.5, 0.6],  # Diferente
            assigned_cluster=2,  # Diferente
            is_centroid=True,  # Diferente
            centroid_label="R"  # Diferente
        )
        
        # Insertar el nuevo resultado
        inserted_id2 = self.controller.insert_result(result2)
        
        # Verificar que se insertó correctamente con un nuevo ID
        self.assertIsNotNone(inserted_id2)
        self.assertNotEqual(inserted_id1, inserted_id2)
        
        # Buscar el nuevo resultado
        found_result = self.controller.get_result_by_id(inserted_id2)
        
        # Verificar que es el nuevo resultado con el mismo título
        self.assertEqual(found_result.title, "Resultado para Reinserción")
        self.assertEqual(found_result.n_clusters, 5)
        self.assertEqual(found_result.coordinates, [0.4, 0.5, 0.6])
        
        # Limpiar: eliminar el registro creado
        self.controller.delete_result(inserted_id2)


if __name__ == '__main__':
    unittest.main()