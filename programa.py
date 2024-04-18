import requests
from tkinter import *
from tkinter import messagebox
from tkinter import Tk, Button
from customtkinter import *
import customtkinter
import hashlib
import string
import random
from datetime import datetime
from tkinter.simpledialog import askstring
from tkinter import filedialog
import webbrowser
from tkinter import font

class Roles:
 USUARIO = "Usuario"
 VIP = "Vip"
 ADMINISTRADOR = "Administrador"

class Utilidades:
 @staticmethod
 def encriptar_contraseña(contraseña):
 contraseña_bytes = contraseña.encode('utf-8')
 hash_obj = hashlib.sha256()
 hash_obj.update(contraseña_bytes)
 hash_hex = hash_obj.hexdigest()
 return hash_hex
 
####### -- VENTANA LOGIN -- #######

class LoginWindow:
 def __init__(self, root):
 self.root = root
 self.root.title("Inicio de Sesión")
 self.root.resizable(False, False)

 # Ancho y alto de la pantalla
 screen_width = self.root.winfo_screenwidth()
 screen_height = self.root.winfo_screenheight()

 # Coordenadas para centrar la ventana y desplazarla un poco hacia arriba
 x_coordinate = (screen_width - 400) // 2
 y_coordinate = (screen_height - 400) // 4

 # Establecer la geometría de la ventana
 self.root.geometry(f"400x400+{x_coordinate}+{y_coordinate}")

 frame = Frame(self.root, padx=20, pady=20)
 frame.pack(padx=10, pady=10)

####### -- MENU INICIO DE SESION -- #######

 # Agregar la imagen de inicio de sesión
 image = PhotoImage(file="icon.png") # Ruta de tu imagen de inicio de sesión
 self.label_image = Label(frame, image=image)
 self.label_image.grid(row=0, columnspan=2) # Esta fila ocupa dos columnas
 self.label_image.image = image # Mantener una referencia para evitar que la imagen sea eliminada por el recolector de basura

 self.label_usuario = Label(frame, text="Usuario:", padx=5, pady=5)
 self.label_usuario.grid(row=1, column=0, sticky="e")

 self.entry_usuario = Entry(frame, width=30)
 self.entry_usuario.grid(row=1, column=1)

 self.label_contraseña = Label(frame, text="Contraseña:", padx=5, pady=5)
 self.label_contraseña.grid(row=2, column=0, sticky="e")

 self.entry_contraseña = Entry(frame, show="*", width=30)
 self.entry_contraseña.grid(row=2, column=1)

 self.btn_iniciar_sesion = Button(self.root, text="Iniciar Sesión", width=15, command=self.iniciar_sesion, bg="light green", font=font.Font(weight="bold"))
 self.btn_iniciar_sesion.pack(pady=5)
 

 self.btn_registrar = Button(self.root, text="Registrar", width=15, command=self.registrar_usuario, bg="light blue", font=font.Font(weight="bold"))
 self.btn_registrar.pack(pady=5)

 self.btn_pass = Button(self.root, text="Cambiar Contraseña", width=15, command=self.cambiar_contraseña, bg="#d5303e", font=font.Font(weight="bold"))
 self.btn_pass.pack(pady=5)

####### -- FUNCION ENCRIPTAR CONTRASEÑA -- #######

 def encriptar_contraseña(self, contraseña):
 contraseña_bytes = contraseña.encode('utf-8')
 hash_obj = hashlib.sha256()
 hash_obj.update(contraseña_bytes)
 hash_hex = hash_obj.hexdigest()
 return hash_hex
 
####### -- FUNCION REGISTRAR USUARIO -- #######

 def registrar_usuario(self):
 usuario = self.entry_usuario.get()
 contraseña = self.entry_contraseña.get()
 
 # Verificar que la contraseña cumpla con ciertos criterios de seguridad
 if not self.verificar_contraseña_segura(contraseña):
 messagebox.showerror("Error", "La contraseña no es segura")
 return
 
 contraseña_encriptada = self.encriptar_contraseña(contraseña)
 
 rol_usuario = Roles.USUARIO
 
 fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
 response = requests.get("https://fearless-chain-healer.glitch.me/articles", params={"correo": usuario})
 data = response.json()
 
 if data:
 messagebox.showerror("Error", "El usuario ya existe")
 else:
 self.usuario = usuario
 payload = {"correo": usuario, "contra": contraseña_encriptada, "rol": rol_usuario, "fecha_creacion": fecha_creacion}
 response = requests.post("https://fearless-chain-healer.glitch.me/articles", json=payload)
 
 if response.ok:
 messagebox.showinfo("Registro", "Usuario registrado correctamente")
 else:
 messagebox.showerror("Error", "Hubo un error al registrar el usuario")

