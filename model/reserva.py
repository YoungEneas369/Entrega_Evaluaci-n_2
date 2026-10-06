from enum import Enum
from model.excepciones import (
    AnticipoInsuficienteError,
    SinCuposError,
    ValidacionError
)
from model.paquete_internacional import PaqueteInternacional
from model.viajero import Viajero

class EstadoReserva(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PAGADA = "PAGADA"
    CANCELADA = "CANCELADA"

class Reserva:

    def __init__(
        self,
        cliente,
        agente,
        paquete,
        proveedor,
        fecha_viaje,
        precio_paquete_clp,
        anticipo=0.0,
        tipo_cambio=1.0,
        estado=EstadoReserva.PENDIENTE,
        viajero: Viajero = None
    ):
        self.cliente = cliente
        self.agente = agente
        self.paquete = paquete
        self.proveedor = proveedor
        self.fecha_viaje = fecha_viaje
        self.precio_paquete_clp = float(precio_paquete_clp)
        self.tipo_cambio = float(tipo_cambio)
        self.detalles = []
        self.anticipo = anticipo
        self.estado = estado
        self.viajero = viajero

    @property
    def anticipo(self):
        return self._anticipo

    @anticipo.setter
    def anticipo(self, valor):
        valor = float(valor)
        if valor < 0:
            raise ValueError("El anticipo no puede ser negativo.")
        self._anticipo = valor

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)

    def total(self):
        total_detalles = sum(
            detalle.subtotal()
            for detalle in self.detalles
        )
        return self.precio_paquete_clp + total_detalles

    def saldo_pendiente(self):
        return max(0.0, self.total() - self.anticipo)

    def cancelar(self):
        self.estado = EstadoReserva.CANCELADA

    def pagar_saldo(self, monto):
        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto a pagar debe ser mayor a cero.")
        
        nuevo_anticipo = self.anticipo + monto
        total_reserva = self.total()
        
        if nuevo_anticipo > total_reserva:
            raise ValueError("El monto ingresado excede el saldo pendiente.")
            
        self.anticipo = nuevo_anticipo
        if self.saldo_pendiente() == 0:
            self.estado = EstadoReserva.PAGADA

    def validar_confirmacion(self):
        if isinstance(self.paquete, PaqueteInternacional):
            if not self.viajero or not self.viajero.numero_pasaporte:
                raise ValidacionError("Un paquete internacional requiere un Viajero con pasaporte válido.")

        if not self.proveedor.tiene_cupos(self.fecha_viaje):
            raise SinCuposError("No se puede confirmar la reserva porque el proveedor no tiene cupos para esa fecha.")

        minimo_anticipo = self.total() * 0.50
        if self.anticipo < minimo_anticipo:
            raise AnticipoInsuficienteError("El anticipo debe ser al menos el 50% del total.")

        self.estado = EstadoReserva.CONFIRMADA
        return True
