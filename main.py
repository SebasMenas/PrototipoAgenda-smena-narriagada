import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QStackedWidget, QLabel, 
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt

from test_db import inicializar_db, validar_credenciales # Importación de la base de datos
from testListaDocentes import ListaDocentesWidget # Importación lista docentes

# Importación de los formularios desarrollados
from testFormDocente import FormularioDocente
from Forms.testFormCita import Formulario as FormularioCita
from Forms.testFormUsr import FormularioUser as FormUser
from Views.viewCitas import ViewCitas as VCitas

class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario_activo):
        super().__init__()
        self.usuario = usuario_activo
        self.setWindowTitle(f"Sistema de Gestión de Citas - {self.usuario.nombre} ({self.usuario.rol})")
        self.setMinimumSize(800, 600)

        # Widget central y layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Sidebar
        self.sidebar = QVBoxLayout()
        self.sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.sidebar, 1) # Proporción 1

        # area de contenido dinamico
        self.content_area = QStackedWidget()
        self.main_layout.addWidget(self.content_area, 4)

        self.inicializar_paginas()
        self.inicializar_menu()

    def inicializar_paginas(self):
        # Índice 0: Pantalla de Inicio
        self.pag_inicio = QLabel(f"Bienvenido(a), {self.usuario.nombre} {self.usuario.apellidos}.\n\nSeleccione una opción en el menú lateral.")
        self.pag_inicio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pag_inicio.setStyleSheet("font-size: 18px; color: #333;")
        self.content_area.addWidget(self.pag_inicio)

        # Índice 1: Formulario de Registro de Docentes
        self.form_docente = FormularioDocente()
        self.content_area.addWidget(self.form_docente)

        # Índice 2: Formulario de Agendamiento de Citas
        self.form_cita = FormularioCita()
        self.content_area.addWidget(self.form_cita)

        # Índice 3: Nueva vista de lista de docentes
        self.lista_docentes = ListaDocentesWidget()
        self.content_area.addWidget(self.lista_docentes)
        
        # Indice 4: Formulario Agregar Usuario
        self.form_usr = FormUser()
        self.content_area.addWidget(self.form_usr)

        self.view_cita = VCitas()
        self.content_area.addWidget(self.view_cita)

    def inicializar_menu(self):
        lbl_menu = QLabel("MENÚ PRINCIPAL")
        lbl_menu.setStyleSheet("font-weight: bold; font-size: 14px; padding-bottom: 10px;")
        self.sidebar.addWidget(lbl_menu)

        # Boton general para todos los roles
        btn_inicio = QPushButton("Inicio")
        btn_inicio.clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.sidebar.addWidget(btn_inicio)

        # Logica de distribución de opciones según el ROL
        rol = self.usuario.rol.upper()

        if rol == "ADMIN":
            btn_add_docente = QPushButton("Registrar Docente")
            btn_add_docente.clicked.connect(lambda: self.content_area.setCurrentIndex(1))
            self.sidebar.addWidget(btn_add_docente)

            btn_agendar = QPushButton("Agendar Cita")
            btn_agendar.clicked.connect(lambda: self.content_area.setCurrentIndex(2))
            self.sidebar.addWidget(btn_agendar)

            btn_ver_docentes = QPushButton("Ver Docentes")
            btn_ver_docentes.clicked.connect(self.cambiar_a_lista_docentes)
            self.sidebar.addWidget(btn_ver_docentes)

            btn_AgUsr = QPushButton("Agregar Usuario")
            btn_AgUsr.clicked.connect(lambda: self.content_area.setCurrentIndex(4))
            self.sidebar.addWidget(btn_AgUsr)

            btn_citas = QPushButton("Ver Citas")
            btn_citas.clicked.connect(lambda: self.content_area.setCurrentIndex(5))
            self.sidebar.addWidget(btn_citas)
            

        elif rol == "PACIENTE":
            btn_agendar = QPushButton("Agendar Cita")
            btn_agendar.clicked.connect(lambda: self.content_area.setCurrentIndex(2))
            self.sidebar.addWidget(btn_agendar)

        elif rol in ["DOCENTE", "DOCTOR"]:
            lbl_info = QLabel("\n(Módulo de revisión de agenda\nen construcción)")
            lbl_info.setStyleSheet("color: gray; font-size: 11px;")
            self.sidebar.addWidget(lbl_info)

        self.sidebar.addStretch()

    def cambiar_a_lista_docentes(self):
        self.lista_docentes.actualizar_tabla()
        self.content_area.setCurrentIndex(3)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Citas - Acceso")
        self.setFixedSize(320, 200)
        self.inicializar_ui()

    def inicializar_ui(self):
        layout = QVBoxLayout()

        self.lbl_titulo = QLabel("SISTEMA DE GESTIÓN DE CITAS")
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titulo.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.lbl_titulo)

        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Nombre de usuario")
        layout.addWidget(self.txt_usuario)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Contraseña")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.txt_password)

        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.clicked.connect(self.procesar_login)
        layout.addWidget(self.btn_login)
        
        self.txt_usuario.returnPressed.connect(self.procesar_login)
        self.txt_password.returnPressed.connect(self.procesar_login)
        
        self.setLayout(layout)

    def procesar_login(self):
        usuario = self.txt_usuario.text().strip()
        password = self.txt_password.text().strip()

        if not usuario or not password:
            QMessageBox.warning(self, "Error de validación", "Debe proveer usuario y contraseña.")
            return

        usuario_activo = validar_credenciales(usuario, password)

        if usuario_activo:
            self.main_window = VentanaPrincipal(usuario_activo)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Acceso Denegado", "Las credenciales ingresadas no son válidas.")
            self.txt_password.clear()

if __name__ == "__main__":
    inicializar_db()
    app = QApplication(sys.argv)
    ventana_login = LoginWindow()
    ventana_login.show()
    sys.exit(app.exec())