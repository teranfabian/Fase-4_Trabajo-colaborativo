# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# ---------------------------------------------------------------------
# Parte 1: Librerías, logs, excepciones y clase abstracta 

# Importo las librerías necesarias para el funcionamiento del programa
from abc import ABC, abstractmethod
import logging
import re

# Creo el logging para registrar eventos y errores del programa
logging.basicConfig(
    filename="software_fj.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")


# Excepciones personalizadas 
class ErrorSistema(Exception):
    """
    Excepción general del sistema.

    Todas las excepciones personalizadas del programa
    heredarán de esta clase.
"""
    pass

class DatoInvalidoError(ErrorSistema):
    """
    Se produce cuando un dato no cumple las validaciones. 
    """
    pass

class ClienteDuplicadoError(ErrorSistema):
    """
    Se produce cuando se intenta registrar un cliente
    que ya existe en el sistema.
    """
    pass

class ClienteNoEncontradoError(ErrorSistema):
    """
    Se produce cuando no se encuentra un cliente registrado.
    """
    pass

class ServicioDuplicadoError(ErrorSistema):
    """
    Se produce cuando se intenta registrar un servicio
    que ya existe en el sistema.
    """
    pass

class ServicioNoEncontradoError(ErrorSistema):
    """
    Se produce cuando no se encuentra un servicio registrado.
    """
    pass

class ServicioNoDisponibleError(ErrorSistema):
    """
    Se produce cuando se intenta reservar un servicio
    que no está disponible.
    """
    pass

class ReservaDuplicadaError(ErrorSistema):
    """
    Se produce cuando se intenta registrar una reserva
    con un código que ya existe.
    """
    pass

class ReservaInvalidaError(ErrorSistema):
    """
    Se produce cuando una reserva contiene datos incorrectos.
    """
    pass

class OperacionNoPermitidaError(ErrorSistema):
    """
    Se produce cuando se intenta realizar una operación
    que no está permitida.
    """
    pass

class CalculoCostoError(ErrorSistema):
    """
    Se produce cuando ocurre una inconsistencia durante
    el cálculo del costo de un servicio.
    """
    pass


# Creo la clase abstracta Entidad 
class Entidad(ABC):
    
    # Constructor de la clase Entidad
    def __init__(self, codigo):
        self.__codigo = self.__validar_codigo(codigo)
        self.__activo = True

        logger.info(
            "Código %s validado para %s.",
             self.__codigo,
            type(self).__name__
        )

    @staticmethod
    def __validar_codigo(codigo):
        """
        Valida que el código sea una cadena no vacía.
        """

        if not isinstance(codigo, str):
            raise DatoInvalidoError(
                "El código debe ser una cadena de texto."
            )

        codigo = codigo.strip()

        if not codigo:
            raise DatoInvalidoError(
                "El código no puede estar vacío."
            )

        if len(codigo) < 2:
            raise DatoInvalidoError(
                "El código debe tener al menos 2 caracteres."
            )

        if len(codigo) > 15:
            raise DatoInvalidoError(
                "El código no puede superar los 15 caracteres."
            )

        return codigo.upper()

    @property
    def codigo(self):
        """
        Permite consultar el código de la entidad.
        """
        return self.__codigo

    @property
    def activo(self):
        """
        Permite consultar si la entidad se encuentra activa.
        """
        return self.__activo


    def activar(self):
        """
        Cambia el estado a activo.
        """

        if self.__activo:
            raise OperacionNoPermitidaError(
                f"{type(self).__name__} con código "
                f"{self.__codigo} ya tiene estado activo."
            )

        self.__activo = True

        logger.info(
            "%s con código %s cambió a estado activo.",
            type(self).__name__,
            self.__codigo
        )

    def desactivar(self):
        """
        Cambia el estado a inactivo.
        """

        if not self.__activo:
            raise OperacionNoPermitidaError(
                f"{type(self).__name__} con código "
                f"{self.__codigo} ya tiene estado inactivo."
            )

        self.__activo = False

        logger.info(
            "%s con código %s cambió a estado inactivo.",
            type(self).__name__,
            self.__codigo
        )

    @abstractmethod
    def mostrar_informacion(self):
        """
        Método abstracto que deberá implementarse
        en todas las clases derivadas.
        """
        pass


# ---------------------------------------------------------------------
# Parte 2: Clase Cliente
class Cliente(Entidad):
    """
    Representa un cliente de la empresa Software FJ.
    
    Hereda el código y el estado 
    de la clase Entidad.
    """
    def __init__(self, codigo, identificacion, nombre, email, telefono):
        
        # Valido los datos antes de almacenarlos
        identificacion_validada = self.__validar_identificacion(identificacion)
        nombre_validado = self.__validar_nombre(nombre)
        email_validado = self.__validar_email(email)
        telefono_validado = self.__validar_telefono(telefono)
        
        # Llamo al constructor de la clase base Entidad
        super().__init__(codigo)
        
        # Almaceno los datos validados en atributos privados
        self.__identificacion = identificacion_validada
        self.__nombre = nombre_validado
        self.__email = email_validado
        self.__telefono = telefono_validado

        logger.info(
            "Cliente con código %s fue registrado correctamente.",
            self.codigo
        )
