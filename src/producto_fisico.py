"""
Módulo producto_fisico.py
Define la subclase ProductoFisico que hereda de Producto (Semana 2: Herencia y Polimorfismo).
"""

from .producto import Producto


class ProductoFisico(Producto):
    """
    Representa un producto tangible que requiere envío y tiene peso.
    Hereda atributos y métodos de la clase Producto y sobrescribe comportamientos usando super().
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio_base: float,
        peso_kg: float,
        tarifa_envio_kg: float = 2.50,
        stock: int = 0,
    ):
        # Invocación al constructor de la clase padre (Herencia)
        super().__init__(codigo=codigo, nombre=nombre, precio_base=precio_base, stock=stock)
        self.peso_kg = peso_kg
        self.tarifa_envio_kg = tarifa_envio_kg

    # --- Getter y Setter de Peso (Kg) ---
    @property
    def peso_kg(self) -> float:
        return self.__peso_kg

    @peso_kg.setter
    def peso_kg(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El peso debe ser un número válido.")

        if val_float <= 0:
            raise ValueError("El peso debe ser mayor a 0 kg.")
        self.__peso_kg = round(val_float, 2)

    # --- Getter y Setter de Tarifa de Envío por Kg ---
    @property
    def tarifa_envio_kg(self) -> float:
        return self.__tarifa_envio_kg

    @tarifa_envio_kg.setter
    def tarifa_envio_kg(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("La tarifa de envío debe ser un número válido.")

        if val_float < 0:
            raise ValueError("La tarifa de envío no puede ser negativa.")
        self.__tarifa_envio_kg = round(val_float, 2)

    @property
    def costo_envio(self) -> float:
        """Calcula el costo total del envío según peso y tarifa."""
        return round(self.__peso_kg * self.__tarifa_envio_kg, 2)

    # --- Sobrescritura de Métodos Polimórficos ---
    def calcular_precio_final(self) -> float:
        """
        Sobrescribe el método de la clase padre.
        Suma el precio base (obtenido con super()) más el costo de envío.
        """
        precio_base_padre = super().calcular_precio_final()
        return round(precio_base_padre + self.costo_envio, 2)

    def obtener_detalle(self) -> str:
        """
        Sobrescribe la descripción agregando atributos específicos de producto físico.
        """
        detalle_padre = super().obtener_detalle()
        return (
            f"{detalle_padre} | Tipo: Físico | "
            f"Peso: {self.__peso_kg} kg | Envío: ${self.costo_envio:.2f}"
        )

    def __repr__(self) -> str:
        return (
            f"ProductoFisico(codigo='{self.codigo}', nombre='{self.nombre}', "
            f"precio_base={self.precio_base}, peso_kg={self.__peso_kg}, "
            f"tarifa_envio_kg={self.__tarifa_envio_kg}, stock={self.stock})"
        )
