import cv2
import tkinter as tk
from tkinter import filedialog
import threading
import mediapipe as mp
from PIL import Image, ImageTk
import pygame
import time

# Inicializa o módulo de detecção de pose do mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Inicializa o pygame para áudio
pygame.mixer.init()

# Carrega o som de alarme (substitua com o seu som de escolha)
alarm_sound = pygame.mixer.Sound("alarme.wav")

# Variáveis globais
video_path = None
is_playing = False
last_alarm_time = 0  # Manter o controle do tempo da última reprodução do som
alarm_thread = None  # Thread para controlar a reprodução do alarme sonoro

# Função para tocar o alarme sonoro em uma thread separada
def play_alarm():
    global last_alarm_time
    alarm_sound.play()
    last_alarm_time = time.time()

def play_video_thread():
    global video_path, is_playing, alarm_thread
    video_path = filedialog.askopenfilename()
    if video_path:
        is_playing = True
        video = cv2.VideoCapture(video_path)
        
        while is_playing:
            ret, frame = video.read()
            if not ret:
                break
            
            # Converte o frame em formato adequado para exibição no Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_pil.thumbnail((640, 480))  # Reduz o tamanho da imagem
            frame_tk = ImageTk.PhotoImage(image=frame_pil)
            
            # Atualiza a imagem na janela Tkinter
            video_label.config(image=frame_tk)
            video_label.image = frame_tk
            
            # Detecta a pose no frame
            results = pose.process(frame)
            landmarks = results.pose_landmarks
            
            if landmarks:
                x, y, w, h = 0, 0, frame.shape[1], frame.shape[0]
                cabeca = landmarks.landmark[0].y * h
                joelho = landmarks.landmark[26].y * h
                diferenca = joelho - cabeca
                if diferenca <= 0:
                    history_text.config(state=tk.NORMAL)
                    history_text.insert(tk.END, 'QUEDA DETECTADA\n')
                    history_text.see(tk.END)
                    history_text.config(state=tk.DISABLED)
                    
                    # Verifica o tempo desde a última reprodução do som
                    current_time = time.time()
                    if current_time - last_alarm_time >= 1.5:  # Intervalo de 1,5 segundos
                        # Inicia uma nova thread para tocar o alarme sonoro
                        if alarm_thread is None or not alarm_thread.is_alive():
                            alarm_thread = threading.Thread(target=play_alarm)
                            alarm_thread.start()
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        
        video.release()
        cv2.destroyAllWindows()
        is_playing = False

def stop_video():
    global is_playing
    is_playing = False

def start_play_thread():
    play_thread = threading.Thread(target=play_video_thread)
    play_thread.start()

def upload_video():
    global is_playing
    if is_playing:
        stop_video()
    start_play_thread()

def clear_history():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)  # Remove todo o conteúdo
    history_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Detecção de Queda")

upload_button = tk.Button(root, text="Upload Video", command=upload_video)
upload_button.pack()

play_button = tk.Button(root, text="Play", command=start_play_thread)
play_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_video)
stop_button.pack()

clear_button = tk.Button(root, text="Limpar Histórico", command=clear_history)
clear_button.pack()

# Janela para exibir o vídeo
video_label = tk.Label(root)
video_label.pack()

# Área de histórico de mensagens
history_text = tk.Text(root, state=tk.DISABLED, height=10, width=40)
history_text.pack()

root.mainloop()


