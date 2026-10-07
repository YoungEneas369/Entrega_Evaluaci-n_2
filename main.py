import sys
from conectar import crear_conexion
from dao.paquete_dao import PaqueteDAO
from model.paquete_nacional import PaqueteNacional
from model.paquete_internacional import PaqueteInternacional
from model.paquete_crucero import PaqueteCrucero
from model.viajero import Viajero
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
                precio_clp = float(input("Ingrese precio base (en Pesos Chilenos): "))
                if precio_clp <= 0:
                    print("Error: El precio debe ser mayor a cero.")
                    continue
                    
                tipo = input("Tipo ('nacional', 'internacional' o 'crucero'): ").strip().lower()
                
                # Conversión interna silenciosa para paquetes internacionales
                if tipo in ['internacional', 'crucero']:
                    servicio = MiIndicador()
                    dolar = servicio.obtener_dolar()
                    precio_guardado = precio_clp / dolar
                else:
                    precio_guardado = precio_clp
                
                if tipo == 'nacional':
                    p = PaqueteNacional(None, nombre, precio_guardado, None)
                elif tipo == 'internacional':
                    p = PaqueteInternacional(None, nombre, precio_guardado, None)
                elif tipo == 'crucero':
                    p = PaqueteCrucero(None, nombre, precio_guardado, None)
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
                    nuevo_precio_clp = float(input("Ingrese nuevo precio base (en Pesos Chilenos): "))
                    if nuevo_precio_clp <= 0:
                        print("Error: El precio debe ser mayor a cero.")
                        continue
                        
                    if isinstance(p, (PaqueteInternacional, PaqueteCrucero)):
                        servicio = MiIndicador()
                        dolar = servicio.obtener_dolar()
                        p.precio_base = nuevo_precio_clp / dolar
                    else:
                        p.precio_base = nuevo_precio_clp
                    
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
                id_paquete = int(input("Ingrese ID del paquete a reservar: "))
                paquete = paquete_dao.buscar(id_paquete)
                if not paquete:
                    print("Error: El paquete no existe.")
                    continue
                
                # Validación de Pasaporte si es Internacional o Crucero
                v = None
                if isinstance(paquete, (PaqueteInternacional, PaqueteCrucero)):
                    pasaporte = input("El paquete es internacional. Ingrese pasaporte del viajero: ").strip()
                    try:
                        # Esto validará la regla del negocio inmediatamente
                        v = Viajero("11111111-1", "UsuarioPrueba", pasaporte)
                    except ValueError as e:
                        print(f"Operación denegada: {e}")
                        continue
                
                cupos = int(input("Ingrese cupos actuales del proveedor en la fecha: "))
                pasajeros = int(input("Ingrese cantidad de pasajeros: "))
                
                prov = Proveedor(1, "Latam Airlines")
                prov.agregar_disponibilidad(Disponibilidad("2026-12-01", cupos))
                
                if pasajeros > cupos:
                    print("Operación denegada: El proveedor no tiene suficientes cupos.")
                    continue
                
                print("Consultando valor del dólar actual...")
                indicador = MiIndicador()
                valor_dolar = indicador.obtener_dolar()
                
                precio_total = paquete.calcular_precio_final(valor_dolar) * pasajeros
                print(f"Valor del dólar usado para la reserva: ${valor_dolar}")
                
                cliente = Cliente("Juan", "11111111-1")
                agente = AgenteViajes("Pedro", "22222222-2")
                
                reserva = Reserva(cliente, agente, paquete, prov, "2026-12-01", precio_total, 0, viajero=v)
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
                    for _ in range(pasajeros):
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
