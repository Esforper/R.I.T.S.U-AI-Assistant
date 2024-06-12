# AppInterface.py

import tkinter as tk
from tkinter import scrolledtext
import re
from collections import Counter

class AppInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesajlaşma Uygulaması")
        self.root.geometry("600x400")

        # Mesaj girişi alanı
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        # Tahmin edilen kelimenin gösterileceği alan
        self.suggestion_label = tk.Label(root, text="", fg="grey")
        self.suggestion_label.pack()

        # Mesajları listeleyen alan (scrollable text area)
        self.message_list = scrolledtext.ScrolledText(root, width=50, height=15, state='disabled')
        self.message_list.pack(pady=10)

        # Mesaj gönderme butonu
        self.send_button = tk.Button(root, text="Mesaj Gönder", command=self.send_message)
        self.send_button.pack(pady=10)

        # Metin girişine tahmin işlevi ekleme
        self.entry.bind("<KeyRelease>", self.predict_word)
        self.entry.bind("<Tab>", self.complete_prediction)

        # Uygulama başladığında geçmiş mesajları yükleme
        self.load_messages()

    def send_message(self):
        message = self.entry.get()
        if message:
            # Mesajları listeleme alanına ekleme
            self.message_list.configure(state='normal')
            self.message_list.insert(tk.END, f"You: {message}\n")
            self.message_list.configure(state='disabled')
            
            # Mesajı dosyaya kaydetme
            with open("messages.txt", "a") as file:
                file.write(f"You: {message}\n")
            
            # Kelimeleri işleme ve dosyaya kaydetme
            self.process_words(message)
            
            # Metin giriş alanını temizleme
            self.entry.delete(0, tk.END)
            self.suggestion_label.config(text="")

    def load_messages(self):
        try:
            with open("messages.txt", "r") as file:
                messages = file.readlines()
                self.message_list.configure(state='normal')
                for message in messages:
                    self.message_list.insert(tk.END, message)
                self.message_list.configure(state='disabled')
        except FileNotFoundError:
            # Eğer dosya bulunamazsa, hiçbir şey yapma
            pass

    def process_words(self, message):
        # Mesajı kelimelere bölme ve kurallara göre filtreleme
        words = re.findall(r'\b\w+\b', message.lower())
        words = [word for word in words if len(word) >= 3]
        
        # Mevcut kelime sayılarını yükleme
        try:
            with open("word_counts.txt", "r") as file:
                lines = file.readlines()
                word_counts = Counter(dict(line.strip().split(': ') for line in lines))
                word_counts = Counter({k: int(v) for k, v in word_counts.items()})
        except FileNotFoundError:
            word_counts = Counter()
        
        # Yeni kelimeleri ekleyerek güncelleme
        word_counts.update(words)
        
        # Kelime sayılarını dosyaya kaydetme
        with open("word_counts.txt", "w") as file:
            for word, count in word_counts.items():
                file.write(f"{word}: {count}\n")

    def predict_word(self, event):
        input_text = self.entry.get()
        words = input_text.split()
        if not words:
            self.suggestion_label.config(text="")
            return
        
        last_word = words[-1]
        if len(last_word) < 3:
            self.suggestion_label.config(text="")
            return

        try:
            with open("word_counts.txt", "r") as file:
                lines = file.readlines()
                word_counts = Counter(dict(line.strip().split(': ') for line in lines))
                word_counts = Counter({k: int(v) for k, v in word_counts.items()})
        except FileNotFoundError:
            word_counts = Counter()
        
        predictions = [word for word in word_counts if word.startswith(last_word.lower())]
        if predictions:
            best_prediction = max(predictions, key=lambda x: word_counts[x])
            suggestion = best_prediction[len(last_word):]
            self.suggestion_label.config(text=suggestion)
        else:
            self.suggestion_label.config(text="")

    def complete_prediction(self, event):
        input_text = self.entry.get()
        suggestion = self.suggestion_label.cget("text")
        if suggestion:
            self.entry.insert(tk.END, suggestion)
            self.suggestion_label.config(text="")
        return "break"