####### -- FUNCION CAMBIAR CONTRASEÑA -- #######

 def cambiar_contraseña(self):
 # Crear la ventana emergente para cambiar la contraseña
 cambiar_contraseña_ventana = Toplevel(self.root)
 cambiar_contraseña_ventana.title("Cambiar Contraseña")

 # Obtener el ancho y alto de la pantalla
 screen_width = cambiar_contraseña_ventana.winfo_screenwidth()
 screen_height = cambiar_contraseña_ventana.winfo_screenheight()

 # Calcular las coordenadas x e y para centrar la ventana emergente
 x_coordinate = (screen_width - cambiar_contraseña_ventana.winfo_reqwidth()) // 2
 y_coordinate = (screen_height - cambiar_contraseña_ventana.winfo_reqheight()) // 4

 # Establecer la posición de la ventana emergente
 cambiar_contraseña_ventana.geometry(f"+{x_coordinate}+{y_coordinate}")

 frame = Frame(cambiar_contraseña_ventana, padx=20, pady=20)
 frame.pack(padx=10, pady=10)

 label_usuario = Label(frame, text="Usuario:")
 label_usuario.grid(row=0, column=0, sticky="e")

 entry_usuario = Entry(frame, width=30)
 entry_usuario.grid(row=0, column=1)

 label_contraseña_actual = Label(frame, text="Contraseña actual:")
 label_contraseña_actual.grid(row=1, column=0, sticky="e")

 entry_contraseña_actual = Entry(frame, show="*", width=30)
 entry_contraseña_actual.grid(row=1, column=1)

 label_nueva_contraseña = Label(frame, text="Nueva contraseña:")
 label_nueva_contraseña.grid(row=2, column=0, sticky="e")

 entry_nueva_contraseña = Entry(frame, show="*", width=30)
 entry_nueva_contraseña.grid(row=2, column=1)

 frame_aceptar = Frame(cambiar_contraseña_ventana)
 frame_aceptar.pack(pady=10)

 def aceptar():
 usuario_actual = entry_usuario.get()
 contraseña_actual = entry_contraseña_actual.get()
 nueva_contraseña = entry_nueva_contraseña.get()

 if usuario_actual and contraseña_actual and nueva_contraseña:
 # URL de la base de datos en Glitch
 url = 'https://fearless-chain-healer.glitch.me/articles'
 
 # Hacer una solicitud GET para obtener los datos actuales
 response = requests.get(url)
 
 # Verificar si la solicitud fue exitosa
 if response.status_code == 200:
 # Obtener los datos actuales en formato JSON
 data = response.json()
 
 # Encriptar la contraseña actual para compararla con la almacenada en la base de datos
 contraseña_actual_encriptada = Utilidades.encriptar_contraseña(contraseña_actual)
 
 # Buscar el usuario en los datos
 usuario_encontrado = False
 for item in data:
 if 'correo' in item and item['correo'] == usuario_actual:
 # Verificar si la contraseña actual coincide
 if 'contra' in item and item['contra'] == contraseña_actual_encriptada:
 # Encriptar la nueva contraseña
 nueva_contraseña_encriptada = Utilidades.encriptar_contraseña(nueva_contraseña)
 
 # Actualizar la contraseña del usuario
 item['contra'] = nueva_contraseña_encriptada
 usuario_encontrado = True
 
 # Enviar una solicitud PATCH para actualizar solo este usuario
 patch_url = f"{url}/{item['id']}"
 response = requests.patch(patch_url, json=item)
 if response.status_code == 200:
 messagebox.showinfo("Éxito", "La contraseña se ha cambiado correctamente.")
 cambiar_contraseña_ventana.destroy()
 else:
 messagebox.showerror("Error", "No se pudo cambiar la contraseña. Inténtalo de nuevo.")
 break
 else:
 messagebox.showerror("Error", "La contraseña actual es incorrecta.")
 
 if not usuario_encontrado:
 messagebox.showerror("Error", f"No se encontró el usuario '{usuario_actual}'.")
 else:
 messagebox.showerror("Error", "Error al obtener los datos de la base de datos.")
 else:
 messagebox.showwarning("Advertencia", "Por favor, introduce todos los campos correctamente.")

 button_aceptar = Button(frame_aceptar, text="Aceptar", command=aceptar)
 button_aceptar.pack(side="left", padx=10)

 button_cancelar = Button(frame_aceptar, text="Cancelar", command=cambiar_contraseña_ventana.destroy)
 button_cancelar.pack(side="left", padx=10)

