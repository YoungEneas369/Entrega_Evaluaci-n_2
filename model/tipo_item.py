class TipoItem:
    def __init__(self, id_tipo: int, nombre_categoria: str):
        self.id_tipo = id_tipo
        self.nombre_categoria = nombre_categoria

    @property
    def nombre_categoria(self):
        return self._nombre_categoria

    @nombre_categoria.setter
    def nombre_categoria(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        self._nombre_categoria = valor
