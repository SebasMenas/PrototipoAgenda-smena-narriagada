from datetime import datetime

#clase/objeto para manejar las citas de manera mas controlada
class ControlCitas:
    def __init__(self):
        #uso de listas temporal
        self.citas = []
        self.usuarios = []

    def AgregarCita(self,_cita):        
        self.citas.append(_cita)

    def EditarFechaCita(self,_idCita,_anio, _mes, _dia, _hora, _minutos):
        self.citas[_idCita].setFecha(_anio, _mes, _dia, _hora, _minutos)

    def CancelarCita(self,_idCita):
        self.citas[_idCita].cancelar()

    def getUsuarioDatos(self,_idCita):
        id_usr = self.citas[_idCita].getUsuario()
        self.usuarios[id_usr].getDatos()
    
#Clase de datos de usuarios registrados
class Usuario:
    def __init__(self,_n,_a,_r,_s,_k):
        self.id = 0
        self.nombre = _n
        self.apellidos = _a
        self.rut = _r
        self.sexo = _s
        self.test = _k

    def getDatos(self,id=0):
        res = [self.nombre, self.apellidos, self.rut, self.sexo]    
        if id == 1:
            res.append(self.id)
        return res
    
    def getTipos():
        pass

    def editDatos():
        pass

    def getDatos(self):
        pass

    
class Cita:
    _contador_id = 1  # variable de clase para autoincremento

    def __init__(self, _anio, _mes, _dia, _hora, _minutos, _usuario_id, _docente, _asunto):
        # Validar asunto
        if len(_asunto) > 200:
            raise ValueError("El asunto no puede superar los 200 caracteres")

        # ID autoincremental
        self.id = Cita._contador_id
        Cita._contador_id += 1

        self.fecha = datetime(_anio, _mes, _dia, _hora, _minutos)

        self.usuario_id = _usuario_id
        self.docente = _docente
        self.asunto = _asunto
        self.estado = 1  # 0=cancelado, 1=activo, 2=ausente, 3=concluida

    #-----Metodos-----

    def cancelar(self):
        self.estado = 0

    def getUsuario(self):
        return self.usuario_id
    
    def setFecha(self,_anio, _mes, _dia, _hora, _minutos):
        self.fecha = datetime(_anio, _mes, _dia, _hora, _minutos)

    def __repr__(self):
        return (f"Cita(id={self.id}, fecha={self.fecha}, "
                f"usuario={self.usuario_id}, docente='{self.docente}', asunto='{self.asunto}')")


# Lista donde se almacenan las citas
lista_citas = []


# Función para agregar citas a la lista
def agregar_cita(lista, anio, mes, dia, hora, minutos, usuario_id, docente, asunto):
    cita = Cita(anio, mes, dia, hora, minutos, usuario_id, docente, asunto)
    lista.append(cita)
    return cita


# Ejemplo de uso
c1 = agregar_cita(lista_citas, 2026, 4, 11, 11,11,11, "Dr. Pérez", "Consulta general")
c2 = agregar_cita(lista_citas, 2026, 4, 12, 12,11,11, "Dra. López", "Revisión médica")

print(lista_citas)