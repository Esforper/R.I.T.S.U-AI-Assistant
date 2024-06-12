# main.py

import tkinter as tk
from AppInterface import AppInterface

# Ana uygulama penceresi oluşturma
root = tk.Tk()

# Arayüzü başlatma
app = AppInterface(root)

# Ana döngüyü başlatma
root.mainloop()
