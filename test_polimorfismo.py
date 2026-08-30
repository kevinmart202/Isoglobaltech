"""
Módulo test_polimorfismo.py
Suite de Pruebas Unitarias para la Actividad Semana 3:
- Clases Abstractas e Interfaces (abc.ABC, @abstractmethod)
- Subclases Concretas (ClienteMayorista, ClienteMinorista)
- Polimorfismo en cálculo de descuentos y proformas
- Encapsulación y Composición
"""

import unittest
from datetime import datetime

from src.cliente import Cliente
from src.cliente_mayorista import ClienteMayorista
from src.cliente_minorista import ClienteMinorista
from src.producto import Producto
from src.producto_fisico import ProductoFisico
from src.producto_digital import ProductoDigital
from src.item_proforma import ItemProforma
from src.proforma import Proforma


class TestClasesAbstractasYPolimorfismo(unittest.TestCase):
    """Pruebas unitarias de clases abstractas, herencia y polimorfismo."""

    def test_01_no_se_puede_instanciar_cliente_abstracto(self):
        """Verifica que la clase abstracta Cliente no pueda instanciarse directamente."""
        with self.assertRaises(TypeError):
            # Intentar instanciar la clase abstracta debe disparar TypeError
            Cliente(
                cedula="0928374651",
                nombre="Cliente Genérico",
                email="cliente@correo.com",
                telefono="0991234567",
            )

    def test_02_cliente_mayorista_descuento_base_y_volumen(self):
        """Verifica el cálculo de descuento para ClienteMayorista con y sin bono de volumen."""
        mayorista = ClienteMayorista(
            cedula="0992345678001",
            nombre="TecnoCorp S.A.",
            email="compras@tecnocorp.com",
            telefono="042889900",
            razon_social="TecnoCorp Distribuciones",
            porcentaje_descuento=0.15,
            monto_minimo_volumen=500.0,
            porcentaje_adicional_volumen=0.05,
        )

        self.assertEqual(mayorista.tipo_cliente(), "Mayorista")
        self.assertEqual(mayorista.razon_social, "TecnoCorp Distribuciones")

        # Compra menor al volumen ($400 < $500) -> 15% de $400 = $60.00
        desc_sin_volumen = mayorista.calcular_descuento(400.0)
        self.assertEqual(desc_sin_volumen, 60.00)

        # Compra que alcanza el volumen ($1000 >= $500) -> (15% + 5% = 20%) de $1000 = $200.00
        desc_con_volumen = mayorista.calcular_descuento(1000.0)
        self.assertEqual(desc_con_volumen, 200.00)

    def test_03_cliente_minorista_descuento_fidelidad_y_puntos(self):
        """Verifica el cálculo de descuento para ClienteMinorista con fidelidad y puntos."""
        minorista = ClienteMinorista(
            cedula="0911223344",
            nombre="Carlos Mendoza",
            email="carlos.m@gmail.com",
            telefono="0987654321",
            puntos_fidelidad=40,
            porcentaje_descuento=0.05,
            valor_por_punto=0.05,
        )

        self.assertEqual(minorista.tipo_cliente(), "Minorista")
        self.assertEqual(minorista.puntos_fidelidad, 40)

        # Subtotal: $100
        # Descuento base (5% de $100 = $5.00) + Puntos (40 * 0.05 = $2.00) = $7.00
        descuento_total = minorista.calcular_descuento(100.0)
        self.assertEqual(descuento_total, 7.00)

        # Acumular puntos
        nuevos_pts = minorista.acumular_puntos(150.0)  # 150 // 10 = 15 puntos
        self.assertEqual(nuevos_pts, 15)
        self.assertEqual(minorista.puntos_fidelidad, 55)

    def test_04_polimorfismo_en_proforma_con_ambos_clientes(self):
        """
        Demuestra polimorfismo puro: la Proforma procesa idénticamente a
        ClienteMayorista y ClienteMinorista mediante la abstracción Cliente.
        """
        prod_fisico = ProductoFisico(
            codigo="FIS-01",
            nombre="Laptop Gamer",
            precio_base=1000.0,
            peso_kg=2.0,
            tarifa_envio_kg=5.0,  # Precio final = 1000 + 10 = 1010.00
            stock=10,
        )

        cliente_may = ClienteMayorista(
            cedula="0992345678001",
            nombre="Distribuidora Alfa",
            email="alfa@correo.com",
            telefono="0991112233",
            porcentaje_descuento=0.15,
            monto_minimo_volumen=500.0,
            porcentaje_adicional_volumen=0.05,
        )

        cliente_min = ClienteMinorista(
            cedula="0912345678",
            nombre="Ana Lucía",
            email="ana@correo.com",
            telefono="0998887766",
            puntos_fidelidad=20,
            porcentaje_descuento=0.05,
            valor_por_punto=0.05,
        )

        # Proforma 1: Mayorista con compra de 1 Laptop ($1010.00)
        # Subtotal: $1010.00 >= $500 -> 20% descuento ($202.00)
        # Subtotal neto: $808.00 | IVA 15%: $121.20 | Total: $929.20
        prof_may = Proforma(numero_proforma="PROF-MAY-01", cliente=cliente_may, porcentaje_iva=0.15)
        prof_may.agregar_item(prod_fisico, 1)

        self.assertEqual(prof_may.calcular_subtotal_neto(), 1010.00)
        self.assertEqual(prof_may.calcular_descuento(), 202.00)
        self.assertEqual(prof_may.calcular_subtotal_con_descuento(), 808.00)
        self.assertEqual(prof_may.calcular_iva(), 121.20)
        self.assertEqual(prof_may.calcular_total(), 929.20)

        # Proforma 2: Minorista con compra de 1 Laptop ($1010.00)
        # Subtotal: $1010.00
        # Descuento: 5% ($50.50) + 20 pts * $0.05 ($1.00) = $51.50
        # Subtotal neto: $1010.00 - $51.50 = $958.50 | IVA 15%: $143.78 | Total: $1102.28
        prof_min = Proforma(numero_proforma="PROF-MIN-01", cliente=cliente_min, porcentaje_iva=0.15)
        prof_min.agregar_item(prod_fisico, 1)

        self.assertEqual(prof_min.calcular_subtotal_neto(), 1010.00)
        self.assertEqual(prof_min.calcular_descuento(), 51.50)
        self.assertEqual(prof_min.calcular_subtotal_con_descuento(), 958.50)
        self.assertEqual(prof_min.calcular_iva(), 143.78)
        self.assertEqual(prof_min.calcular_total(), 1102.28)

    def test_05_polimorfismo_en_productos(self):
        """Verifica el cálculo polimórfico en productos físicos y digitales."""
        prod_fis = ProductoFisico("F-01", "Impresora", 200.0, peso_kg=4.0, tarifa_envio_kg=3.0)
        prod_dig = ProductoDigital("D-01", "Antivirus Anual", 50.0, tamano_mb=120.0, enlace_descarga="http://link", porcentaje_tarifa_servicio=0.10)

        self.assertEqual(prod_fis.calcular_precio_final(), 212.00)  # 200 + 4*3
        self.assertEqual(prod_dig.calcular_precio_final(), 55.00)   # 50 + 50*0.10

    def test_06_encapsulamiento_validaciones(self):
        """Valida que los setters rechacen valores inválidos en todas las entidades."""
        with self.assertRaises(ValueError):
            ClienteMayorista(cedula="", nombre="Test", email="test@empresa.com", telefono="12345")

        with self.assertRaises(ValueError):
            ClienteMinorista(cedula="12345", nombre="Test", email="correo-invalido", telefono="12345")

        with self.assertRaises(ValueError):
            Producto("P-01", "Producto", precio_base=-10.0)

        with self.assertRaises(ValueError):
            p = Producto("P-01", "Producto", precio_base=10.0, stock=5)
            p.reducir_stock(10)  # Más del stock disponible


if __name__ == "__main__":
    unittest.main()
