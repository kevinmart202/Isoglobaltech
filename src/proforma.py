"""
Módulo proforma.py
Define la clase Proforma (Semana 2: Composición con ItemProforma y Asociación con Cliente).
"""

from datetime import datetime
from typing import List, Optional
from .cliente import Cliente
from .producto import Producto
from .item_proforma import ItemProforma


class Proforma:
    """
    Representa una proforma comercial / cotización.
    Demuestra el principio de Composición: contiene una colección de objetos ItemProforma.
    """

    def __init__(
        self,
        numero_proforma: str,
        cliente: Cliente,
        fecha: Optional[datetime] = None,
        porcentaje_iva: float = 0.15,
    ):
        self.numero_proforma = numero_proforma
        self.cliente = cliente
        self.__fecha = fecha if fecha is not None else datetime.now()
        self.porcentaje_iva = porcentaje_iva
        # Composición: la proforma gestiona internamente la lista de items
        self.__items: List[ItemProforma] = []

    # --- Getter y Setter de Número de Proforma ---
    @property
    def numero_proforma(self) -> str:
        return self.__numero_proforma

    @numero_proforma.setter
    def numero_proforma(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El número de proforma no puede estar vacío.")
        self.__numero_proforma = valor.strip().upper()

    # --- Getter y Setter de Cliente ---
    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @cliente.setter
    def cliente(self, valor: Cliente) -> None:
        if not isinstance(valor, Cliente):
            raise TypeError("El cliente debe ser una instancia de la clase Cliente.")
        self.__cliente = valor

    # --- Getter de Fecha ---
    @property
    def fecha(self) -> datetime:
        return self.__fecha

    # --- Getter y Setter de Porcentaje IVA ---
    @property
    def porcentaje_iva(self) -> float:
        return self.__porcentaje_iva

    @porcentaje_iva.setter
    def porcentaje_iva(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El porcentaje de IVA debe ser un número válido.")

        if val_float < 0:
            raise ValueError("El porcentaje de IVA no puede ser negativo.")
        self.__porcentaje_iva = round(val_float, 4)

    # --- Getter de Items (Retorna copia para proteger encapsulación) ---
    @property
    def items(self) -> List[ItemProforma]:
        return list(self.__items)

    # --- Métodos de Gestión de Composición ---
    def agregar_item(self, producto: Producto, cantidad: int) -> ItemProforma:
        """
        Crea y agrega un nuevo ItemProforma a la colección.
        Valida que el producto tenga stock suficiente y reduce dicho stock.
        """
        if not isinstance(producto, Producto):
            raise TypeError("El producto debe ser una instancia válida de Producto o sus subclases.")

        # Verificar si el producto ya existe en la proforma para acumular cantidad
        for item in self.__items:
            if item.producto.codigo == producto.codigo:
                producto.reducir_stock(cantidad)
                item.cantidad += cantidad
                return item

        # Si es nuevo ítem
        producto.reducir_stock(cantidad)
        nuevo_item = ItemProforma(producto=producto, cantidad=cantidad)
        self.__items.append(nuevo_item)
        return nuevo_item

    def eliminar_item(self, codigo_producto: str) -> bool:
        """
        Elimina un ítem de la proforma por código de producto y restaura su stock.
        """
        codigo_limpio = codigo_producto.strip().upper()
        for idx, item in enumerate(self.__items):
            if item.producto.codigo == codigo_limpio:
                item.producto.aumentar_stock(item.cantidad)
                self.__items.pop(idx)
                return True
        return False

    def contar_items(self) -> int:
        """Retorna la cantidad total de líneas de producto en la proforma."""
        return len(self.__items)

    # --- Métodos de Cálculo Financiero ---
    def calcular_subtotal_neto(self) -> float:
        """Calcula la suma de los subtotales de todos los ítems."""
        return round(sum(item.calcular_subtotal() for item in self.__items), 2)

    def calcular_iva(self) -> float:
        """Calcula el valor del IVA sobre el subtotal neto."""
        return round(self.calcular_subtotal_neto() * self.__porcentaje_iva, 2)

    def calcular_total(self) -> float:
        """Calcula el monto total a pagar (Subtotal + IVA)."""
        return round(self.calcular_subtotal_neto() + self.calcular_iva(), 2)

    # --- Representación y Salida Formateada ---
    def generar_proforma_texto(self) -> str:
        """Genera una representación tabular completa de la proforma."""
        separador = "=" * 80
        linea = "-" * 80
        fecha_str = self.__fecha.strftime("%d/%m/%Y %H:%M:%S")

        encabezado = [
            separador,
            "                          ISOGLOBALTECH - SISTEMA DE FACTURACIÓN",
            "                                 PROFORMA COMERCIAL",
            separador,
            f" N° Proforma: {self.__numero_proforma:<25} Fecha de Emisión: {fecha_str}",
            f" Cliente:     {self.__cliente.nombre:<25} Cédula/RUC:       {self.__cliente.cedula}",
            f" Email:       {self.__cliente.email:<25} Teléfono:         {self.__cliente.telefono}",
            linea,
            f" {'CÓDIGO':<10} | {'DESCRIPCIÓN':<22} | {'TIPO':<8} | {'CANT':<4} | {'P. UNIT':>8} | {'SUBTOTAL':>8}",
            linea,
        ]

        detalles = []
        if not self.__items:
            detalles.append(" [No se han registrado ítems en esta proforma]")
        else:
            for item in self.__items:
                detalles.append(f" {item.obtener_linea_detalle()}")

        pie = [
            linea,
            f" {'SUBTOTAL NETO:':>65} ${self.calcular_subtotal_neto():>10.2f}",
            f" {'IVA (' + str(int(self.__porcentaje_iva * 100)) + '%):':>65} ${self.calcular_iva():>10.2f}",
            f" {'TOTAL A PAGAR:':>65} ${self.calcular_total():>10.2f}",
            separador,
        ]

        return "\n".join(encabezado + detalles + pie)

    def __str__(self) -> str:
        return self.generar_proforma_texto()

    def __repr__(self) -> str:
        return (
            f"Proforma(numero='{self.__numero_proforma}', cliente='{self.__cliente.nombre}', "
            f"items={len(self.__items)}, total={self.calcular_total()})"
        )
