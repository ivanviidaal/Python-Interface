import requests
from tkinter import *
from tkinter import messagebox
import hashlib
import string
import random
from datetime import datetime
from tkinter.simpledialog import askstring
from tkinter import filedialog

class Roles:
    USUARIO = "Usuario"
    VIP = "Vip"
    ADMINISTRADOR = "Administrador"

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.usuario = None

        frame = Frame(self.root, padx=20, pady=20)
        frame.pack(padx=10, pady=10)

        image = PhotoImage(file="programa/icon.png")
        self.label_image = Label(frame, image=image)
        self.label_image.grid(row=0, columnspan=2)
        self.label_image.image = image

        self.label_usuario = Label(frame, text="Usuario:", padx=5, pady=5)
        self.label_usuario.grid(row=1, column=0, sticky="e")

        self.entry_usuario = Entry(frame, width=30)
        self.entry_usuario.grid(row=1, column=1)

        self.label_contraseña = Label(frame, text="Contraseña:", padx=5, pady=5)
        self.label_contraseña.grid(row=2, column=0, sticky="e")

        self.entry_contraseña = Entry(frame, show="*", width=30)
        self.entry_contraseña.grid(row=2, column=1)

        self.btn_iniciar_sesion = Button(self.root, text="Iniciar Sesión", width=15, command=self.iniciar_sesion)
        self.btn_iniciar_sesion.pack(pady=5)

        self.btn_registrar = Button(self.root, text="Registrar", width=15, command=self.registrar_usuario)
        self.btn_registrar.pack(pady=5)

    def encriptar_contraseña(self, contraseña):
        contraseña_bytes = contraseña.encode('utf-8')
        hash_obj = hashlib.sha256()
        hash_obj.update(contraseña_bytes)
        hash_hex = hash_obj.hexdigest()
        return hash_hex

    def registrar_usuario(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        
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


class MainWindow:
    def __init__(self, root, rol, nombre_usuario, usuario):
        self.root = root
        self.rol = rol
        self.nombre_usuario = nombre_usuario
        self.usuario = usuario
        self.root.title("Ventana Principal")
        self.root.geometry("900x900")
        
        menubar = Menu(root)
        root.config(menu=menubar)
        
        inicio_menu = Menu(menubar, tearoff=0)
        inicio_menu.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menubar.add_cascade(label="Inicio", menu=inicio_menu)

        herramientas_menu = Menu(menubar, tearoff=0)
        herramientas_menu.add_command(label="Herramientas", command=self.mostrar_herramientas)
        menubar.add_cascade(label="Herramientas", menu=herramientas_menu)
        
        licencias_menu = Menu(menubar, tearoff=0)
        licencias_menu.add_command(label="Canjear Licencia", command=self.canjear_licencia)
        licencias_menu.add_command(label="Estado", command=self.estado_licencia)
        licencias_menu.add_command(label="Comprar Licencia", command=self.comprar_licencia)
        menubar.add_cascade(label="Licencias", menu=licencias_menu)

        ayuda_menu = Menu(menubar, tearoff=0)
        ayuda_menu.add_command(label="Sobre nosotros")
        ayuda_menu.add_command(label="Soporte")
        ayuda_menu.add_command(label="Manual")
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)

        perfil_menu = Menu(menubar, tearoff=0)
        perfil_menu.add_command(label="Mi Cuenta", command=lambda: self.mostrar_info_cuenta(nombre_usuario, rol))
        perfil_menu.add_command(label="Cambiar usuario", command=self.cambiar_usuario)
        perfil_menu.add_command(label="Cambiar contraseña")
        perfil_menu.add_command(label="Eliminar mi cuenta", command=self.eliminar_cuenta)
        menubar.add_cascade(label=nombre_usuario.capitalize(), menu=perfil_menu)
        

        self.crear_menu(rol, menubar)

        mensaje_bienvenida = f"Bienvenido a la ventana principal, {nombre_usuario}!"
        label = Label(root, text=mensaje_bienvenida)
        label.pack(side="bottom", padx=10, pady=10, anchor="se")

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?")
        if respuesta:
            self.root.destroy() 
            root = Tk()
            app = LoginWindow(root)
            root.mainloop()

    def mostrar_herramientas(self):
        messagebox.showinfo("Herramientas", "Aquí van las herramientas")

    def canjear_licencia(self):
        canjear_ventana = Toplevel(self.root)
        canjear_ventana.title("Canjear Licencia")
        canjear_ventana.geometry("400x200")
        
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

    def estado_licencia(self):
        messagebox.showinfo("Estado de Licencia", "Aquí puedes ver el estado de tu licencia")

    def comprar_licencia(self):
        messagebox.showinfo("Comprar Licencia", "Aquí puedes comprar una nueva licencia")

    def cambiar_usuario(self):
        usuario_actual = askstring("Cambiar Usuario", "Introduce tu usuario actual:")
        nuevo_usuario = askstring("Cambiar Usuario", "Introduce el nuevo nombre de usuario:")

        if usuario_actual and nuevo_usuario:
            url = "https://fearless-chain-healer.glitch.me/articles/update"
            payload = {"usuario_actual": usuario_actual, "nuevo_usuario": nuevo_usuario}
            response = requests.put(url, json=payload)

            if response.ok:
                messagebox.showinfo("Éxito", "El nombre de usuario se ha actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el nombre de usuario. Inténtalo de nuevo.")
        else:
             messagebox.showwarning("Advertencia", "Por favor, introduce todos los campos correctamente.")

    def cambiar_rol(self):
        cambiar_rol_window = Toplevel(self.root)
        cambiar_rol_window.title("Cambiar Rol de Usuario")

        response = requests.get("https://fearless-chain-healer.glitch.me/articles")
        usuarios = [usuario['correo'] for usuario in response.json()]

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
            else:
                messagebox.showerror("Error", "No se pudo cambiar el rol")

        Button(cambiar_rol_window, text="Guardar", command=aplicar_cambio).pack(pady=10)

    def cambiar_rol_usuario(self, correo, nuevo_rol):
        try:
            payload = {"rol": nuevo_rol}
            response = requests.put(f"https://fearless-chain-healer.glitch.me/articles/{correo}", json=payload)
            
            if response.ok:
                return True
            else:
                print("Error al actualizar el rol del usuario:", response.text)
                return False
        except Exception as e:
            print("Error durante la solicitud PUT:", e)
            return False

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

    def crear_menu(self, rol, menubar):
        if rol == Roles.ADMINISTRADOR:
            admin_menu = Menu(menubar, tearoff=0)
            admin_menu.add_command(label="Cambiar Rol", command=self.cambiar_rol)
            admin_menu.add_command(label="Generar Licencia", command=self.generar_licencia_y_enviar)
            menubar.add_cascade(label="Admin", menu=admin_menu)
        elif rol == Roles.VIP:
            vip_menu = Menu(menubar, tearoff=0)
            vip_menu.add_command(label="test", command=lambda: print("Opción para usuarios VIP"))
            menubar.add_cascade(label="Vip", menu=vip_menu)

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
            
            url = f"https://fearless-chain-healer.glitch.me/articles/{nombre_usuario}"
            payload = {"rol": Roles.VIP}
            response = requests.put(url, json=payload)
            
            if response.ok:
                messagebox.showinfo("Actualización de Rol", "Tu rol ha sido actualizado a VIP.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar tu rol. Inténtalo de nuevo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar el rol: {e}")

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


# Ejecutar la aplicación
root = Tk()
app = LoginWindow(root)
root.mainloop()
