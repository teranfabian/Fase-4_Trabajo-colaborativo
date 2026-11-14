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


# validaciones de los datos del cliente
    @staticmethod
    def __validar_identificacion(identificacion):
        """
        Valida que la identificación sea una cadena no vacía.
        """
        if not isinstance(identificacion, str):
            raise DatoInvalidoError(
                "La identificación debe ser una cadena de texto."
            )
            
        identificacion = identificacion.strip()
            
        if not identificacion:
            raise DatoInvalidoError(
                "La identificación no puede estar vacía."
            )
            
        if not identificacion.isdigit():
            raise DatoInvalidoError(
                "La identificación debe contener solo dígitos."
            )
                
        if len(identificacion) < 5 or len(identificacion) > 15:
            raise DatoInvalidoError(
                "La identificación debe tener entre 5 y 15 dígitos."
            )
                
        return identificacion
        
        
    @staticmethod
    def __validar_nombre(nombre):
        """
        Valida que el nombre sea una cadena no vacía.
        """
        if not isinstance(nombre, str):
            raise DatoInvalidoError(
                "El nombre debe ser una cadena de texto."
            )
            
        # Elimino espacios en blanco al inicio y al final del nombre
        nombre = nombre.strip()
        nombre = " ".join(nombre.split())  # Reemplazo múltiples espacios por uno solo
            
        if not nombre:
            raise DatoInvalidoError(
                "El nombre no puede estar vacío."
            )
            
        if len(nombre) < 2 or len(nombre) > 50:
            raise DatoInvalidoError(
                "El nombre debe tener entre 2 y 50 caracteres."
            )
            
        # Permito que el nombre contenga letras, espacios, guiones y apóstrofes
        for caracter in nombre:
            if not (
                caracter.isalpha() 
                or caracter.isspace()
                or caracter in "-'"
                ):
                    
                raise DatoInvalidoError(
                    "El nombre solo puede contener letras, "
                    "espacios, guiones y apóstrofes."
                )
            
        # Devuelvo el nombre con la primera letra de cada palabra en mayúscula
        return nombre.title()
        
        
    @staticmethod
    def __validar_email(email):
        """
        Valida que el email sea una cadena no vacía y tenga un formato válido.
        """
        if not isinstance(email, str):
            raise DatoInvalidoError(
                "El email debe ser una cadena de texto."
            )
            
        # Elimino espacios en blanco al inicio y al final del email y lo convierto a minúsculas
        email = email.strip().lower()
            
        if not email:
            raise DatoInvalidoError(
                "El email no puede estar vacío."
            )
            
        if len(email) < 10 or len(email) > 100:
            raise DatoInvalidoError(
                "El email debe tener entre 10 y 100 caracteres."
            )
            
        # Valido el formato del email usando una expresión regular
        patron_email = r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$"
            
        if not re.fullmatch(patron_email, email):
            raise DatoInvalidoError(
                "El email no tiene un formato válido."
            )
            
        return email.lower()

    
    @staticmethod
    def __validar_telefono(telefono):
        """
        Valida que el teléfono sea una cadena no vacía y tenga un formato válido.
        """
        if not isinstance(telefono, str):
            raise DatoInvalidoError(
                "El teléfono debe ser una cadena de texto."
            )
            
        # Elimino espacios en blanco al inicio y al final del teléfono
        telefono = telefono.strip()
            
        if not telefono:
            raise DatoInvalidoError(
                "El teléfono no puede estar vacío."
            )
            
        # Permite el signo + solamente al comienzo
        if telefono.startswith("+"):
            numero = telefono[1:]
        else:
            numero = telefono
            
        if not numero.isdigit():
            raise DatoInvalidoError(
                "El teléfono debe contener solo dígitos " 
                "y opcionalmente un signo + al inicio."
            )
            
        if len(numero) < 7 or len(numero) > 15:
            raise DatoInvalidoError(
                "El teléfono debe tener entre 7 y 15 dígitos."
            )
                
        return telefono

# Propiedades para consultar y modificar los atributos del cliente    
    @property
    def identificacion(self):
        """
        Permite consultar la identificación del cliente.
        """
        return self.__identificacion
        
    @property
    def nombre(self):
        """
        Permite consultar el nombre del cliente.
        """
        return self.__nombre
        
    @nombre.setter
    def nombre(self, nuevo_nombre):
        """
        Permite modificar el nombre del cliente.
        """
        nombre_anterior = self.__nombre
        self.__nombre = self.__validar_nombre(nuevo_nombre)
            
        logger.info(
            "Nombre del cliente %s actualizado de %s a %s.",
            self.codigo,
            nombre_anterior,
            self.__nombre
        )
        
    @property
    def email(self):
        """
        Permite consultar el email del cliente.
        """
        return self.__email
        
    @email.setter
    def email(self, nuevo_email):
        """
        Permite modificar el email del cliente.
        """
        email_anterior = self.__email
        self.__email = self.__validar_email(nuevo_email)
            
        logger.info(
            "Email del cliente %s actualizado de %s a %s.",
            self.codigo,
            email_anterior,
            self.__email
            )
            
    @property
    def telefono(self):
        """
        Permite consultar el teléfono del cliente.
        """
        return self.__telefono
        
    @telefono.setter
    def telefono(self, nuevo_telefono):
        """
        Permite modificar el teléfono del cliente.
        """
        telefono_anterior = self.__telefono
        self.__telefono = self.__validar_telefono(nuevo_telefono)
            
        logger.info(
            "Teléfono del cliente %s actualizado de %s a %s.",
            self.codigo,
            telefono_anterior,
            self.__telefono
        )


    # Sobrescribo el método abstracto mostrar_informacion de la clase Entidad        
    def mostrar_informacion(self):
        """
        Muestro la información del cliente.
        """
        estado = "Activo" if self.activo else "Inactivo"
            
        return (
            f"Código: {self.codigo}\n"
            f"Identificación: {self.__identificacion}\n"
            f"Nombre: {self.__nombre}\n"
            f"Email: {self.__email}\n"
            f"Teléfono: {self.__telefono}\n"
            f"Estado: {estado}\n"
        )
