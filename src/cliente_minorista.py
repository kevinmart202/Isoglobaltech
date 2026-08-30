"""
Módulo cliente_minorista.py
Define la subclase ClienteMinorista que hereda de Cliente (Semana 3: Polimorfismo y Clases Concretas).
"""

from .cliente import Cliente


class ClienteMinorista(Cliente):
    """
    Representa a un cliente final o minorista.
    Hereda de Cliente e implementa su propia lógica de descuento comercial:
    un porcentaje de descuento por fidelización y un beneficio económico canjeable por puntos acumulados.
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        email: str,
        telefono: str,
        puntos_fidelidad: int = 0,
        porcentaje_descuento: float = 0.05,
        valor_por_punto: float = 0.05,
    ):
        super().__init__(cedula=cedula, nombre=nombre, email=email, telefono=telefono)
        self.puntos_fidelidad = puntos_fidelidad
        self.porcentaje_descuento = porcentaje_descuento
        self.valor_por_punto = valor_por_punto

    # --- Getter y Setter de Puntos de Fidelidad ---
    @property
    def puntos_fidelidad(self) -> int:
        return self.__puntos_fidelidad

    @puntos_fidelidad.setter
    def puntos_fidelidad(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("Los puntos de fidelidad deben ser un número entero.")
        if valor < 0:
            raise ValueError("Los puntos de fidelidad no pueden ser negativos.")
        self.__puntos_fidelidad = valor

    # --- Getter y Setter de Porcentaje de Descuento ---
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
            raise ValueError("El porcentaje de descuento debe estar entre 0.0 (0%) y 1.0 (100%).")
        self.__porcentaje_descuento = round(val_float, 4)

    # --- Getter y Setter de Valor por Punto ---
    @property
    def valor_por_punto(self) -> float:
        return self.__valor_por_punto

    @valor_por_punto.setter
    def valor_por_punto(self, valor: float) -> None:
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise TypeError("El valor monetario por punto debe ser un número válido.")

        if val_float < 0:
            raise ValueError("El valor por punto no puede ser negativo.")
        self.__valor_por_punto = round(val_float, 4)

    # --- Implementación Polimórfica de Métodos Abstractos ---
    def calcular_descuento(self, subtotal: float) -> float:
        """
        Calcula el descuento para clientes minoristas.
        Combina un descuento porcentual base por cliente frecuente con el saldo acumulado en puntos.
        El descuento total nunca puede exceder el subtotal de la compra.
        """
        if subtotal <= 0:
            return 0.0

        descuento_base = subtotal * self.__porcentaje_descuento
        descuento_puntos = self.__puntos_fidelidad * self.__valor_por_punto
        total_descuento = min(subtotal, descuento_base + descuento_puntos)

        return round(total_descuento, 2)

    def tipo_cliente(self) -> str:
        return "Minorista"

    def acumular_puntos(self, monto_compra: float) -> int:
        """Acumula 1 punto por cada $10 gastados en la compra."""
        if monto_compra > 0:
            puntos_ganados = int(monto_compra // 10)
            self.__puntos_fidelidad += puntos_ganados
            return puntos_ganados
        return 0

    def obtener_resumen(self) -> str:
        resumen_base = super().obtener_resumen()
        tasa_pct = int(self.__porcentaje_descuento * 100)
        return (
            f"{resumen_base} | Puntos Club: {self.__puntos_fidelidad} pts "
            f"(${self.__puntos_fidelidad * self.__valor_por_punto:.2f}) | Desc. Base: {tasa_pct}%"
        )
