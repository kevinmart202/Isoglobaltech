"""
Módulo item_proforma.py
Define la clase ItemProforma (Semana 2: Elemento de la Composición dentro de Proforma).
"""

from .producto import Producto


class ItemProforma:
    """
    Representa una línea o ítem dentro de una Proforma comercial.
    Asocia un objeto Producto (o sus subclases ProductoFisico/ProductoDigital) con una cantidad.
    """

    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

    # --- Getter y Setter de Producto ---
    @property
    def producto(self) -> Producto:
        return self.__producto

    @producto.setter
    def producto(self, valor: Producto) -> None:
        if not isinstance(valor, Producto):
            raise TypeError("El ítem debe contener una instancia válida de la clase Producto o sus derivadas.")
        self.__producto = valor

    # --- Getter y Setter de Cantidad ---
    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("La cantidad del ítem debe ser un número entero.")
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        self.__cantidad = valor

    # --- Métodos de Negocio ---
    def calcular_subtotal(self) -> float:
        """
        Calcula el subtotal multiplicando la cantidad por el precio final polimórfico del producto.
        """
        return round(self.__producto.calcular_precio_final() * self.__cantidad, 2)

    def obtener_linea_detalle(self) -> str:
        """Genera una línea formateada para la tabla de proforma."""
        tipo = "Físico" if hasattr(self.__producto, "peso_kg") else ("Digital" if hasattr(self.__producto, "tamano_mb") else "Estándar")
        return (
            f"{self.__producto.codigo:<10} | "
            f"{self.__producto.nombre[:22]:<22} | "
            f"{tipo:<8} | "
            f"{self.__cantidad:>4} uds | "
            f"${self.__producto.calcular_precio_final():>8.2f} | "
            f"${self.calcular_subtotal():>8.2f}"
        )

    def __str__(self) -> str:
        return self.obtener_linea_detalle()

    def __repr__(self) -> str:
        return f"ItemProforma(producto={self.__producto.codigo}, cantidad={self.__cantidad}, subtotal={self.calcular_subtotal()})"
