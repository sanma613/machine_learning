class KmeansError(Exception):
    pass


class EmptyDatasetError(KmeansError):
    def __init__(self):
        message = (
            "El dataset está vacío: "
            "Se intentó ejecutar el algoritmo con un dataset sin registros. "
            "Verifica que el dataset contenga datos antes de iniciar el proceso."
        )
        super().__init__(message)


class ZeroCentroidsError(KmeansError):
    def __init__(self):
        message = (
            "El numero de centroides es 0: "
            "Se ingresó 0 como número de centroides. "
            "Ingresa un número mayor que 0 para continuar."
        )
        super().__init__(message)


class MoreCentroidsError(KmeansError):
    def __init__(self, num_centroids: int, num_data: int):
        message = (
            f"El número de centroides es inválido: "
            f"Se ingresó {num_centroids} centroides para {num_data} datos. "
            "Asegúrate de que el número de centroides sea menor o igual al número de registros del dataset."
        )
        super().__init__(message)


class NoNumericColumnsError(KmeansError):
    def __init__(self, invalid_columns: list[str]):
        message = (
            "Se encontraron columnas con datos no numéricos. "
            f"Las siguientes columnas contienen datos no numéricos: {invalid_columns}. "
            "Revisa y transforma los datos de las columnas indicadas a formato numérico, o elimínalas."
        )
        super().__init__(message)
