from model.tipo_item import TipoItem

class DetalleReserva:

    def __init__(
        self,
        tipo_item: TipoItem,
        descripcion: str,
        cantidad: int,
        precio_unitario: float
    ):
        self.tipo_item = tipo_item
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    @property
    def tipo_item(self):
        return self._tipo_item

    @tipo_item.setter
    def tipo_item(self, valor):
        if not isinstance(valor, TipoItem):
            raise ValueError("El tipo debe ser una instancia de TipoItem.")
        self._tipo_item = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        valor = int(valor)
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self._cantidad = valor

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor):
        valor = float(valor)
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio_unitario = valor

    def subtotal(self):
        return self.cantidad * self.precio_unitario