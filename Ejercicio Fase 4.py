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
            
        if len(email) < 6 or len(email) > 30:
            raise DatoInvalidoError(
                "El email debe tener entre 6 y 30 caracteres."
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


# ------------------------------------------------------------------           
# Parte 3:  Clase abstracta Servicio y clases derivadas

class Servicio(Entidad, ABC):
    """
    Representa los servicios ofrecidos por la empresa Software FJ.
    """
    
    def __init__(self, codigo, nombre,  precio_base, disponible=True):
                
        # Llamo al constructor de la clase base Entidad
        super().__init__(codigo)
        
        # Almaceno los datos validados en atributos privados
        self.__nombre = self.__validar_nombre(nombre)
        self.__precio_base = self.__validar_precio_base(precio_base)
        self.__disponible = self.__validar_disponible(disponible)

        logger.info(
            "Datos generales del servicio %s validados correctamente.",
            self.codigo
        )
    
    # Validaciones de los datos del servicio    
    @staticmethod
    def __validar_nombre(nombre):
        """
        Valida el nombre del servicio.
        """
        if not isinstance(nombre, str):
            raise DatoInvalidoError(
                "El nombre del servicio debe ser una cadena de texto."
            )
            
        # Elimino espacios en blanco al inicio y al final del nombre
        nombre = nombre.strip()
        nombre = " ".join(nombre.split())  # Reemplazo múltiples espacios por uno solo
            
        if not nombre:
            raise DatoInvalidoError(
                "El nombre del servicio no puede estar vacío."
            )
            
        if len(nombre) < 2 or len(nombre) > 50:
            raise DatoInvalidoError(
                "El nombre del servicio debe tener entre 2 y 50 caracteres."
            )
            
        # Devuelvo el nombre con la primera letra de cada palabra en mayúscula
        return nombre.title()
    
    @staticmethod
    def __validar_precio_base(precio_base):
        """
        Valida el precio base del servicio.
        """
        if  isinstance(precio_base, bool):
            raise DatoInvalidoError(
                "El precio base del servicio debe ser un número."
            )
            
        try:
            precio_base = float(precio_base)
        
        except (ValueError, TypeError) as error_original:
            raise DatoInvalidoError(
                "El precio base del servicio debe ser un valor numérico."
            ) from error_original

        if precio_base <= 0:
            raise DatoInvalidoError(
                "El precio base del servicio debe ser mayor que cero."
            )

        return precio_base
    
    @staticmethod
    def __validar_disponible(disponible):
        """
        Valida el estado de disponibilidad del servicio.
        """
        if not isinstance(disponible, bool):
            raise DatoInvalidoError(
                "El estado de disponibilidad del servicio debe ser un valor booleano."
            )
        
        return disponible
      
    @staticmethod
    def _validar_duracion(duracion):
        """
        Valida la duración del servicio.
        """
        if isinstance(duracion, bool):
            raise DatoInvalidoError(
                "La duración debe ser un valor numérico."
            )
            
        try:
            duracion = float(duracion)

        except (ValueError, TypeError) as error_original:
            raise DatoInvalidoError(
                "La duración debe ser un valor numérico."
            ) from error_original
        
        if duracion <= 0:
            raise DatoInvalidoError(
                "La duración del servicio debe ser mayor que cero."
            )
        
        return duracion    
    
    @staticmethod
    def _aplicar_ajustes(subtotal, impuesto=0, descuento=0):
        """
        Aplica ajustes al subtotal del servicio.
        """
        if (
            isinstance(subtotal, bool) or
            isinstance(impuesto, bool) or
            isinstance(descuento, bool)
        ):
                
            raise CalculoCostoError(
                "El subtotal, el impuesto y el descuento deben ser valores numéricos."
            )
        
        try:
            subtotal = float(subtotal)
            impuesto = float(impuesto)
            descuento = float(descuento)
        
        except (ValueError, TypeError) as error_original:
            raise CalculoCostoError(
                "El subtotal, el impuesto y el descuento deben ser numéricos."
            ) from error_original
        
        if subtotal < 0:
            raise CalculoCostoError(
                "El subtotal no puede ser negativo."
            )

        if impuesto < 0 or impuesto > 1:
            raise CalculoCostoError(
                "El impuesto debe estar entre 0 y 1."
            )
        
        if descuento < 0 or descuento > 1:
            raise CalculoCostoError(
                "El descuento debe estar entre 0 y 1."
            )
            
        total_con_impuesto = subtotal * (1 + impuesto)
        total = total_con_impuesto * (1 - descuento)
        
        return round(total, 2)
    
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el costo total del servicio."""
        pass
    
    @abstractmethod
    def describir_servicio(self):
        """Método abstracto que deberá implementarse en todas las clases derivadas."""
        pass
    
    @abstractmethod
    def validar_parametros(self):
        """Método abstracto que deberá implementarse en todas las clases derivadas."""
        pass
    

    # Propiedades para consultar los atributos del servicio
    @property
    def nombre(self):
        """Permite consultar el nombre del servicio."""
        return self.__nombre
    
    @property
    def precio_base(self):
        """Permite consultar el precio base del servicio."""
        return self.__precio_base
    
    @property
    def disponible(self):
        """Permite consultar si el servicio está disponible."""
        return self.__disponible
    
    
    def habilitar_disponibilidad(self):
        """Habilita la disponibilidad del servicio."""
        if self.__disponible:
            raise OperacionNoPermitidaError(
                f"El servicio con código {self.codigo} ya está disponible."
            )
        
        self.__disponible = True
        logger.info(
            "Servicio con código %s fue establecido como disponible.",
            self.codigo
        )
        
    def deshabilitar_disponibilidad(self):
        """Deshabilita la disponibilidad del servicio."""
        if not self.__disponible:
            raise OperacionNoPermitidaError(
                f"El servicio con código {self.codigo} ya no está disponible."
            )
        
        self.__disponible = False
        logger.info(
            "Servicio con código %s fue establecido como no disponible.",
            self.codigo
        )
    
    def verificar_disponibilidad(self):
        """Verifica si el servicio está activo y disponible."""
        
        if not self.activo:
            raise OperacionNoPermitidaError(
                f"El servicio con código {self.codigo} no está activo."
            )
            
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio con código {self.codigo} no está disponible."
            )
    
    def mostrar_informacion(self):
        """Muestra la información del servicio."""
        estado = "Activo" if self.activo else "Inactivo"
        
        disponibilidad = (
            "Disponible" if self.__disponible 
            else "No Disponible"
            )
        
        return (
            f"Código: {self.codigo}\n"
            f"Servicio: {self.__nombre}\n"
            f"Precio Base: ${self.__precio_base:.2f}\n"
            f"Estado: {estado}\n"
            f"Disponibilidad: {disponibilidad}\n"
        )


# _______________ Clase derivada (ReservaSala)

class ReservaSala(Servicio):
    
    def __init__(self, codigo, nombre, precio_base, 
                 capacidad, tipo_sala, recargo, disponible=True):
        
        # Llamo al constructor de la clase base Servicio
        super().__init__(codigo, nombre, precio_base, disponible)
        
        # Defino los atributos específicos de la reserva de sala
        self.__capacidad = capacidad
        self.__tipo_sala = tipo_sala
        self.__recargo = recargo
        
        self.validar_parametros()
        
        logger.info(
            "Servicio de reserva de sala con código %s fue creado correctamente.",
            self.codigo
        )
        
    def validar_parametros(self):
        """
        Valida la capacidad, el tipo de sala y el recargo.
        """
        if (not isinstance(self.__capacidad, int) 
            or isinstance (self.__capacidad, bool)):
            
            raise DatoInvalidoError(
                "La capacidad de la sala debe ser un número entero."
                )
        
        if self.__capacidad <= 0:
            raise DatoInvalidoError(
                "La capacidad de la sala debe ser mayor que cero."
                )
        
        if not isinstance(self.__tipo_sala, str):
            raise DatoInvalidoError(
                "El tipo de sala debe ser una cadena de texto."
                )
            
        self.__tipo_sala = self.__tipo_sala.strip().title()
        
        if not self.__tipo_sala:
            raise DatoInvalidoError(
                "El tipo de sala no puede estar vacío."
                )
            
        if isinstance(self.__recargo, bool):
            raise DatoInvalidoError(
                "El recargo debe ser un valor numérico."
                )
        
        try:
            self.__recargo = float(self.__recargo)
            
        except (ValueError, TypeError) as error_original:
            raise DatoInvalidoError(
                "El recargo debe ser un valor numérico."
                ) from error_original
            
        if self.__recargo < 0:
            raise DatoInvalidoError(
                "El recargo no puede ser negativo."
                )
    
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """
        Calcula el costo total de la reserva de sala.
        """
        
        self.verificar_disponibilidad()
        duracion = self._validar_duracion(duracion)
        
        subtotal = (self.precio_base * duracion )+ self.__recargo
        total = self._aplicar_ajustes(subtotal, impuesto, descuento)
        
        logger.info(
            "Costo calculado para reserva de sala con código %s: "
            "Subtotal: %.2f, Impuesto: %.2f, Descuento: %.2f, Total: %.2f",
            self.codigo,
            subtotal,
            impuesto,
            descuento,
            total
        )
        
        return total
    
    def describir_servicio(self):
        """
        Devuelve la descripción de la sala.
        """
        return (
            f"Reserva de Sala: {self.nombre}\n"
            f"Capacidad: {self.__capacidad} personas\n"
            f"Tipo de Sala: {self.__tipo_sala}\n"
            f"Recargo: ${self.__recargo:.2f}\n"
        )


# ________________ Clase derivada (AlquilerEquipo)

class AlquilerEquipo(Servicio):
    """ 
    Representa el servicio de alquiler de equipos. 
    """
    
    def __init__(self, codigo, nombre, precio_base, 
                 tipo_equipo, cantidad, deposito, disponible=True):
        
        # Llamo al constructor de la clase base Servicio
        super().__init__(codigo, nombre, precio_base, disponible)
        
        # Defino los atributos específicos del alquiler de equipo
        self.__tipo_equipo = tipo_equipo
        self.__cantidad = cantidad
        self.__deposito = deposito
        
        self.validar_parametros()
        
        logger.info(
            "Servicio de alquiler de equipo con código %s fue creado correctamente.",
            self.codigo
        )
    
    def validar_parametros(self):
        """
        Valida el tipo de equipo, la cantidad y el depósito.
        """
        if not isinstance(self.__tipo_equipo, str):
            raise DatoInvalidoError(
                "El tipo de equipo debe ser una cadena de texto."
                )
            
        self.__tipo_equipo = self.__tipo_equipo.strip().title()
        
        if not self.__tipo_equipo:
            raise DatoInvalidoError(
                "El tipo de equipo no puede estar vacío."
                )
            
        if ( 
            not isinstance(self.__cantidad, int) 
            or isinstance(self.__cantidad, bool)
            ):
                
            raise DatoInvalidoError(
                "La cantidad de equipos debe ser un número entero."
                )        
            
        if self.__cantidad <= 0:
            raise DatoInvalidoError(
                "La cantidad de equipos debe ser mayor que cero."
                )
            
        if isinstance(self.__deposito, bool):
            raise DatoInvalidoError(
                "El depósito debe ser un valor numérico."
                )
        
        try:
            self.__deposito = float(self.__deposito)
        except (TypeError, ValueError) as error_original:
            raise DatoInvalidoError(
                "El depósito debe ser un valor numérico."
                ) from error_original
            
        if self.__deposito < 0:
            raise DatoInvalidoError(
                "El depósito no puede ser negativo."
                )
    
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        
        """
        Calcula el costo total del alquiler de equipo.
        """
        
        self.verificar_disponibilidad()
        duracion = self._validar_duracion(duracion)
        
        subtotal = (self.precio_base * duracion * self.__cantidad) + self.__deposito
        total = self._aplicar_ajustes(subtotal, impuesto, descuento)
        
        logger.info(
            "Costo calculado para alquiler de equipo con código %s: "
            "Subtotal: %.2f, Impuesto: %.2f, Descuento: %.2f, Total: %.2f",
            self.codigo,
            subtotal,
            impuesto,
            descuento,
            total
        )
        
        return total
    
    def describir_servicio(self):
        """
        Devuelve la descripción del alquiler de equipo.
        """
        return (
            f"Alquiler de Equipo: {self.nombre}\n"
            f"Tipo de Equipo: {self.__tipo_equipo}\n"
            f"Cantidad: {self.__cantidad}\n"
            f"Depósito: ${self.__deposito:.2f}\n"
        )
