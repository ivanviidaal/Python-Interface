from tkinter import *

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal")
        self.root.geometry("900x900")
        
        label = Label(root, text="¡Bienvenido a la ventana principal!")
        label.pack(pady=50)

def main():
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
