"""
Paquete src: Sistema de Gestión de Productos, Clientes y Proformas Comerciales
Actividad Semana 3 - Polimorfismo, Interfaces y Clases Abstractas (UEES)
"""

from .cliente import Cliente
from .cliente_mayorista import ClienteMayorista
from .cliente_minorista import ClienteMinorista
from .producto import Producto
from .producto_fisico import ProductoFisico
from .producto_digital import ProductoDigital
from .item_proforma import ItemProforma
from .proforma import Proforma

__all__ = [
    "Cliente",
    "ClienteMayorista",
    "ClienteMinorista",
    "Producto",
    "ProductoFisico",
    "ProductoDigital",
    "ItemProforma",
    "Proforma",
]
