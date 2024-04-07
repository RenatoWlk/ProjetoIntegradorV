import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk

# CORES
cinza_escuro = '#222831'
cinza = '#393E46'
amarelo = '#FFD369'
branco = '#EEEEEE'

#Criando a janela
w = tk.Tk()
title = "Monitoramento do estacionamento"
w.title(title)

#Dimensões da janela
width = 1200
height = 900
w.geometry(f"{width}x{height}")

# Função para criar um Frame com borda
def criar_frame_com_borda(parent, width, height, x, y, text):
    frame = tk.Frame(parent, width=width, height=height, highlightthickness=6, highlightbackground=amarelo, border=None)
    frame.place(x=x, y=y)  # Posicionando o Frame
    label = tk.Label(frame, text=text, width=width, height=height, border=None, relief="solid", bg=cinza, fg=branco, font=("Arial", 12))
    label.pack()  # Usando pack() para posicionar o Label dentro do Frame

# ÁREA DA RELAÇÃO DE CARROS E VAGAS LIVRES
criar_frame_com_borda(w, 48, 10, 50, 50, "Área de relação carros e vagas")

# ÁREA DE LOGS DE REGISTROS
criar_frame_com_borda(w, 48, 10, 650, 50, "Logs de Registros de movimentação no estacionamento")

# ÁREA DO VÍDEO DE MONITORAMENTO DO ESTACIONAMENTO

criar_frame_com_borda(w, 115, 30, 50, 300, "Área do vídeo")
w.configure(background=cinza_escuro)





w.mainloop()
