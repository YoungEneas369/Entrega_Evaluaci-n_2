from model.paquete import Paquete


class PaqueteCrucero(Paquete):

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

        if tipo_cambio <= 0:
            raise ValueError(
                "El tipo de cambio debe ser mayor que cero."
            )

        return round(
            self.precio_base
            * tipo_cambio
            * 1.12
        ) 