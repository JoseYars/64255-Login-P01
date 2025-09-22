# login_app.py

import tkinter as tk
from tkinter import messagebox
import hashlib # Importar para hashear
from utils.saveJson import cargar_diccionario, guardar_diccionario

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login Seguro")
        self.root.geometry("400x350")
        self.root.configure(bg='#f0f0f0')
        
        self.db_file = "users-db.json"
        self.users = cargar_diccionario(self.db_file)
        
        self.create_widgets()
    
    def hash_password(self, password):
        """Paso 3: Hashea la contraseña usando SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def create_widgets(self):
        # (The widget creation code remains the same as the original)
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        title_label = tk.Label(
            main_frame, text="Inicio de Sesión (Con Hash)", 
            font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#333333'
        )
        title_label.pack(pady=(0, 30))
        
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)
        
        user_label = tk.Label(
            input_frame, text="Usuario:", font=('Arial', 12),
            bg='#f0f0f0', anchor='w', width=15
        )
        user_label.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        self.user_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.user_entry.grid(row=0, column=1, padx=5, pady=10)
        self.user_entry.focus()
        
        pass_label = tk.Label(
            input_frame, text="Contraseña:", font=('Arial', 12),
            bg='#f0f0f0', anchor='w', width=15
        )
        pass_label.grid(row=1, column=0, padx=5, pady=10, sticky='w')
        
        self.pass_entry = tk.Entry(input_frame, font=('Arial', 12), width=20, show='*')
        self.pass_entry.grid(row=1, column=1, padx=5, pady=10)
        self.pass_entry.bind('<Return>', lambda event: self.login())
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(
            button_frame, text="Iniciar Sesión", font=('Arial', 12, 'bold'),
            bg='#4CAF50', fg='white', width=12, command=self.login
        )
        
        sigin_btn = tk.Button(
            button_frame, text="Registrarse", font=('Arial', 12, 'bold'),
            bg="#4C65AF", fg='white', width=12, command=self.signin
        )
        
        login_btn.pack(pady=5)
        sigin_btn.pack(pady=1)
        
        clear_btn = tk.Button(
            button_frame, text="Limpiar", font=('Arial', 10),
            bg='#f44336', fg='white', width=10, command=self.clear_fields
        )
        clear_btn.pack(pady=5)
        
    def signin(self):
        """Guarda un nuevo usuario con contraseña hasheada."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error de Registro", "El usuario y la contraseña no pueden estar vacíos.")
            return

        self.users = cargar_diccionario(self.db_file)

        if username in self.users:
            messagebox.showerror("Error de Registro", "El nombre de usuario ya existe.")
            return
        
        # Hashear la contraseña antes de guardarla
        hashed_password = self.hash_password(password)
        self.users[username] = hashed_password
        
        if guardar_diccionario(self.users, self.db_file):
            messagebox.showinfo("Registro Exitoso", f"Usuario '{username}' registrado de forma segura.")
            self.clear_fields()
        else:
            messagebox.showerror("Error de Registro", "No se pudo guardar el nuevo usuario.")

    def login(self):
        """Paso 4: Verifica las credenciales usando el hash."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return
            
        self.users = cargar_diccionario(self.db_file)
        
        # Hashear la contraseña ingresada para compararla
        hashed_input_password = self.hash_password(password)
        
        stored_password_hash = self.users.get(username)
        
        if stored_password_hash and stored_password_hash == hashed_input_password:
            messagebox.showinfo("Éxito", f"¡Bienvenido, {username}!")
            self.open_dashboard(username)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    
    def clear_fields(self):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.user_entry.focus()
    
    def open_dashboard(self, username):
        self.root.destroy()
        dashboard = tk.Tk()
        dashboard.title("Dashboard Principal")
        dashboard.geometry("600x400")
        dashboard.configure(bg='#ffffff')
        welcome_label = tk.Label(
            dashboard, text=f"Bienvenido al Sistema, {username}!",
            font=('Arial', 16, 'bold'), bg='#ffffff', fg='#333333'
        )
        welcome_label.pack(pady=50)
        logout_btn = tk.Button(
            dashboard, text="Cerrar Sesión", font=('Arial', 12),
            bg='#ff9800', fg='white', command=dashboard.quit
        )
        logout_btn.pack(pady=20)
        dashboard.mainloop()

def main():
    root = tk.Tk()
    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()