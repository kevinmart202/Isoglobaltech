"""
Módulo cliente.py
Define la clase Cliente implementando encapsulación estricta con atributos privados y métodos getters/setters.
"""

import re


class Cliente:
    """
    Representa un cliente dentro del sistema comercial.
    Aplica encapsulamiento mediante atributos privados (__cedula, __nombre, __email, __telefono).
    """

    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # --- Getter y Setter de Cédula ---
    @property
    def cedula(self) -> str:
        return self.__cedula

    @cedula.setter
    def cedula(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La cédula no puede estar vacía y debe ser una cadena de texto.")
        valor_limpio = valor.strip()
        if len(valor_limpio) < 5:
            raise ValueError("La cédula o identificación debe contener al menos 5 caracteres.")
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

    def obtener_resumen(self) -> str:
        """Retorna una cadena con la información resumida del cliente."""
        return f"Cliente: {self.__nombre} | CI/RUC: {self.__cedula} | Email: {self.__email} | Tel: {self.__telefono}"

    def __str__(self) -> str:
        return self.obtener_resumen()

    def __repr__(self) -> str:
        return f"Cliente(cedula='{self.__cedula}', nombre='{self.__nombre}', email='{self.__email}', telefono='{self.__telefono}')"
