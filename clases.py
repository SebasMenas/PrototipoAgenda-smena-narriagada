#clase/objeto para manejar las citas de manera mas controlada
class ControlCitas:
    def __init__(self):
        #uso de listas temporal
        self.citas = []
        self.usuarios = []

    def AgregarCita(self,_cita):        
        self.citas.append(_cita)

    def CancelarCita(self,_idCita):
        self.citas[_idCita].cancelar()

    def getUsuarioDatos(self,_idCita):
        id_usr = self.citas[_idCita].getUsuario()
        self.usuarios[id_usr].getDatos()
    
#clase de datos de usuarios registrados

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

        
        

    
class Cita:
    _contador_id = 1  # variable de clase para autoincremento

    def __init__(self, anio, mes, dia, usuario_id, docente, asunto):
        # Validar asunto
        if len(asunto) > 200:
            raise ValueError("El asunto no puede superar los 200 caracteres")

        # Validación simple de fecha
        if not (1 <= mes <= 12):
            raise ValueError("Mes inválido")
        if not (1 <= dia <= 31):
            raise ValueError("Día inválido")

        self.id = Cita._contador_id
        Cita._contador_id += 1

        self.anio = anio
        self.mes = mes
        self.dia = dia
        self.usuario_id = usuario_id
        self.docente = docente
        self.asunto = asunto
        self.estado = 1 #0 = cancelado, 1 = activo, 2 = ausente, 3 = concluida

    def cancelar(self):
        self.estado = 0

    def getUsuario(self):
        return self.usuario_id

    def __repr__(self):
        return (f"Cita(id={self.id}, fecha={self.dia}/{self.mes}/{self.anio}, "
                f"usuario={self.usuario_id}, docente='{self.docente}', asunto='{self.asunto}')")


# Lista donde se almacenan las citas
lista_citas = []


# Función para agregar citas a la lista
def agregar_cita(lista, anio, mes, dia, usuario_id, docente, asunto):
    cita = Cita(anio, mes, dia, usuario_id, docente, asunto)
    lista.append(cita)
    return cita


# Ejemplo de uso
c1 = agregar_cita(lista_citas, 2026, 4, 11, 101, "Dr. Pérez", "Consulta general")
c2 = agregar_cita(lista_citas, 2026, 4, 12, 102, "Dra. López", "Revisión médica")

print(lista_citas)