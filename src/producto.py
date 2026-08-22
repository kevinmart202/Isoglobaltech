"""
Módulo producto.py
Define la clase base Producto (Semana 1: Clases, Encapsulación y Getters/Setters).
"""


class Producto:
    """
    Clase base que representa un producto general en el catálogo.
    Implementa encapsulación de atributos con validaciones en los métodos setters.
    """

    def __init__(self, codigo: str, nombre: str, precio_base: float, stock: int = 0):
        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = precio_base
        self.stock = stock

    # --- Getter y Setter de Código ---
    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self.__codigo = valor.strip().upper()

    # --- Getter y Setter de Nombre ---
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self.__nombre = valor.strip()

    # --- Getter y Setter de Precio Base ---
    @property
    def precio_base(self) -> float:
        return self.__precio_base

    @precio_base.setter
    def precio_base(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El precio base debe ser un número válido.")

        if val_float <= 0:
            raise ValueError("El precio base debe ser mayor a 0.")
        self.__precio_base = round(val_float, 2)

    # --- Getter y Setter de Stock ---
    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("El stock debe ser un número entero.")
        if valor < 0:
            raise ValueError("El stock no puede ser un valor negativo.")
        self.__stock = valor

    # --- Métodos de Negocio ---
    def calcular_precio_final(self) -> float:
        """
        Calcula el precio final de venta.
        En la clase base corresponde al precio base. Las subclases sobrescribirán este método.
        """
        return self.__precio_base

    def reducir_stock(self, cantidad: int) -> None:
        """Reduce la cantidad de existencias disponibles."""
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a reducir debe ser un entero positivo.")
        if cantidad > self.__stock:
            raise ValueError(
                f"Stock insuficiente para '{self.__nombre}'. Disponible: {self.__stock}, solicitado: {cantidad}"
            )
        self.__stock -= cantidad

    def aumentar_stock(self, cantidad: int) -> None:
        """Aumenta el stock del producto."""
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a agregar debe ser un entero positivo.")
        self.__stock += cantidad

    def obtener_detalle(self) -> str:
        """Retorna una descripción detallada del producto."""
        return (
            f"[{self.__codigo}] {self.__nombre} | "
            f"Precio Base: ${self.__precio_base:.2f} | "
            f"Stock: {self.__stock} uds | "
            f"Precio Final: ${self.calcular_precio_final():.2f}"
        )

    def __str__(self) -> str:
        return self.obtener_detalle()

    def __repr__(self) -> str:
        return (
            f"Producto(codigo='{self.__codigo}', nombre='{self.__nombre}', "
            f"precio_base={self.__precio_base}, stock={self.__stock})"
        )
