"""
Módulo producto_digital.py
Define la subclase ProductoDigital que hereda de Producto (Semana 2: Herencia y Polimorfismo).
"""

from .producto import Producto


class ProductoDigital(Producto):
    """
    Representa un producto intangible/descargable (software, ebook, curso, etc.).
    Hereda atributos y métodos de la clase Producto y sobrescribe comportamientos usando super().
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio_base: float,
        tamano_mb: float,
        enlace_descarga: str,
        porcentaje_tarifa_servicio: float = 0.05,
        stock: int = 9999,
    ):
        # Invocación al constructor de la clase padre (Herencia)
        super().__init__(codigo=codigo, nombre=nombre, precio_base=precio_base, stock=stock)
        self.tamano_mb = tamano_mb
        self.enlace_descarga = enlace_descarga
        self.porcentaje_tarifa_servicio = porcentaje_tarifa_servicio

    # --- Getter y Setter de Tamaño en MB ---
    @property
    def tamano_mb(self) -> float:
        return self.__tamano_mb

    @tamano_mb.setter
    def tamano_mb(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El tamaño del archivo debe ser un número válido.")

        if val_float <= 0:
            raise ValueError("El tamaño en MB debe ser mayor a 0.")
        self.__tamano_mb = round(val_float, 2)

    # --- Getter y Setter de Enlace de Descarga ---
    @property
    def enlace_descarga(self) -> str:
        return self.__enlace_descarga

    @enlace_descarga.setter
    def enlace_descarga(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El enlace de descarga no puede estar vacío.")
        self.__enlace_descarga = valor.strip()

    # --- Getter y Setter de Tarifa de Servicio Digital ---
    @property
    def porcentaje_tarifa_servicio(self) -> float:
        return self.__porcentaje_tarifa_servicio

    @porcentaje_tarifa_servicio.setter
    def porcentaje_tarifa_servicio(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El porcentaje de tarifa digital debe ser un número válido.")

        if val_float < 0:
            raise ValueError("El porcentaje de tarifa no puede ser negativo.")
        self.__porcentaje_tarifa_servicio = round(val_float, 4)

    # --- Sobrescritura de Métodos Polimórficos ---
    def calcular_precio_final(self) -> float:
        """
        Sobrescribe el método de la clase padre.
        Aplica un cargo por servicio de almacenamiento/distribución digital al precio base.
        """
        precio_base_padre = super().calcular_precio_final()
        recargo_digital = precio_base_padre * self.__porcentaje_tarifa_servicio
        return round(precio_base_padre + recargo_digital, 2)

    def obtener_detalle(self) -> str:
        """
        Sobrescribe la descripción agregando atributos específicos de producto digital.
        """
        detalle_padre = super().obtener_detalle()
        return (
            f"{detalle_padre} | Tipo: Digital | "
            f"Tamaño: {self.__tamano_mb} MB | Link: {self.__enlace_descarga}"
        )

    def __repr__(self) -> str:
        return (
            f"ProductoDigital(codigo='{self.codigo}', nombre='{self.nombre}', "
            f"precio_base={self.precio_base}, tamano_mb={self.__tamano_mb}, "
            f"enlace_descarga='{self.__enlace_descarga}', stock={self.stock})"
        )
