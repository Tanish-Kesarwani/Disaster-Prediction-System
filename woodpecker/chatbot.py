import tkinter as tk
from tkinter import scrolledtext
import pickle
import os

class Chatbot:
    def __init__(self, training_file='training_data.txt', learned_file='learned_data.pkl'):
        self.training_file = training_file
        self.learned_file = learned_file
        self.responses = {}
        self.load_initial_data()
        self.load_learned_data()

    def load_initial_data(self):
        if os.path.exists(self.training_file):
            with open(self.training_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split('::')
                    if len(parts) == 2:
                        self.responses[parts[0].strip().lower()] = parts[1].strip()

    def load_learned_data(self):
        if os.path.exists(self.learned_file):
            with open(self.learned_file, 'rb') as file:
                self.responses.update(pickle.load(file))

    def save_learned_data(self):
        with open(self.learned_file, 'wb') as file:
            pickle.dump(self.responses, file)

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        return self.responses.get(user_input, None)

    def learn_response(self, user_input, response):
        self.responses[user_input.lower().strip()] = response.lower().strip()
        self.save_learned_data()

class ChatbotUI:
    def __init__(self, root, chatbot):
        self.chatbot = chatbot

        self.root = root
        self.root.title("Chatbot")

        # Set the background color
        self.root.configure(bg='#e0f7fa')

        # Create the chat history area
        self.chat_history = scrolledtext.ScrolledText(self.root, state='disabled', width=50, height=20,
                                                     bg='#b2ebf2', fg='#000000', font=("Arial", 12))
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Create the user input area
        self.user_input = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        # Create the send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message,
                                     bg='#4fc3f7', fg='#ffffff', font=("Arial", 12), relief='raised', bd=2)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Create the bottom padding
        self.bottom_padding = tk.Label(self.root, bg='#e0f7fa')
        self.bottom_padding.grid(row=2, column=0, columnspan=2, pady=(0, 10))

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("You: " + user_message)
            response = self.chatbot.get_response(user_message)
            if response:
                self.display_message("Bot: " + response)
            else:
                self.display_message("Bot: I don't know the answer to that. What should I respond?")
                new_response = self.user_input.get()
                self.chatbot.learn_response(user_message, new_response)
                self.display_message("Bot: Thank you for teaching me!")
            self.user_input.delete(0, tk.END)

    def display_message(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message + '\n')
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = Chatbot()
    ui = ChatbotUI(root, chatbot)
    root.mainloop()
