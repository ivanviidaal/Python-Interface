from tkinter import *
from tkinter import messagebox
import sqlite3
import hashlib
import pyperclip
import main

# Función para encriptar contraseñas
def encriptar_contraseña(contraseña):
    # Convertir la contraseña a bytes
    contraseña_bytes = contraseña.encode('utf-8')

    # Crear un objeto hash con el algoritmo SHA-256
    hash_obj = hashlib.sha256()

    # Actualizar el objeto hash con la contraseña
    hash_obj.update(contraseña_bytes)

    # Obtener el hash en formato hexadecimal
    hash_hex = hash_obj.hexdigest()

    return hash_hex

# Crear o conectar a la base de datos
miConexion = sqlite3.connect('miprograma.db')
miCursor = miConexion.cursor()

# Crear tabla usuarios si no existe
miCursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        contraseña TEXT
    )
''')

def recuperar_usuario():
    contraseña = entry_contraseña.get()
    if contraseña:
        miCursor.execute("SELECT usuario FROM usuarios WHERE contraseña = ?", (encriptar_contraseña(contraseña),))
        usuario_recuperado = miCursor.fetchone()
        
        if usuario_recuperado:
            usuario = usuario_recuperado[0]
            messagebox.showinfo("Usuario recuperado", f"El usuario asociado a esta contraseña es: {usuario}")
            pyperclip.copy(usuario)  # Copiar el usuario al portapapeles
            entry_contraseña.delete(0, END)  # Limpiar el campo de entrada de contraseña después de mostrar el usuario
        else:
            messagebox.showerror("Error", "La contraseña no coincide con ningún usuario")
    else:
        messagebox.showerror("Error", "Por favor, ingresa tu contraseña")

def registrar_usuario():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    
    # Encriptar la contraseña
    contraseña_encriptada = encriptar_contraseña(contraseña)
    
    try:
        miCursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)", (usuario, contraseña_encriptada))
        miConexion.commit()
        messagebox.showinfo("Registro", "Usuario registrado correctamente")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El usuario ya existe")

def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    
    # Encriptar la contraseña ingresada para compararla con la almacenada
    contraseña_encriptada = encriptar_contraseña(contraseña)
    
    miCursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña_encriptada))
    usuario_encontrado = miCursor.fetchone()
    
    if usuario_encontrado:
        messagebox.showinfo("Inicio de sesión", "¡Bienvenido, {}!".format(usuario))
        root_inicio.destroy()  # Destruir la ventana de inicio de sesión
        main.main()  # Abrir la ventana principal desde main.py
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

root_inicio = Tk()
root_inicio.title("Inicio de Sesión")
root_inicio.geometry("400x300")

# Widgets para la ventana de inicio de sesión
frame = Frame(root_inicio, padx=20, pady=20)
frame.pack(padx=10, pady=10)

label_usuario = Label(frame, text="Usuario:", padx=5, pady=5)
label_usuario.grid(row=0, column=0, sticky="e")

entry_usuario = Entry(frame, width=30)
entry_usuario.grid(row=0, column=1)

label_contraseña = Label(frame, text="Contraseña:", padx=5, pady=5)
label_contraseña.grid(row=1, column=0, sticky="e")

entry_contraseña = Entry(frame, show="*", width=30)
entry_contraseña.grid(row=1, column=1)

btn_iniciar_sesion = Button(root_inicio, text="Iniciar Sesión", width=15, command=iniciar_sesion)
btn_iniciar_sesion.pack(pady=5)

btn_registrar = Button(root_inicio, text="Registrar", width=15, command=registrar_usuario)
btn_registrar.pack(pady=5)

btn_recuperar_usuario = Button(root_inicio, text="Recuperar usuario", width=20, command=recuperar_usuario)
btn_recuperar_usuario.pack(pady=5)

root_inicio.mainloop()