####### -- FUNCION VERIFICAR CONTRASEÑA SEGURA -- #######

 def verificar_contraseña_segura(self, contraseña):
 if len(contraseña) < 8:
 return False
 
 return True
 
####### -- FUNCION INICIAR SESION -- #######

 def iniciar_sesion(self):
 usuario = self.entry_usuario.get()
 contraseña = self.entry_contraseña.get()
 
 contraseña_encriptada = self.encriptar_contraseña(contraseña)
 
 response = requests.get("https://fearless-chain-healer.glitch.me/articles", params={"correo": usuario, "contra": contraseña_encriptada})
 data = response.json()
 
 if data:
 if 'rol' in data[0]:
 rol_usuario = data[0]['rol']
 nombre_usuario = usuario
 messagebox.showinfo("Inicio de sesión", f"¡Bienvenido, {usuario}!")
 self.root.destroy()
 root = Tk()
 app = MainWindow(root, rol_usuario, nombre_usuario, usuario)
 root.mainloop()
 else:
 messagebox.showerror("Error", "El rol del usuario no está disponible")
 else:
 messagebox.showerror("Error", "Usuario o contraseña incorrectos")

####### -- VENTANA MAIN -- #######

class MainWindow:
 def __init__(self, root, rol, nombre_usuario, usuario):
 self.root = root
 self.rol = rol
 self.nombre_usuario = nombre_usuario
 self.usuario = usuario
 self.root.title("Ventana Principal")

 # Ancho y alto de la pantalla
 screen_width = self.root.winfo_screenwidth()
 screen_height = self.root.winfo_screenheight()

 # Coordenadas para centrar la ventana y desplazarla un poco hacia arriba
 x_coordinate = (screen_width - 900) // 2
 y_coordinate = (screen_height - 900) // 4

 # Establecer la geometría de la ventana
 self.root.geometry(f"900x900+{x_coordinate}+{y_coordinate}")
 
 menubar = Menu(root)
 root.config(menu=menubar)

