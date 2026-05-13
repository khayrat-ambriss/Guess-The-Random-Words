import tkinter as tk
import random
from .config import COLORS, FONTS, GAME_CONFIG
from .data import CATEGORIES
from .engine import GameEngine, LetterState

class CyberWordleUI:
    def __init__(self, root):
        self.root = root
        self.engine = GameEngine()
        self.engine.max_attempts = GAME_CONFIG["max_attempts"]

        self.root.title("CYBER WORDLE INFINITY")
        try:
            self.root.state('zoomed')
        except tk.TclError:
            pass
        self.root.configure(bg=COLORS["bg_deep"])

        self.selected_category = list(CATEGORIES.keys())[0]
        self.tiles = []
        self.bg_particles = []
        self.cat_buttons = {}

        self.setup_ui()
        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Key>", self.handle_keypress)
        self.animate_bg()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg=COLORS["bg_deep"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.header = self.canvas.create_text(0, 0, text="CYBER WORDLE", font=FONTS["header"], fill=COLORS["accent"])

        # Category Frame
        self.ctrl_frame = tk.Frame(self.root, bg=COLORS["bg_deep"])
        self.ctrl_window = self.canvas.create_window(0, 0, window=self.ctrl_frame)

        for cat in CATEGORIES.keys():
            btn = tk.Button(self.ctrl_frame, text=cat,
                            command=lambda c=cat: self.select_cat(c),
                            font=FONTS["button"], bg=COLORS["card"], fg="white",
                            activebackground=COLORS["accent"], activeforeground="black",
                            relief="flat", bd=0, padx=15, pady=8, cursor="hand2")
            btn.pack(side="left", padx=5)
            self.cat_buttons[cat] = btn

        # Game controls
        self.btn_init = tk.Button(self.root, text="[ INITIATE SYSTEM BREACH ]", command=self.start_game,
                                 font=("Impact", 16), bg=COLORS["correct"], fg="black",
                                 relief="flat", borderwidth=0, cursor="hand2", padx=40, pady=10)
        self.init_window = self.canvas.create_window(0, 0, window=self.btn_init)

        # Hint display
        self.hint_text = self.canvas.create_text(0, 0, text="", font=FONTS["hint"], fill=COLORS["present"], state="hidden")

        # Signature
        self.sig_glow = self.canvas.create_text(21, 0, text="MADE BY KHAYRAT AMBRISS",
                                               font=FONTS["info"], fill="#005577", anchor="sw")
        self.signature = self.canvas.create_text(20, 0, text="MADE BY KHAYRAT AMBRISS",
                                               font=FONTS["info"], fill=COLORS["accent"], anchor="sw")

        self.select_cat(self.selected_category)

    def select_cat(self, cat):
        self.selected_category = cat
        for name, btn in self.cat_buttons.items():
            if name == self.selected_category:
                btn.config(bg=COLORS["accent"], fg="black")
            else:
                btn.config(bg=COLORS["card"], fg="white")

    def on_resize(self, event=None):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.canvas.coords(self.header, w/2, 80)
        self.canvas.coords(self.ctrl_window, w/2, 170)
        self.canvas.coords(self.init_window, w/2, 240)
        self.canvas.coords(self.hint_text, w/2, 300)
        self.canvas.coords(self.sig_glow, 31, h - 29)
        self.canvas.coords(self.signature, 30, h - 30)
        if hasattr(self, 'board_y'):
            self.reposition_board()

    def reposition_board(self):
        if not self.tiles: return
        w = self.root.winfo_width()
        tw, th = GAME_CONFIG["tile_size"]
        gap = GAME_CONFIG["tile_gap"]
        word_len = len(self.engine.target_word)
        board_w = (word_len * tw) + ((word_len - 1) * gap)
        start_x = (w - board_w) / 2
        start_y = 350

        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                x1, y1 = start_x + c * (tw + gap), start_y + r * (th + gap)
                # We need to update the coordinates of the polygon and text
                points = self.get_rounded_rect_points(x1, y1, x1+tw, y1+th, radius=12)
                self.canvas.coords(tile["rect"], *points)
                self.canvas.coords(tile["text"], x1+tw/2, y1+th/2)

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
        word_data = random.choice(CATEGORIES[self.selected_category])
        self.engine.set_word(word_data["word"], word_data["hint"], word_data["emoji"])

        self.canvas.delete("game_tile")
        self.tiles = []

        self.canvas.itemconfig(self.hint_text, text=f"HINT: {self.engine.hint}", state="normal")

        w = self.root.winfo_width()
        tw, th = GAME_CONFIG["tile_size"]
        gap = GAME_CONFIG["tile_gap"]
        word_len = len(self.engine.target_word)
        board_w = (word_len * tw) + ((word_len - 1) * gap)
        start_x, start_y = (w - board_w) / 2, 350

        for r in range(self.engine.max_attempts):
            row_tiles = []
            for c in range(word_len):
                x1, y1 = start_x + c * (tw + gap), start_y + r * (th + gap)
                rect = self.draw_rounded_rect(self.canvas, x1, y1, x1+tw, y1+th, radius=12,
                                             fill=COLORS["bg_deep"], outline=COLORS["absent"], width=2, tags="game_tile")
                text = self.canvas.create_text(x1+tw/2, y1+th/2, text="", font=FONTS["tile"], fill="white", tags="game_tile")
                row_tiles.append({"rect": rect, "text": text})
            self.tiles.append(row_tiles)

    def draw_rounded_rect(self, canvas, x1, y1, x2, y2, radius=15, **kwargs):
        points = self.get_rounded_rect_points(x1, y1, x2, y2, radius)
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def get_rounded_rect_points(self, x1, y1, x2, y2, radius=15):
        return [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

    def handle_keypress(self, event):
        if self.engine.game_over:
            return

        if event.keysym == "BackSpace":
            if self.engine.remove_letter():
                self.update_board()
        elif event.keysym == "Return":
            self.submit_guess()
        elif len(event.char) == 1 and event.char.isalpha():
            if self.engine.add_letter(event.char):
                self.update_board()

    def update_board(self):
        if not self.tiles or self.engine.game_over: return

        current_row = len(self.engine.attempts)
        if current_row >= self.engine.max_attempts: return

        current_guess = self.engine.current_attempt
        states = self.engine.get_letter_states_realtime()

        for i, tile in enumerate(self.tiles[current_row]):
            if i < len(current_guess):
                char = current_guess[i]
                state = states[i]
                color = self.get_color_for_state(state)

                self.canvas.itemconfig(tile["text"], text=char.upper(), fill=color)
                self.canvas.itemconfig(tile["rect"], outline=color, width=2 if state == LetterState.ABSENT else 4)
            else:
                self.canvas.itemconfig(tile["text"], text="", fill="white")
                self.canvas.itemconfig(tile["rect"], outline=COLORS["absent"], width=2)
            self.canvas.tag_raise(tile["text"])

    def submit_guess(self):
        current_row = len(self.engine.attempts)
        success, results = self.engine.submit_guess()

        if not success:
            self.shake_row(current_row)
            return

        # Animate current row with final results
        for i, state in enumerate(results):
            tile = self.tiles[current_row][i]
            color = self.get_color_for_state(state)
            self.canvas.itemconfig(tile["rect"], fill=color, outline=color)
            self.canvas.itemconfig(tile["text"], fill="black" if state in [LetterState.CORRECT, LetterState.PRESENT] else "white")

        if self.engine.won:
            self.root.after(300, lambda: self.show_msg(f"ACCESS GRANTED {self.engine.emoji}", COLORS["correct"]))
        elif self.engine.game_over:
            self.root.after(300, lambda: self.show_msg(f"LOCKOUT: {self.engine.target_word.upper()}", COLORS["danger"]))

    def get_color_for_state(self, state):
        if state == LetterState.CORRECT: return COLORS["correct"]
        if state == LetterState.PRESENT: return COLORS["present"]
        if state == LetterState.ABSENT: return COLORS["text_dim"]
        return "white"

    def shake_row(self, row_idx):
        tags = f"row_{row_idx}"
        for tile in self.tiles[row_idx]:
            self.canvas.addtag_withtag(tags, tile["rect"])
            self.canvas.addtag_withtag(tags, tile["text"])

        for _ in range(3):
            self.canvas.move(tags, 10, 0); self.root.update(); self.root.after(20)
            self.canvas.move(tags, -10, 0); self.root.update(); self.root.after(20)

    def show_msg(self, text, color):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        cx, cy = w / 2, h / 2
        bg = self.canvas.create_rectangle(cx-400, cy-70, cx+400, cy+70, fill=COLORS["bg_deep"], outline=color, width=5, tags="game_tile")
        msg = self.canvas.create_text(cx, cy, text=text, font=FONTS["message"], fill="white", tags="game_tile")
        self.canvas.tag_raise(bg)
        self.canvas.tag_raise(msg)
