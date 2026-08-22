"""
Módulo main.py
Sistema Interactivo Comercial y de Emisión de Proformas / Facturas
Programación Estructurada - Semanas 1 y 2
Universidad Espíritu Santo (UEES)
"""

import os
import sys
from datetime import datetime
from typing import List, Optional

from src.cliente import Cliente
from src.producto import Producto
from src.producto_fisico import ProductoFisico
from src.producto_digital import ProductoDigital
from src.proforma import Proforma


def pausar() -> None:
    """Pausa la ejecución hasta que el usuario presione ENTER."""
    input("\nPresione [ENTER] para continuar...")


def mostrar_encabezado():
    print("\n" + "=" * 80)
    print("   ISOGLOBALTECH - SISTEMA DE FACTURACIÓN & PROFORMAS   ".center(80))
    print("=" * 80)


def leer_texto_no_vacio(mensaje: str) -> str:
    """Solicita un texto no vacío al usuario."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  ⚠️ El campo no puede quedar vacío. Intente de nuevo.")


def leer_float_positivo(mensaje: str, default: Optional[float] = None) -> float:
    """Solicita un número decimal mayor a cero."""
    while True:
        entrada = input(mensaje).strip()
        if not entrada and default is not None:
            return default
        try:
            num = float(entrada)
            if num > 0:
                return num
            print("  ⚠️ Ingrese un valor mayor a cero (0).")
        except ValueError:
            print("  ⚠️ Ingrese un número válido (ejemplo: 25.50).")


def leer_entero_positivo(mensaje: str) -> int:
    """Solicita un número entero positivo."""
    while True:
        entrada = input(mensaje).strip()
        try:
            num = int(entrada)
            if num > 0:
                return num
            print("  ⚠️ La cantidad debe ser un número entero mayor a cero.")
        except ValueError:
            print("  ⚠️ Ingrese un número entero válido (ejemplo: 2).")


def solicitar_datos_cliente() -> Cliente:
    """Solicita interactivamente los datos del cliente con validación mediante setters de POO."""
    print("\n" + "-" * 80)
    print(" 👤 PASO 1: REGISTRO DE DATOS DEL CLIENTE")
    print("-" * 80)
    
    while True:
        try:
            cedula = leer_texto_no_vacio(" Ingrese Cédula o RUC (mínimo 5 dígitos): ")
            nombre = leer_texto_no_vacio(" Ingrese Nombre y Apellido completo: ")
            email = leer_texto_no_vacio(" Ingrese Correo Electrónico (ej. usuario@dominio.com): ")
            telefono = leer_texto_no_vacio(" Ingrese Teléfono o Celular: ")

            # La creación invoca los setters y aplica encapsulación estricta
            cliente = Cliente(cedula=cedula, nombre=nombre, email=email, telefono=telefono)
            print(f"\n ✅ Cliente '{cliente.nombre}' registrado correctamente.")
            return cliente
        except ValueError as val_err:
            print(f"\n ❌ Error de validación: {val_err}")
            print(" Por favor ingrese los datos nuevamente con el formato correcto.\n")


def registrar_nuevo_producto_interactivo(catalogo: List[Producto]) -> Optional[Producto]:
    """Permite registrar un producto físico o digital interactivamente."""
    print("\n" + "-" * 80)
    print(" ➕ REGISTRO DE NUEVO PRODUCTO EN EL CATÁLOGO")
    print("-" * 80)
    print(" Tipo de Producto:")
    print("   [1] Producto Físico  (con peso en kg y costo de envío)")
    print("   [2] Producto Digital (software/descarga con tarifa de servicio)")
    print("   [0] Cancelar registro")

    opcion_tipo = input("\n Seleccione una opción (1/2/0): ").strip()
    if opcion_tipo == "0":
        return None

    if opcion_tipo not in ["1", "2"]:
        print(" ❌ Opción inválida.")
        return None

    while True:
        try:
            codigo = leer_texto_no_vacio(" Código del producto (ej. FIS-01 / DIG-01): ").upper()
            if any(p.codigo == codigo for p in catalogo):
                print(f" ❌ Ya existe un producto con el código '{codigo}'. Ingrese uno diferente.")
                continue

            nombre = leer_texto_no_vacio(" Nombre / Descripción del producto: ")
            precio_base = leer_float_positivo(" Precio Base ($): ")
            stock = leer_entero_positivo(" Stock inicial disponible: ")

            if opcion_tipo == "1":
                peso = leer_float_positivo(" Peso del producto en Kilogramos (kg): ")
                tarifa_envio = leer_float_positivo(" Tarifa de envío por Kg ($) [Enter para $2.50]: ", default=2.50)
                
                nuevo_prod = ProductoFisico(
                    codigo=codigo,
                    nombre=nombre,
                    precio_base=precio_base,
                    peso_kg=peso,
                    tarifa_envio_kg=tarifa_envio,
                    stock=stock,
                )
            else:
                tamano_mb = leer_float_positivo(" Tamaño del archivo descargable en MB: ")
                enlace = leer_texto_no_vacio(" Enlace de descarga (URL o link): ")
                tarifa_srv = leer_float_positivo(" Porcentaje de tarifa digital (ej. 0.05 para 5%) [Enter para 0.05]: ", default=0.05)

                nuevo_prod = ProductoDigital(
                    codigo=codigo,
                    nombre=nombre,
                    precio_base=precio_base,
                    tamano_mb=tamano_mb,
                    enlace_descarga=enlace,
                    porcentaje_tarifa_servicio=tarifa_srv,
                    stock=stock,
                )

            catalogo.append(nuevo_prod)
            print(f"\n ✅ Producto '{nuevo_prod.nombre}' agregado exitosamente al catálogo.")
            print(f"    Precio Base: ${nuevo_prod.precio_base:.2f} | Precio Final Polimórfico: ${nuevo_prod.calcular_precio_final():.2f}")
            return nuevo_prod

        except ValueError as err:
            print(f"\n ❌ Error en los datos del producto: {err}")
            print(" Por favor ingrese los datos nuevamente.\n")


def mostrar_catalogo_tabla(catalogo: List[Producto]) -> None:
    """Muestra los productos disponibles en formato de tabla clara."""
    print("\n📦 CATÁLOGO DE PRODUCTOS DISPONIBLES:")
    print(f" {'#':<3} | {'CÓDIGO':<9} | {'TIPO':<8} | {'DESCRIPCIÓN':<30} | {'P. BASE':>8} | {'P. FINAL':>9} | {'STOCK':>6}")
    print(" " + "-" * 82)
    for idx, prod in enumerate(catalogo, 1):
        tipo_str = "Físico" if isinstance(prod, ProductoFisico) else "Digital"
        print(
            f" [{idx:2}] | {prod.codigo:<9} | {tipo_str:<8} | {prod.nombre[:30]:<30} | "
            f"${prod.precio_base:>7.2f} | ${prod.calcular_precio_final():>8.2f} | {prod.stock:>6}"
        )
    print(" " + "-" * 82)
    print(" * P. Final incluye costo de envío para físicos o tarifa de servicio para digitales.")


def emitir_factura_paso_a_paso(catalogo: List[Producto]) -> None:
    """Flujo guiado paso a paso para crear clientes, seleccionar productos y emitir la factura final."""
    mostrar_encabezado()
    print("\n 🚀 ASISTENTE INTERACTIVO DE EMISIÓN DE FACTURA / PROFORMA")
    print(" Este asistente le guiará para registrar el cliente, seleccionar productos y emitir el documento final.\n")

    # 1. Registrar Cliente
    cliente = solicitar_datos_cliente()

    # 2. Inicializar Proforma
    num_proforma = f"PROF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    proforma = Proforma(
        numero_proforma=num_proforma,
        cliente=cliente,
        fecha=datetime.now(),
        porcentaje_iva=0.15,
    )

    # 3. Ciclo de agregar productos
    while True:
        print("\n" + "-" * 80)
        print(" 🛒 PASO 2: AGREGAR PRODUCTOS A LA FACTURA")
        print("-" * 80)
        
        mostrar_catalogo_tabla(catalogo)
        
        print("\n Opciones:")
        print("   [1] Seleccionar un producto del catálogo por su CÓDIGO o NÚMERO")
        print("   [2] Registrar un NUEVO producto y agregarlo")
        print("   [3] Finalizar selección y EMITIR FACTURA")
        print("   [0] Cancelar factura y salir al menú")

        opc = input("\n Seleccione opción (1/2/3/0): ").strip()

        if opc == "0":
            # Si cancela, devolvemos el stock de los productos ya agregados
            for item in proforma.items:
                item.producto.aumentar_stock(item.cantidad)
            print("\n ⚠️ Emisión de factura cancelada. El inventario ha sido restablecido.")
            pausar()
            return

        elif opc == "2":
            nuevo = registrar_nuevo_producto_interactivo(catalogo)
            if nuevo:
                cant = leer_entero_positivo(f" Ingrese la cantidad a comprar de '{nuevo.nombre}': ")
                try:
                    proforma.agregar_item(nuevo, cant)
                    print(f" ✅ Agregado: {cant} unidad(es) de '{nuevo.nombre}'.")
                    print(f" 💵 Subtotal parcial de la factura: ${proforma.calcular_subtotal_neto():.2f}")
                except Exception as e:
                    print(f" ❌ No se pudo agregar: {e}")

        elif opc == "1":
            seleccion = input("\n Ingrese el CÓDIGO o NÚMERO [#] del producto: ").strip().upper()
            
            # Buscar por número de índice o código
            producto_elegido = None
            if seleccion.isdigit() and 1 <= int(seleccion) <= len(catalogo):
                producto_elegido = catalogo[int(seleccion) - 1]
            else:
                producto_elegido = next((p for p in catalogo if p.codigo == seleccion), None)

            if not producto_elegido:
                print(f" ❌ No se encontró ningún producto correspondiente a '{seleccion}'.")
                continue

            print(f"\n 👉 Seleccionado: {producto_elegido.nombre}")
            print(f"    Stock disponible: {producto_elegido.stock} uds. | Precio Final Unitario: ${producto_elegido.calcular_precio_final():.2f}")
            
            if producto_elegido.stock <= 0:
                print(" ❌ No hay stock disponible de este producto.")
                continue

            cant = leer_entero_positivo(f" Ingrese la cantidad a comprar: ")
            try:
                proforma.agregar_item(producto_elegido, cant)
                print(f"\n ✅ ¡{cant} unidad(es) de '{producto_elegido.nombre}' agregada(s) con éxito!")
                print(f" 💵 Subtotal neto acumulado: ${proforma.calcular_subtotal_neto():.2f} | Total con IVA 15%: ${proforma.calcular_total():.2f}")
            except Exception as err:
                print(f"\n ❌ Error al agregar producto: {err}")

        elif opc == "3":
            if len(proforma.items) == 0:
                print(" ⚠️ Debe agregar al menos un producto a la factura antes de emitirla.")
                continue
            break
        else:
            print(" ❌ Opción inválida.")

    # 4. Emisión de la Factura Final
    mostrar_encabezado()
    print("\n 🎉 ¡FACTURA / PROFORMA EMITIDA EXITOSAMENTE!\n")
    texto_factura = proforma.generar_proforma_texto()
    print(texto_factura)
    pausar()


def inicializar_catalogo_base() -> List[Producto]:
    """Crea un catálogo inicial con productos físicos y digitales listos para usar."""
    return [
        ProductoFisico(
            codigo="FIS-01",
            nombre="Laptop Dell Inspiron 15",
            precio_base=850.00,
            peso_kg=2.40,
            tarifa_envio_kg=3.50,
            stock=10,
        ),
        ProductoFisico(
            codigo="FIS-02",
            nombre="Teclado Mecánico RGB",
            precio_base=65.00,
            peso_kg=0.90,
            tarifa_envio_kg=3.00,
            stock=25,
        ),
        ProductoDigital(
            codigo="DIG-01",
            nombre="Masterclass IA & POO en Python",
            precio_base=120.00,
            tamano_mb=3500.0,
            enlace_descarga="https://cursos.uees.edu.ec/descargas/ia-poo",
            porcentaje_tarifa_servicio=0.08,
            stock=100,
        ),
        ProductoDigital(
            codigo="DIG-02",
            nombre="Licencia JetBrains All Products",
            precio_base=199.00,
            tamano_mb=850.0,
            enlace_descarga="https://jetbrains.com/activate/uees",
            porcentaje_tarifa_servicio=0.05,
            stock=50,
        ),
    ]


def menu_principal():
    catalogo = inicializar_catalogo_base()

    while True:
        mostrar_encabezado()
        print("  MENÚ PRINCIPAL:")
        print("  [1] 📝 CREAR Y EMITIR FACTURA / PROFORMA (Paso a Paso)")
        print("  [2] 📦 Ver catálogo de productos")
        print("  [3] ➕ Registrar nuevo producto en el catálogo (Físico o Digital)")
        print("  [0] 🚪 Salir del Sistema")
        print("=" * 80)

        opcion = input(" Seleccione una opción (0-3): ").strip()

        if opcion == "1":
            emitir_factura_paso_a_paso(catalogo)
        elif opcion == "2":
            mostrar_encabezado()
            mostrar_catalogo_tabla(catalogo)
            pausar()
        elif opcion == "3":
            mostrar_encabezado()
            registrar_nuevo_producto_interactivo(catalogo)
            pausar()
        elif opcion == "0":
            print("\n ¡Gracias por utilizar el Sistema Comercial ISOGLOBALTECH! Hasta luego.\n")
            break
        else:
            print("\n ❌ Opción no válida. Por favor intente de nuevo.")
            pausar()


if __name__ == "__main__":
    menu_principal()


