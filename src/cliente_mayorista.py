"""
Módulo cliente_mayorista.py
Define la subclase ClienteMayorista que hereda de Cliente (Semana 3: Polimorfismo y Clases Concretas).
"""

from .cliente import Cliente


class ClienteMayorista(Cliente):
    """
    Representa a un cliente corporativo o distribuidor mayorista.
    Hereda de Cliente e implementa su propia lógica de descuento comercial:
    un porcentaje de descuento base y una bonificación adicional por compras por volumen.
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        email: str,
        telefono: str,
        razon_social: str = "",
        porcentaje_descuento: float = 0.15,
        monto_minimo_volumen: float = 500.0,
        porcentaje_adicional_volumen: float = 0.05,
    ):
        super().__init__(cedula=cedula, nombre=nombre, email=email, telefono=telefono)
        self.razon_social = razon_social if razon_social else nombre
        self.porcentaje_descuento = porcentaje_descuento
        self.monto_minimo_volumen = monto_minimo_volumen
        self.porcentaje_adicional_volumen = porcentaje_adicional_volumen

    # --- Getter y Setter de Razón Social ---
    @property
    def razon_social(self) -> str:
        return self.__razon_social

    @razon_social.setter
    def razon_social(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La razón social de la empresa no puede estar vacía.")
        self.__razon_social = valor.strip()

    # --- Getter y Setter de Porcentaje de Descuento Base ---
    @property
    def porcentaje_descuento(self) -> float:
        return self.__porcentaje_descuento

    @porcentaje_descuento.setter
    def porcentaje_descuento(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El porcentaje de descuento debe ser un número válido.")

        if not (0.0 <= val_float <= 1.0):
            raise ValueError("El porcentaje de descuento base debe estar entre 0.0 (0%) y 1.0 (100%).")
        self.__porcentaje_descuento = round(val_float, 4)

    # --- Getter y Setter de Monto Mínimo para Descuento por Volumen ---
    @property
    def monto_minimo_volumen(self) -> float:
        return self.__monto_minimo_volumen

    @monto_minimo_volumen.setter
    def monto_minimo_volumen(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El monto mínimo de volumen debe ser un número válido.")

        if val_float < 0:
            raise ValueError("El monto mínimo de volumen no puede ser negativo.")
        self.__monto_minimo_volumen = round(val_float, 2)

    # --- Getter y Setter de Porcentaje Adicional por Volumen ---
    @property
    def porcentaje_adicional_volumen(self) -> float:
        return self.__porcentaje_adicional_volumen

    @porcentaje_adicional_volumen.setter
    def porcentaje_adicional_volumen(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El porcentaje adicional por volumen debe ser un número válido.")

        if not (0.0 <= val_float <= 1.0):
            raise ValueError("El porcentaje adicional por volumen debe estar entre 0.0 y 1.0.")
        self.__porcentaje_adicional_volumen = round(val_float, 4)

    # --- Implementación Polimórfica de Métodos Abstractos ---
    def calcular_descuento(self, subtotal: float) -> float:
        """
        Calcula el descuento para clientes mayoristas.
        Aplica el porcentaje de descuento base (ej. 15%) y si la compra supera o iguala
        el monto_minimo_volumen (ej. $500), agrega la bonificación por volumen (ej. +5%).
        """
        if subtotal <= 0:
            return 0.0

        tasa_total = self.__porcentaje_descuento
        if subtotal >= self.__monto_minimo_volumen:
            tasa_total += self.__porcentaje_adicional_volumen

        # El descuento no puede superar el subtotal
        tasa_total = min(tasa_total, 1.0)
        return round(subtotal * tasa_total, 2)

    def tipo_cliente(self) -> str:
        return "Mayorista"

    def obtener_resumen(self) -> str:
        resumen_base = super().obtener_resumen()
        tasa_base_pct = int(self.__porcentaje_descuento * 100)
        tasa_vol_pct = int(self.__porcentaje_adicional_volumen * 100)
        return (
            f"{resumen_base} | Razón Social: {self.__razon_social} | "
            f"Desc. Base: {tasa_base_pct}% | Bono Volumen (>=${self.__monto_minimo_volumen:.2f}): +{tasa_vol_pct}%"
        )
