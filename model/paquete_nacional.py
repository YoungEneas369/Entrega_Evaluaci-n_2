from model.paquete import Paquete


class PaqueteNacional(Paquete):

    def __init__(
        self,
        id_paquete,
        nombre,
        precio_base,
        proveedor_id
    ):
        super().__init__(
            id_paquete,
            nombre,
            precio_base,
            proveedor_id
        )

    def calcular_precio_final(
        self,
        tipo_cambio=1.0
    ):

        return round(
            self.precio_base
        ) 