####### -- MENUS VENTANA MAIN -- #######
 
 inicio_menu = Menu(menubar, tearoff=0)
 inicio_menu.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
 menubar.add_cascade(label="Inicio", menu=inicio_menu)

 herramientas_menu = Menu(menubar, tearoff=0)
 herramientas_menu.add_command(label="Herramientas")
 menubar.add_cascade(label="Herramientas", menu=herramientas_menu)
 
 licencias_menu = Menu(menubar, tearoff=0)
 licencias_menu.add_command(label="Canjear Licencia", command=self.canjear_licencia)
 licencias_menu.add_command(label="Estado", command=self.estado_licencia)
 licencias_menu.add_command(label="Comprar Licencia", command=self.comprar_licencia)
 menubar.add_cascade(label="Licencias", menu=licencias_menu)

 ayuda_menu = Menu(menubar, tearoff=0)
 ayuda_menu.add_command(label="Sobre nosotros", command=self.abrir_perfil_github)
 ayuda_menu.add_command(label="Soporte")
 ayuda_menu.add_command(label="Manual")
 menubar.add_cascade(label="Ayuda", menu=ayuda_menu)

 perfil_menu = Menu(menubar, tearoff=0)
 perfil_menu.add_command(label="Mi Cuenta", command=lambda: self.mostrar_info_cuenta(nombre_usuario, rol))
 perfil_menu.add_command(label="Cambiar usuario", command=self.cambiar_usuario)
 perfil_menu.add_command(label="Cambiar contraseña", command=self.cambiar_contraseña)
 perfil_menu.add_command(label="Eliminar mi cuenta", command=self.eliminar_cuenta)
 menubar.add_cascade(label=nombre_usuario.capitalize(), menu=perfil_menu)

 self.crear_menu(rol, menubar)

 mensaje_bienvenida = f"Bienvenido a la ventana principal, {nombre_usuario}!"
 label = Label(root, text=mensaje_bienvenida)
 label.pack(side="bottom", padx=10, pady=10, anchor="se")
 
 frame_row1 = Frame(root)
 frame_row1.pack()

 # Configurar el ancho y alto común para todos los botones
 button_width = 28
 button_height = 4

 # Botones de la primera fila
 btn_notas = Button(frame_row1, text="Notas", bg="red", width=button_width, height=button_height)
 btn_notas.pack(side="left", padx=10, pady=10)

 btn_calculadora = Button(frame_row1, text="Calculadora", bg="red", width=button_width, height=button_height)
 btn_calculadora.pack(side="left", padx=10, pady=10)

 btn_soon1 = Button(frame_row1, text="Soon", bg="red", width=button_width, height=button_height)
 btn_soon1.pack(side="left", padx=10, pady=10)

 # Crear un marco para los botones de la segunda fila
 frame_row2 = Frame(root)
 frame_row2.pack()

 # Botones de la segunda fila
 btn_soon2 = Button(frame_row2, text="Soon", bg="red", width=button_width, height=button_height)
 btn_soon2.pack(side="left", padx=10, pady=10)

 btn_soon3 = Button(frame_row2, text="Soon", bg="red", width=button_width, height=button_height)
 btn_soon3.pack(side="left", padx=10, pady=10)

 btn_soon4 = Button(frame_row2, text="Soon", bg="red", width=button_width, height=button_height)
 btn_soon4.pack(side="left", padx=10, pady=10)

 # Crear un marco para los botones de la segunda fila
 frame_row3 = Frame(root)
 frame_row3.pack()

 # Botones de la segunda fila
 btn_soon2 = Button(frame_row3, text="Soon", bg="red", width=button_width, height=button_height)
 btn_soon2.pack(side="left", padx=10, pady=10)

 btn_soon3 = Button(frame_row3, text="Soon", bg="red", width=button_width, height=button_height)
 btn_soon3.pack(side="left", padx=10, pady=10)

 btn_soon4 = Button(frame_row3, text="Soon", bg="red", width=button_width, height=button_height)
 btn_soon4.pack(side="left", padx=10, pady=10)


####### -- FUNCION CERRAR SESION -- #######

 def cerrar_sesion(self):
 respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?")
 if respuesta:
 self.root.destroy() 
 root = Tk()
 app = LoginWindow(root)
 root.mainloop()

####### -- FUNCION MOSTRAR HERRAMIENTAS -- #######

 def mostrar_herramientas(self):
 messagebox.showinfo("Herramientas", "Aquí van las herramientas")
 
####### -- FUNCION CANJEAR LICENCIA -- #######

 def canjear_licencia(self):
 canjear_ventana = Toplevel(self.root)
 canjear_ventana.title("Canjear Licencia")
 # Dimensiones de la ventana
 ventana_ancho = 400
 ventana_alto = 200
 # Dimensiones de la pantalla
 pantalla_ancho = canjear_ventana.winfo_screenwidth()
 pantalla_alto = canjear_ventana.winfo_screenheight()
 # Calcula las coordenadas x e y para centrar la ventana en la pantalla y un poco más arriba
 x = (pantalla_ancho - ventana_ancho) // 2
 y = (pantalla_alto - ventana_alto) // 3
 # Establece la geometría de la ventana con las coordenadas centradas
 canjear_ventana.geometry(f"{ventana_ancho}x{ventana_alto}+{x}+{y}")
 
 label = Label(canjear_ventana, text="Introducir código de licencia:")
 label.pack()
 entry = Entry(canjear_ventana)
 entry.pack()
 
 frame = Frame(canjear_ventana)
 frame.pack(pady=10)
 
 def aceptar():
 codigo_licencia = entry.get()
 if codigo_licencia:
 valido, mensaje = self.validar_licencia(codigo_licencia)
 if valido:
 self.actualizar_rol_vip()
 messagebox.showinfo("Licencia Canjeada", f"La licencia {codigo_licencia} ha sido canjeada con éxito.")
 else:
 messagebox.showwarning("Error", mensaje)
 canjear_ventana.destroy()
 else:
 messagebox.showwarning("Error", "Por favor, introduzca un código de licencia válido.")
 
 def cancelar():
 canjear_ventana.destroy()
 
 button_aceptar = Button(frame, text="Aceptar", command=aceptar)
 button_aceptar.pack(side="left", padx=10)
 
 button_cancelar = Button(frame, text="Cancelar", command=cancelar)
 button_cancelar.pack(side="left", padx=10)

