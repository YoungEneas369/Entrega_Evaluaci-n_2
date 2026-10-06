import sys
from conectar import crear_conexion
from dao.paquete_dao import PaqueteDAO
from model.paquete_nacional import PaqueteNacional
from model.paquete_internacional import PaqueteInternacional
from model.paquete_crucero import PaqueteCrucero
from model.viajero import Viajero
from model.persona import Persona
from model.reserva import Reserva
from model.detalle_reserva import DetalleReserva
from servicios.mindicador import MiIndicador
from model.proveedor import Proveedor
from model.disponibilidad import Disponibilidad
from model.tipo_item import TipoItem
from model.cliente import Cliente
from model.agente_viajes import AgenteViajes

def menu():
    print("\n" + "="*45)
    print("   AGENCIA DE VIAJES RUTASUR")
    print("="*45)
    print("1. Crear Paquete")
    print("2. Listar Paquetes")
    print("3. Modificar Paquete")
    print("4. Eliminar Paquete")
    print("5. Validar Pasaporte Viajero")
    print("6. Calcular Precio con Dólar")
    print("7. Registrar Reserva")
    print("8. Ver detalle de reserva")
    print("9. Salir")
    print("="*45)
    return input("Seleccione una opción: ").strip()

def main():
    try:
        conexion = crear_conexion()
        paquete_dao = PaqueteDAO(conexion)
        paquete_dao.crear_tabla()
        
        from dao.reserva_dao import ReservaDAO
        reserva_dao = ReservaDAO(conexion)
        reserva_dao.crear_tabla()
        
        conexion.commit()
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        sys.exit(1)

    while True:
        opcion = menu()

        if opcion == '1':
            print("\n--- CREAR PAQUETE ---")
            nombre = input("Ingrese nombre del paquete: ").strip()
            if not nombre:
                print("Error: El nombre no puede estar vacío.")
                continue
                
            try:
                precio = float(input("Ingrese precio base: "))
                if precio <= 0:
                    print("Error: El precio debe ser mayor a cero.")
                    continue
                    
                tipo = input("Tipo ('nacional', 'internacional' o 'crucero'): ").strip().lower()
                
                if tipo == 'nacional':
                    p = PaqueteNacional(None, nombre, precio, None)
                elif tipo == 'internacional':
                    p = PaqueteInternacional(None, nombre, precio, None)
                elif tipo == 'crucero':
                    p = PaqueteCrucero(None, nombre, precio, None)
                else:
                    print("Error: Tipo inválido.")
                    continue
                    
                paquete_dao.insertar(p, tipo)
                print("Operación exitosa: Paquete guardado correctamente.")
            except ValueError:
                print("Error: El precio debe ser un número.")

        elif opcion == '2':
            print("\n--- LISTADO DE PAQUETES ---")
            paquetes = paquete_dao.listar()
            if paquetes:
                print(f"{'ID':<4} | {'NOMBRE':<20} | {'PRECIO BASE':<12} | {'TIPO'}")
                print("-" * 55)
                for p, t in paquetes:
                    print(f"{p.id_paquete:<4} | {p.nombre:<20} | ${p.precio_base:<11.2f} | {t}")
            else:
                print("No hay paquetes registrados.")

        elif opcion == '3':
            print("\n--- MODIFICAR PAQUETE ---")
            try:
                id_buscar = int(input("Ingrese ID del paquete: "))
                p = paquete_dao.buscar(id_buscar)
                if p:
                    print(f"Actual: {p.nombre} - ${p.precio_base}")
                    nuevo_precio = float(input("Ingrese nuevo precio base: "))
                    if nuevo_precio <= 0:
                        print("Error: El precio debe ser mayor a cero.")
                        continue
                        
                    p.precio_base = nuevo_precio
                    
                    if isinstance(p, PaqueteNacional):
                        tipo_actual = "nacional"
                    elif isinstance(p, PaqueteInternacional):
                        tipo_actual = "internacional"
                    else:
                        tipo_actual = "crucero"
                        
                    paquete_dao.actualizar(p, tipo_actual)
                    print("Operación exitosa: Paquete modificado.")
                else:
                    print("Error: Paquete no encontrado.")
            except ValueError:
                print("Error: ID o precio inválido (debe ser número).")

        elif opcion == '4':
            print("\n--- ELIMINAR PAQUETE ---")
            try:
                id_buscar = int(input("Ingrese ID del paquete a eliminar: "))
                eliminado = paquete_dao.eliminar(id_buscar)
                if eliminado:
                    print("Operación exitosa: Paquete eliminado.")
                else:
                    print("Error: Paquete no encontrado.")
            except ValueError:
                print("Error: ID inválido (debe ser número).")

        elif opcion == '5':
            print("\n--- VALIDAR PASAPORTE VIAJERO ---")
            pasaporte = input("Ingrese Pasaporte (Dato de prueba): ").strip()
            
            try:
                v = Viajero("11111111-1", "UsuarioPrueba", pasaporte)
                print(f"Operación exitosa: Pasaporte aceptado ({v.numero_pasaporte}).")
            except ValueError as e:
                print(f"Error de validación: {e}")

        elif opcion == '6':
            print("\n--- CALCULAR PRECIO CON DÓLAR ---")
            try:
                id_buscar = int(input("Ingrese ID del paquete: "))
                p = paquete_dao.buscar(id_buscar)
                if p:
                    servicio = MiIndicador()
                    dolar = servicio.obtener_dolar()
                    print(f"Valor dólar obtenido: ${dolar}")
                    
                    if isinstance(p, PaqueteNacional):
                        print(f"Cálculo: ${p.precio_base:,.2f} (No aplica dólar)")
                    elif isinstance(p, PaqueteInternacional):
                        print(f"Cálculo: ${p.precio_base:,.2f} * ${dolar}")
                    elif isinstance(p, PaqueteCrucero):
                        print(f"Cálculo: ${p.precio_base:,.2f} * ${dolar} * 1.12")
                        
                    precio_final = p.calcular_precio_final(dolar)
                    print(f"Precio final: ${precio_final:,.2f}")
                else:
                    print("Error: Paquete no encontrado.")
            except ValueError:
                print("Error: ID inválido (debe ser número).")
                
        elif opcion == '7':
            print("\n--- REGISTRAR RESERVA ---")
            try:
                cupos = int(input("Ingrese cupos actuales del proveedor en la fecha: "))
                prov = Proveedor(1, "Latam Airlines")
                prov.agregar_disponibilidad(Disponibilidad("2026-12-01", cupos))
                
                if not prov.tiene_cupos("2026-12-01"):
                    print("Operación denegada: El proveedor no tiene cupos disponibles.")
                    continue
                
                precio_total = float(input("Ingrese precio del paquete: "))
                if precio_total <= 0:
                    print("Error: El precio debe ser mayor a cero.")
                    continue
                
                cliente = Cliente("Juan", "11111111-1")
                agente = AgenteViajes("Pedro", "22222222-2", "pedrito", "123")
                
                reserva = Reserva(cliente, agente, None, prov, "2026-12-01", precio_total, 0)
                reserva.agregar_detalle(DetalleReserva(TipoItem(1, "Vuelo"), "Santiago-Miami", 1, 150000))
                reserva.agregar_detalle(DetalleReserva(TipoItem(2, "Hotel"), "Hotel Miami", 7, 50000))
                reserva.agregar_detalle(DetalleReserva(TipoItem(3, "Seguro de Viaje"), "Cobertura Total", 1, 30000))
                reserva.agregar_detalle(DetalleReserva(TipoItem(4, "Excursión"), "City Tour", 2, 25000))
                
                print("\nDesglose de la Reserva:")
                print(f"- Paquete: ${precio_total:,.0f}")
                suma_detalles = 0
                for d in reserva.detalles:
                    subtotal = d.cantidad * d.precio_unitario
                    suma_detalles += subtotal
                    print(f"- {d.cantidad}x {d.tipo_item.nombre_categoria} a ${d.precio_unitario:,.0f} = ${subtotal:,.0f}")
                
                total_real = reserva.total()
                print(f"Total a pagar (Paquete + Detalles): ${total_real:,.0f}")
                
                anticipo = float(input(f"Ingrese monto de anticipo (Mínimo requerido 50% = ${total_real * 0.5:,.0f}): "))
                reserva.anticipo = anticipo
                
                if reserva.validar_confirmacion():
                    prov.descontar_cupo("2026-12-01")
                    reserva_id = reserva_dao.insertar(reserva)
                    print("Operación exitosa: Reserva confirmada y guardada en BD.")
                    print(f"Saldo pendiente a pagar: ${total_real - anticipo:,.0f}")
                    print(f"ID Reserva: {reserva_id} (Use la Opción 8 para consultar el detalle)")
                else:
                    print("Operación denegada: El anticipo no alcanza el 50% requerido.")
            except ValueError:
                print("Error: Ingreso inválido. Deben ser números.")
            except Exception as e:
                print(f"Error al procesar reserva: {e}")

        elif opcion == '8':
            print("\n--- VER DETALLE DE RESERVA ---")
            try:
                id_reserva = int(input("Ingrese ID de la reserva a consultar: "))
                data = reserva_dao.buscar_detalles(id_reserva)
                if data:
                    r = data["reserva"]
                    paquete_principal = r[2]
                    anticipo = r[3]
                    
                    print(f"\nReserva ID: {r[0]} | Fecha: {r[1]} | Estado: {r[4]}")
                    print(f"Paquete principal: ${paquete_principal:,.0f} | Anticipo pagado: ${anticipo:,.0f}")
                    print("Líneas de detalle guardadas:")
                    
                    suma_detalles = 0
                    for d in data["detalles"]:
                        subtotal = d[2] * d[3]
                        suma_detalles += subtotal
                        print(f"-> {d[2]}x {d[1]} ({d[0]}) a ${d[3]:,.0f} = ${subtotal:,.0f}")
                        
                    total_real = paquete_principal + suma_detalles
                    saldo_pendiente = total_real - anticipo
                    
                    print(f"\nTotal Final: ${total_real:,.0f}")
                    print(f"Saldo Pendiente: ${saldo_pendiente:,.0f}")
                else:
                    print("Error: No se encontró la reserva en la Base de Datos.")
            except ValueError:
                print("Error: Ingrese un ID numérico válido.")
            except Exception as e:
                print(f"Error al consultar la base de datos: {e}")

        elif opcion == '9':
            print("Saliendo...")
            conexion.close()
            break
        else:
            print("Error: Opción de menú inválida.")
            
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
