import tkinter as tk
from tkinter import ttk
import random

# --- Level 10,000 Cyber-Light Palette ---
C = {
    "bg_deep": "#000B1E",
    "card": "#002B5B",
    "accent": "#00D4FF",      
    "correct": "#00FF95",  # Neon Green
    "present": "#FFD700",  # Cyber Gold
    "absent": "#1A2A40",   # Dark Blue-Gray
    "text_dim": "#445566", # For wrong letters
    "text": "#FFFFFF",
    "danger": "#FF3131",
}

CATEGORIES = {
    "🏀 Basketball": ["LeBron", "Giannis", "Luka", "Curry", "Durant"],
    "⚽ Football": ["Messi", "Ronaldo", "Mbappe", "Neymar", "Haaland"],
    "🌍 Countries": ["Brazil", "France", "Japan", "Canada", "Norway"],
    "👾 Random": ["Space", "Pixel", "Cyber", "Ghost", "Light"]
}

class WordleInfinity:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBER WORDLE INFINITY")
        self.root.state('zoomed')
        self.root.configure(bg=C["bg_deep"])
        
        self.root.update_idletasks()

        self.word = ""
        self.current_row = 0
        self.current_guess = ""
        self.selected_category = "👾 Random"
        self.tiles = []
        self.bg_particles = []
        self.cat_buttons = {}

        self.setup_ui()
        self.root.bind("<Configure>", self.on_resize)
        self.animate_bg()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg=C["bg_deep"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.header = self.canvas.create_text(0, 0, text="CYBER WORDLE", font=("Fixedsys", 60, "bold"), fill=C["accent"])

        self.ctrl_frame = tk.Frame(self.root, bg=C["bg_deep"])
        self.ctrl_window = self.canvas.create_window(0, 0, window=self.ctrl_frame)

        for cat in CATEGORIES.keys():
            btn = tk.Button(self.ctrl_frame, text=cat,
                            command=lambda c=cat: self.select_cat(c),
                            font=("Verdana", 11, "bold"), bg=C["card"], fg="white",
                            activebackground=C["accent"], activeforeground="black",
                            relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
            btn.pack(side="left", padx=5)
            self.cat_buttons[cat] = btn

        self.btn_init = tk.Button(self.root, text="[ INITIATE SYSTEM BREACH ]", command=self.start_game,
                                 font=("Impact", 16), bg=C["correct"], fg="black",
                                 relief="flat", borderwidth=0, cursor="hand2", padx=40, pady=10)
        self.init_window = self.canvas.create_window(0, 0, window=self.btn_init)

        self.sig_glow = self.canvas.create_text(21, 0, text="MADE BY KHAYRAT AMBRISS",
                                               font=("Courier", 11, "bold"), fill="#005577", anchor="sw")
        self.signature = self.canvas.create_text(20, 0, text="MADE BY KHAYRAT AMBRISS",
                                               font=("Courier", 11, "bold"), fill=C["accent"], anchor="sw")

        self.entry = tk.Entry(self.root, width=1, bg=C["bg_deep"], bd=0, fg=C["bg_deep"], insertontime=0)
        self.entry_window = self.canvas.create_window(0, 0, window=self.entry)
        self.entry.bind("<KeyRelease>", self.handle_keypress)
        self.entry.bind("<Return>", lambda e: self.submit_guess())
        
        self.select_cat("👾 Random")

    def select_cat(self, cat):
        self.selected_category = cat
        self.refresh_button_styles()

    def refresh_button_styles(self):
        for name, btn in self.cat_buttons.items():
            if name == self.selected_category:
                btn.config(bg=C["accent"], fg="black")
            else:
                btn.config(bg=C["card"], fg="white")

    def on_resize(self, event=None):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.canvas.coords(self.header, w/2, 100)
        self.canvas.coords(self.ctrl_window, w/2, 210)
        self.canvas.coords(self.init_window, w/2, 290)
        self.canvas.coords(self.entry_window, w/2, h - 50)
        self.canvas.coords(self.sig_glow, 31, h - 29)
        self.canvas.coords(self.signature, 30, h - 30)

    def animate_bg(self):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        if len(self.bg_particles) < 70:
            x = random.randint(0, w)
            p = self.canvas.create_oval(x, 0, x+2, random.randint(5, 15), fill="#003366", outline="")
            self.canvas.tag_lower(p)
            self.bg_particles.append([p, random.uniform(3, 8)])

        for p_data in self.bg_particles[:]:
            p, speed = p_data
            try:
                self.canvas.move(p, 0, speed)
                if self.canvas.coords(p)[1] > h:
                    self.canvas.delete(p)
                    self.bg_particles.remove(p_data)
            except: pass
        self.root.after(30, self.animate_bg)

    def start_game(self):
        self.word = random.choice(CATEGORIES[self.selected_category]).lower()
        self.current_row = 0
        self.current_guess = ""
        self.canvas.delete("game_tile")
        self.tiles = []

        w = self.root.winfo_width()
        tw, th, gap = 75, 95, 15
        board_w = (len(self.word) * tw) + ((len(self.word)-1) * gap)
        start_x, start_y = (w - board_w) / 2, 380

        for r in range(5): 
            row_tiles = []
            for c in range(len(self.word)):
                x1, y1 = start_x + c * (tw + gap), start_y + r * (th + gap)
                rect = self.draw_rounded_rect(self.canvas, x1, y1, x1+tw, y1+th, radius=12,
                                             fill=C["bg_deep"], outline=C["absent"], width=2, tags="game_tile")
                text = self.canvas.create_text(x1+tw/2, y1+th/2, text="", font=("Verdana", 34, "bold"), fill="white", tags="game_tile")
                row_tiles.append({"rect": rect, "text": text})
            self.tiles.append(row_tiles)
        self.entry.focus_set()

    def draw_rounded_rect(self, canvas, x1, y1, x2, y2, radius=15, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def handle_keypress(self, event):
        if event.keysym == "BackSpace": 
            self.current_guess = self.current_guess[:-1]
        elif len(self.current_guess) < len(self.word) and event.char.isalpha():
            self.current_guess += event.char.lower()
        self.update_board()

    def update_board(self):
        """Re-tests ALL letters in the current guess against the target word in real-time."""
        if not self.tiles or self.current_row >= 5: return
        
        target_list = list(self.word)
        
        for i, tile in enumerate(self.tiles[self.current_row]):
            if i < len(self.current_guess):
                char = self.current_guess[i]
                
                # RE-TEST LOGIC
                if char == self.word[i]:
                    color = C["correct"]
                    border = 4
                elif char in self.word:
                    color = C["present"]
                    border = 2
                else:
                    color = C["text_dim"]
                    border = 1
                
                self.canvas.itemconfig(tile["text"], text=char.upper(), fill=color)
                self.canvas.itemconfig(tile["rect"], outline=color, width=border)
            else:
                # Reset empty tiles
                self.canvas.itemconfig(tile["text"], text="", fill="white")
                self.canvas.itemconfig(tile["rect"], outline=C["absent"], width=2)
            
            self.canvas.tag_raise(tile["text"])

    def submit_guess(self):
        if len(self.current_guess) != len(self.word):
            self.shake_row()
            return

        if self.current_guess == self.word:
            self.root.after(200, lambda: self.show_msg("ACCESS GRANTED", C["correct"]))
        elif self.current_row == 4:
            self.root.after(200, lambda: self.show_msg(f"LOCKOUT: {self.word.upper()}", C["danger"]))
        else:
            self.current_row += 1
            self.current_guess = ""
            # Board updates automatically for the new row because current_guess is now empty

    def shake_row(self):
        for _ in range(3):
            self.canvas.move("game_tile", 15, 0); self.root.update(); self.root.after(20)
            self.canvas.move("game_tile", -15, 0); self.root.update(); self.root.after(20)

    def show_msg(self, text, color):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        cx, cy = w / 2, h / 2
        bg = self.canvas.create_rectangle(cx-300, cy-70, cx+300, cy+70, fill=C["bg_deep"], outline=color, width=5, tags="game_tile")
        msg = self.canvas.create_text(cx, cy, text=text, font=("Impact", 45), fill="white", tags="game_tile")
        self.canvas.tag_raise(bg)
        self.canvas.tag_raise(msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleInfinity(root)
    app.on_resize()
    root.mainloop()
    