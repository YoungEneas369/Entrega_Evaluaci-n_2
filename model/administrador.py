from model.trabajador import Trabajador

class Administrador(Trabajador):

     def __init__(self, nombre, rut, usuario, password_hash):
          super().__init__(nombre, rut, usuario, password_hash)

     def puede_atender_clientes(self):
          return False