####### -- FUNCION ESTADO LICENCIA -- #######

 def estado_licencia(self):
 messagebox.showinfo("Estado de Licencia", "Aquí puedes ver el estado de tu licencia")

####### -- COMPRAR LICENCIA -- #######

 def comprar_licencia(self):
 messagebox.showinfo("Comprar Licencia", "Aquí puedes comprar una nueva licencia")

####### -- CAMBIAR USUARIO -- #######

 def cambiar_usuario(self):
 usuario_actual = askstring("Cambiar Usuario", "Introduce tu usuario actual:")
 nuevo_usuario = askstring("Cambiar Usuario", "Introduce el nuevo nombre de usuario:")

 if usuario_actual and nuevo_usuario:
 # URL de la base de datos en Glitch
 url = 'https://fearless-chain-healer.glitch.me/articles'
 
 # Hacer una solicitud GET para obtener los datos actuales
 response = requests.get(url)
 
 # Verificar si la solicitud fue exitosa
 if response.status_code == 200:
 # Obtener los datos actuales en formato JSON
 data = response.json()
 
 # Buscar el usuario en los datos
 usuario_encontrado = False
 for item in data:
 if 'correo' in item and item['correo'] == usuario_actual:
 # Actualizar el nombre de usuario
 item['correo'] = nuevo_usuario
 usuario_encontrado = True
 
 # Enviar una solicitud PATCH para actualizar solo este usuario
 patch_url = f"{url}/{item['id']}"
 response = requests.patch(patch_url, json=item)
 if response.status_code == 200:
 messagebox.showinfo("Éxito", "El nombre de usuario se ha actualizado correctamente.")
 
 # Cerrar sesión después de cambiar el nombre de usuario
 self.cerrar_sesion()
 else:
 messagebox.showerror("Error", "No se pudo actualizar el nombre de usuario. Inténtalo de nuevo.")
 break
 
 if not usuario_encontrado:
 messagebox.showerror("Error", f"No se encontró el usuario '{usuario_actual}'.")
 else:
 messagebox.showerror("Error", "Error al obtener los datos de la base de datos.")
 else:
 messagebox.showwarning("Advertencia", "Por favor, introduce todos los campos correctamente.")

