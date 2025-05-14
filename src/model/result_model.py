from typing import List, Dict, Optional, Any, Union

class ClusteringResult:
    def __init__(
        self,
        title: str,
        n_clusters: int,
        used_iterations: int,
        coordinates: List[float],
        assigned_cluster: int,
        is_centroid: bool,
        centroid_label: Optional[str] = None,
        id: Optional[int] = None
    ):
        """
        Modelo para representar el resultado de un algoritmo de clustering.
        
        Args:
            title: Título descriptivo del resultado de clustering
            n_clusters: Número de clusters utilizados
            used_iterations: Número de iteraciones utilizadas
            coordinates: Coordenadas del punto en el espacio
            assigned_cluster: Cluster asignado al punto
            is_centroid: Indica si el punto es un centroide
            centroid_label: Etiqueta del centroide (solo si is_centroid es True)
            id: Identificador único en la base de datos (opcional)
        """
        self.id = id
        self.title = title
        self.n_clusters = n_clusters
        self.used_iterations = used_iterations
        self.coordinates = coordinates
        self.assigned_cluster = assigned_cluster
        self.is_centroid = is_centroid
        self.centroid_label = centroid_label
    
        
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a un diccionario para facilitar su serialización."""
        return {
            "id": self.id,
            "title": self.title,
            "n_clusters": self.n_clusters,
            "used_iterations": self.used_iterations,
            "coordinates": self.coordinates,
            "assigned_cluster": self.assigned_cluster,
            "is_centroid": self.is_centroid,
            "centroid_label": self.centroid_label
        }
    
    def isEqual(self, other: 'ClusteringResult') -> bool:
        """
        Compara si dos objetos ClusteringResult son iguales en sus atributos principales.
        No compara el ID porque puede ser asignado por la base de datos.
        """
        if not isinstance(other, ClusteringResult):
            return False
            
        return (
            self.title == other.title and
            self.n_clusters == other.n_clusters and
            self.used_iterations == other.used_iterations and
            self.coordinates == other.coordinates and
            self.assigned_cluster == other.assigned_cluster and
            self.is_centroid == other.is_centroid and
            self.centroid_label == other.centroid_label
        )
    
    def __str__(self) -> str:
        """Representación en cadena del objeto ClusteringResult."""
        return (f"ClusteringResult(id={self.id}, title='{self.title}', "
                f"n_clusters={self.n_clusters}, used_iterations={self.used_iterations}, "
                f"assigned_cluster={self.assigned_cluster}, is_centroid={self.is_centroid}, "
                f"centroid_label={self.centroid_label})")
    
    def __repr__(self) -> str:
        """Representación detallada del objeto ClusteringResult."""
        return str(self)