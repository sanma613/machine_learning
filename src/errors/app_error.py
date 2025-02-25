class KmeansErrors(Exception):
    pass


class EmptyDatasetError(KmeansErrors):
    """
    El Dataset no puede ser un conjunto de datos vacio
    """


class ZeroCentroidsError(KmeansErrors):
    """
    El numero de centroides no puede ser cero
    """


class MoreCentroidsError(KmeansErrors):
    """
    El numero de centroides no puede ser mayor a el numero de datos
    """