####### -- FUNCION CAMBIAR CONTRASEÑA -- #######

 def cambiar_contraseña(self):
 cambiar_contraseña_ventana = Toplevel(self.root)
 cambiar_contraseña_ventana.title("Cambiar Contraseña")
 
 frame = Frame(cambiar_contraseña_ventana, padx=20, pady=20)
 frame.pack(padx=10, pady=10)

 label_usuario = Label(frame, text="Usuario actual:")
 label_usuario.grid(row=0, column=0, sticky="e")

 entry_usuario = Entry(frame, width=30)
 entry_usuario.grid(row=0, column=1)

 label_contraseña_actual = Label(frame, text="Contraseña actual:")
 label_contraseña_actual.grid(row=1, column=0, sticky="e")

 entry_contraseña_actual = Entry(frame, show="*", width=30)
 entry_contraseña_actual.grid(row=1, column=1)

 label_nueva_contraseña = Label(frame, text="Nueva contraseña:")
 label_nueva_contraseña.grid(row=2, column=0, sticky="e")

 entry_nueva_contraseña = Entry(frame, show="*", width=30)
 entry_nueva_contraseña.grid(row=2, column=1)

 frame_aceptar = Frame(cambiar_contraseña_ventana)
 frame_aceptar.pack(pady=10)

 def aceptar():
 usuario_actual = entry_usuario.get()
 contraseña_actual = entry_contraseña_actual.get()
 nueva_contraseña = entry_nueva_contraseña.get()

 if usuario_actual and contraseña_actual and nueva_contraseña:
 # URL de la base de datos en Glitch
 url = 'https://fearless-chain-healer.glitch.me/articles'
 
 # Hacer una solicitud GET para obtener los datos actuales
 response = requests.get(url)
 
 # Verificar si la solicitud fue exitosa
 if response.status_code == 200:
 # Obtener los datos actuales en formato JSON
 data = response.json()
 
 # Encriptar la contraseña actual para compararla con la almacenada en la base de datos
 contraseña_actual_encriptada = Utilidades.encriptar_contraseña(contraseña_actual)
 
 # Buscar el usuario en los datos
 usuario_encontrado = False
 for item in data:
 if 'correo' in item and item['correo'] == usuario_actual:
 # Verificar si la contraseña actual coincide
 if 'contra' in item and item['contra'] == contraseña_actual_encriptada:
 # Encriptar la nueva contraseña
 nueva_contraseña_encriptada = Utilidades.encriptar_contraseña(nueva_contraseña)
 
 # Actualizar la contraseña del usuario
 item['contra'] = nueva_contraseña_encriptada
 usuario_encontrado = True
 
 # Enviar una solicitud PATCH para actualizar solo este usuario
 patch_url = f"{url}/{item['id']}"
 response = requests.patch(patch_url, json=item)
 if response.status_code == 200:
 messagebox.showinfo("Éxito", "La contraseña se ha cambiado correctamente.")
 
 # Cerrar sesión después de cambiar la contraseña
 self.cerrar_sesion()
 else:
 messagebox.showerror("Error", "No se pudo cambiar la contraseña. Inténtalo de nuevo.")
 break
 else:
 messagebox.showerror("Error", "La contraseña actual es incorrecta.")
 
 if not usuario_encontrado:
 messagebox.showerror("Error", f"No se encontró el usuario '{usuario_actual}'.")
 else:
 messagebox.showerror("Error", "Error al obtener los datos de la base de datos.")
 else:
 messagebox.showwarning("Advertencia", "Por favor, introduce todos los campos correctamente.")

 button_aceptar = Button(frame_aceptar, text="Aceptar", command=aceptar)
 button_aceptar.pack(side="left", padx=10)

 button_cancelar = Button(frame_aceptar, text="Cancelar", command=cambiar_contraseña_ventana.destroy)
 button_cancelar.pack(side="left", padx=10)

