"""
Módulo cliente.py
Define la clase abstracta Cliente (Semana 3: Clases Abstractas e Interfaces).
Aplica encapsulación estricta con atributos privados y métodos getters/setters,
además de definir el contrato abstracto para el cálculo polimórfico de descuentos.
"""

from abc import ABC, abstractmethod
import re


class Cliente(ABC):
    """
    Clase base abstracta que representa un cliente genérico dentro del sistema comercial.
    Establece la estructura común (cédula, nombre, email, teléfono) y define el método
    abstracto calcular_descuento() que todas las subclases deben implementar obligatoriamente.
    """

    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # --- Getter y Setter de Cédula / Identificación ---
    @property
    def cedula(self) -> str:
        return self.__cedula

    @cedula.setter
    def cedula(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación (Cédula/RUC) no puede estar vacía.")
        valor_limpio = valor.strip()
        if len(valor_limpio) < 5:
            raise ValueError("La identificación debe contener al menos 5 caracteres.")
        self.__cedula = valor_limpio

    # --- Getter y Setter de Nombre ---
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    # --- Getter y Setter de Email ---
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El correo electrónico no puede estar vacío.")
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, valor.strip()):
            raise ValueError(f"El formato de correo '{valor}' no es válido.")
        self.__email = valor.strip()

    # --- Getter y Setter de Teléfono ---
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El teléfono no puede estar vacío.")
        self.__telefono = valor.strip()

    # --- Métodos Abstractos (Contrato de Polimorfismo) ---
    @abstractmethod
    def calcular_descuento(self, subtotal: float) -> float:
        """
        Calcula el monto del descuento aplicable según el subtotal de la compra y
        el tipo concreto de cliente.
        
        :param subtotal: Monto subtotal de los productos antes de descuento.
        :return: Monto a descontar en dólares ($).
        """
        pass

    @abstractmethod
    def tipo_cliente(self) -> str:
        """
        Retorna la denominación del tipo de cliente (ej. 'Mayorista', 'Minorista').
        """
        pass

    # --- Métodos de Representación ---
    def obtener_resumen(self) -> str:
        """Retorna una cadena con la información resumida del cliente."""
        return (
            f"[{self.tipo_cliente()}] {self.__nombre} | "
            f"CI/RUC: {self.__cedula} | Email: {self.__email} | Tel: {self.__telefono}"
        )

    def __str__(self) -> str:
        return self.obtener_resumen()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(cedula='{self.__cedula}', "
            f"nombre='{self.__nombre}', email='{self.__email}', telefono='{self.__telefono}')"
        )