####### -- FUNCION CAMBIAR ROL -- #######

 def cambiar_rol(self):
 cambiar_rol_window = Toplevel(self.root)
 cambiar_rol_window.geometry("500x400")
 cambiar_rol_window.title("Cambiar Rol de Usuario")
 
 # Definir el tamaño de la ventana
 window_width = 500
 window_height = 300
 cambiar_rol_window.geometry(f"{window_width}x{window_height}")
 
 # Calcular las coordenadas para centrar la ventana
 screen_width = self.root.winfo_screenwidth()
 screen_height = self.root.winfo_screenheight()
 x_coordinate = (screen_width - window_width) // 2
 y_coordinate = (screen_height - window_height) // 4
 
 # Establecer las coordenadas de la ventana
 cambiar_rol_window.geometry(f"+{x_coordinate}+{y_coordinate}")

 response = requests.get("https://fearless-chain-healer.glitch.me/articles")
 usuarios = [usuario['correo'] for usuario in response.json() if 'correo' in usuario]

 Label(cambiar_rol_window, text="Seleccionar usuario:").pack()
 usuario_var = StringVar(cambiar_rol_window)
 usuario_var.set(usuarios[0])
 OptionMenu(cambiar_rol_window, usuario_var, *usuarios).pack(pady=10)

 Label(cambiar_rol_window, text="Seleccionar nuevo rol:").pack()
 nuevo_rol_var = StringVar(cambiar_rol_window)
 nuevo_rol_var.set(Roles.USUARIO)
 opciones_roles = [Roles.USUARIO, Roles.VIP, Roles.ADMINISTRADOR]
 OptionMenu(cambiar_rol_window, nuevo_rol_var, *opciones_roles).pack(pady=10)

 def aplicar_cambio():
 usuario = usuario_var.get()
 nuevo_rol = nuevo_rol_var.get()
 if self.cambiar_rol_usuario(usuario, nuevo_rol):
 messagebox.showinfo("Cambio de Rol", f"Rol cambiado a {nuevo_rol} correctamente")
 cambiar_rol_window.destroy() # Cerrar la ventana después de cambiar el rol
 else:
 messagebox.showerror("Error", "No se pudo cambiar el rol")

 Button(cambiar_rol_window, text="Guardar", command=aplicar_cambio).pack(pady=10)

 def cambiar_rol_usuario(self, correo, nuevo_rol):
 try:
 # URL de la base de datos en Glitch
 url = 'https://fearless-chain-healer.glitch.me/articles'
 
 # Hacer una solicitud GET para obtener los datos actuales
 response = requests.get(url)
 
 # Verificar si la solicitud fue exitosa
 if response.status_code == 200:
 # Obtener los datos actuales en formato JSON
 data = response.json()
 
 # Buscar el usuario en los datos
 usuario_encontrado = False
 for item in data:
 if 'correo' in item and item['correo'] == correo:
 # Actualizar el rol del usuario
 item['rol'] = nuevo_rol
 usuario_encontrado = True
 
 # Enviar una solicitud PATCH para actualizar solo este usuario
 patch_url = f"{url}/{item['id']}"
 response = requests.patch(patch_url, json=item)
 if response.status_code == 200:
 print(f"Se ha actualizado el rol de '{correo}' a '{nuevo_rol}'.")
 return True
 else:
 print("Error al actualizar el rol del usuario.")
 return False
 break
 
 if not usuario_encontrado:
 print(f"No se encontró el usuario '{correo}'.")
 return False
 else:
 print("Error al obtener los datos de la base de datos.")
 return False
 except Exception as e:
 print("Error durante la solicitud PATCH:", e)
 return False
 
####### -- ELIMINAR CUENTA -- #######

 def eliminar_cuenta(self):
 if messagebox.askyesno("Eliminar Cuenta", "¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer."):
 try:
 nombre_usuario = self.nombre_usuario
 url = "https://fearless-chain-healer.glitch.me/articles"
 response = requests.get(url)
 
 if response.ok:
 data = response.json()
 
 for item in data:
 if 'correo' in item and item['correo'] == nombre_usuario:
 entry_id = item['id']
 delete_url = f"https://fearless-chain-healer.glitch.me/articles/{entry_id}"
 delete_response = requests.delete(delete_url)
 
 if delete_response.ok:
 print(f"Entrada correspondiente al usuario '{nombre_usuario}' eliminada correctamente.")
 else:
 print(f"No se pudo eliminar la entrada correspondiente al usuario '{nombre_usuario}'.")
 
 messagebox.showinfo("Cuenta Eliminada", "Tu cuenta ha sido eliminada correctamente.")
 self.root.destroy()
 else:
 messagebox.showerror("Error", "No se pudo obtener los datos de la base de datos. Inténtalo de nuevo.")
 except Exception as e:
 messagebox.showerror("Error", f"Ocurrió un error al eliminar la cuenta: {e}")

####### -- CREAR MENU -- #######

 def crear_menu(self, rol, menubar):
 if rol == Roles.ADMINISTRADOR:
 admin_menu = Menu(menubar, tearoff=0)
 admin_menu.add_command(label="Cambiar Rol", command=self.cambiar_rol)
 admin_menu.add_command(label="Generar Licencia", command=self.generar_licencia_y_enviar)
 menubar.add_cascade(label="Admin Menu", menu=admin_menu)
 elif rol == Roles.VIP:
 vip_menu = Menu(menubar, tearoff=0)
 vip_menu.add_command(label="test", command=lambda: print("Opción para usuarios VIP"))
 menubar.add_cascade(label="Vip Menu", menu=vip_menu)

####### -- LICENCIAS -- #######

 def generar_licencia_y_enviar(self):
 caracteres = string.ascii_uppercase + string.digits
 licencia = ''.join(random.choice(caracteres) for _ in range(8))

 fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

 url = "https://fearless-chain-healer.glitch.me/articles"
 
 data = {"licencia": licencia, "fecha_creacion": fecha_creacion, "administrada_por": self.usuario}
 
 response = requests.post(url, data=data)
 
 if response.status_code == 200:
 messagebox.showinfo("Licencia Creada", "La licencia ha sido creada con éxito.")
 else:
 messagebox.showinfo("Licencia Creada", "La licencia ha sido creada con éxito.")

 def validar_licencia(self, codigo_licencia):
 response = requests.get("https://fearless-chain-healer.glitch.me/articles")
 licencias = [licencia['licencia'] for licencia in response.json() if 'licencia' in licencia]
 
 if codigo_licencia in licencias:
 return True, "Licencia válida"
 else:
 return False, "Licencia no válida"

 def actualizar_rol_vip(self):
 try:
 nombre_usuario = self.nombre_usuario
 
 # URL de la base de datos en Glitch
 url = 'https://fearless-chain-healer.glitch.me/articles'
 
 # Hacer una solicitud GET para obtener los datos actuales
 response = requests.get(url)
 
 # Verificar si la solicitud fue exitosa
 if response.status_code == 200:
 # Obtener los datos actuales en formato JSON
 data = response.json()
 
 # Buscar el usuario en los datos
 usuario_encontrado = False
 for item in data:
 if 'correo' in item and item['correo'] == nombre_usuario:
 # Actualizar el rol del usuario a VIP
 item['rol'] = Roles.VIP
 usuario_encontrado = True
 
 # Enviar una solicitud PATCH para actualizar solo este usuario
 patch_url = f"{url}/{item['id']}"
 response = requests.patch(patch_url, json=item)
 if response.status_code == 200:
 messagebox.showinfo("Actualización de Rol", "Tu rol ha sido actualizado a VIP.")
 else:
 messagebox.showerror("Error", "No se pudo actualizar tu rol. Inténtalo de nuevo.")
 break
 
 if not usuario_encontrado:
 messagebox.showerror("Error", f"No se encontró el usuario '{nombre_usuario}'.")
 else:
 messagebox.showerror("Error", "Error al obtener los datos de la base de datos.")
 except Exception as e:
 messagebox.showerror("Error", f"Ocurrió un error al actualizar el rol: {e}")


####### -- PERFIL -- #######

 def mostrar_info_cuenta(self, nombre_usuario, rol):
 ventana_info_cuenta = Toplevel(self.root)
 ventana_info_cuenta.title("Información de la Cuenta")
 ventana_info_cuenta.geometry("400x200")
 
 label_style = {'font': ('Arial', 12)}
 
 frame = Frame(ventana_info_cuenta)
 frame.pack(padx=10, pady=10)
 
 Label(frame, text="Información de la Cuenta", **label_style).grid(row=0, column=0, columnspan=2, pady=5)
 Label(frame, text="Nombre de usuario:", **label_style).grid(row=1, column=0, sticky='w')
 Label(frame, text=nombre_usuario, **label_style).grid(row=1, column=1, sticky='w')
 Label(frame, text="Rol:", **label_style).grid(row=2, column=0, sticky='w')
 Label(frame, text=rol, **label_style).grid(row=2, column=1, sticky='w')
 
 def cargar_foto_perfil():
 filename = filedialog.askopenfilename(title="Seleccionar Foto de Perfil", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
 if filename:
 Label(frame, text=f"Foto de Perfil: {filename}", **label_style).grid(row=3, column=0, columnspan=2, pady=5)

 cargar_foto_button = Button(frame, text="Cargar Foto de Perfil", command=cargar_foto_perfil)
 cargar_foto_button.grid(row=4, column=0, columnspan=2, pady=5)
 
 close_button = Button(ventana_info_cuenta, text="Cerrar", command=ventana_info_cuenta.destroy)
 close_button.pack(pady=5)
 
 # Botón de cerrar
 close_button = Button(ventana_info_cuenta, text="Cerrar", command=ventana_info_cuenta.destroy)
 close_button.pack(pady=5)


####### -- GITHUB -- #######

 def abrir_perfil_github(self):
 webbrowser.open("https://github.com/ivanviidaal")
 

root = Tk()
app = LoginWindow(root)
root.mainloop()
