"""
Mastermind (Tkinter)

Gameplay:
- 10 rows, each row: 4 large guess pegs + small 2x2 feedback block to the right.
- Palette (6 color pegs) below the board. Clicking a color fills the next empty peg
  in the current row automatically.
- When a row completes (4 pegs), feedback is calculated and shown immediately.
- If solved or out of tries, user is offered to play again via a dialog.

Top-level functions (testable):
- generate_code(colors, length)
- check_guess(secret, guess)
- format_feedback(black, white, length)
"""

import random
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox, ttk
from typing import List, Tuple

def make_rounded_board(w, h, radius, color="#1e252b"):
    img = Image.new("RGBA", (w, h), color)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), radius, fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)

# constants & appearance
# use hex colors for consistent Tk behavior on macOS/Linux/Windows
COLORS = ["#38ffff", "#ff6a00", "#ccf300", "#ff5e9c", "#5a7af5", "#b277ff"]
DISPLAY_NAMES = {
    "#38ffff": "Cyan",
    "#ff6a00": "Orange",
    "#ccf300": "Lime",
    "#ff5e9c": "Pink",
    "#5a7af5": "Blue",
    "#b277ff": "Violet",
}

CODE_LENGTH = 4
MAX_TRIES = 10

# board and palette layout constants
BOARD_WIDTH = 360
BOARD_HEIGHT = 600
BORDER_RADIUS = 24
HEADER_WIDTH = 400
HEADER_HEIGHT = 60
PALETTE_HEIGHT = 110

# game peg visual sizes (pixels)
LARGE_PEG_DIAM = 40
LARGE_PEG_GAP = 12
ROW_PAD_Y = 3

# the feedback block is the same height as a large peg; small pegs form a 2x2 inside it
FEEDBACK_BLOCK_SIZE = LARGE_PEG_DIAM
SMALL_PEG_DIAM = (FEEDBACK_BLOCK_SIZE - 8) // 2
SMALL_PEG_GAP = 6


# core logic
def generate_code(colors: List[str] = COLORS, length: int = CODE_LENGTH) -> List[str]:
    """Return a random secret code (list of colors). Duplicates allowed."""
    return [random.choice(colors) for _ in range(length)]


def check_guess(secret: List[str], guess: List[str]) -> Tuple[int, int]:
    """
    Return (black, white):
    - black: correct color & position
    - white: correct color, wrong position (excluding blacks)
    """
    if len(secret) != len(guess):
        raise ValueError("Secret and guess must be same length")
    black = sum(s == g for s, g in zip(secret, guess))
    total_matches = sum(min(secret.count(c), guess.count(c)) for c in set(guess))
    white = total_matches - black
    return black, white


def format_feedback(black: int, white: int, length: int = CODE_LENGTH) -> List[str]:
    """
    Return a list of length `length` with 'black' first, then 'white', then 'empty'.
    """
    if black < 0 or white < 0 or black + white > length:
        raise ValueError("Invalid black/white counts")
    return ["black"] * black + ["white"] * white + ["empty"] * (length - black - white)


# GUI
class MastermindGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mastermind")
        self.logo_img = ImageTk.PhotoImage(
            Image.open("mastermind.png").resize((40, 40), Image.LANCZOS)
        )
        self.secret = generate_code()
        self.current_try = 0
        self.rows = []
        self.game_over = False

        self._build_ui()
        self._create_rows()
        
        self.root.update_idletasks()
        self.root.after_idle(self._show_welcome_dialog)

    def _build_ui(self):
        pad = 12
        self.container = tk.Frame(self.root, padx=pad, pady=pad)
        self.container.pack()

        header = ttk.Frame(self.container)
        header.grid(row=0, column=0, columnspan=3, pady=(4, 4))

        ttk.Label(header, image=self.logo_img).pack(side="left", padx=6)

        ttk.Label(
            header,
            text="BARIS' MASTERMIND",
            font=("Helvetica", 18, "bold"),
        ).pack(side="left", padx=8)

        ttk.Button(
            header,
            text="?",
            style="Help.TButton",
            command=self._show_welcome_dialog,
            cursor="hand2",
        ).pack(side="left", padx=6)

        ttk.Label(header, image=self.logo_img).pack(side="left", padx=6)

        self.board_color = "#1e252b"

        self.board_img = make_rounded_board(BOARD_WIDTH, BOARD_HEIGHT, BORDER_RADIUS, self.board_color)

        self.board_label = tk.Label(self.container, image=self.board_img, bg=self.container.cget("bg"))
        self.board_label.grid(row=1, column=0, columnspan=3, pady=(4, 0))

        self.board_bg = tk.Frame(self.board_label, bg=self.board_color, padx=24, pady=24)
        self.board_bg.place(relx=0.5, rely=0.0, anchor="n")

        self.board_frame = tk.Frame(self.board_bg, bg=self.board_color)
        self.board_frame.pack()

        self.palette_img = make_rounded_board(BOARD_WIDTH, PALETTE_HEIGHT, BORDER_RADIUS, self.board_color)

        self.palette_label = tk.Label(self.container, image=self.palette_img, bg=self.container.cget("bg"))
        self.palette_label.grid(row=2, column=0, columnspan=3, pady=(4, 0))

        peg_row = tk.Frame(self.palette_label, bg=self.board_color)
        peg_row.place(relx=0.5, rely=0.40, anchor="center")

        # status label
        self.status_label = tk.Label(
            self.palette_label,
            text="",
            fg="white",
            bg=self.board_color,
            font=("Helvetica", 11, "bold")
        )
        self.status_label.place(relx=0.5, rely=0.80, anchor="center")

        for color in COLORS:
            pc = tk.Canvas(
                peg_row,
                width=LARGE_PEG_DIAM,
                height=LARGE_PEG_DIAM,
                highlightthickness=0,
                bd=0,
                cursor="hand2",
                bg=self.board_color
            )
            pc.pack(side="left", padx=6)
            pc.create_oval(2, 2, LARGE_PEG_DIAM - 2, LARGE_PEG_DIAM - 2, fill=color, outline=color)
            pc.bind("<Button-1>", lambda ev, col=color: self._palette_click(col))

        self.root.bind("<h>", lambda e: self._show_welcome_dialog())
        self.root.bind("<H>", lambda e: self._show_welcome_dialog())

    def _show_welcome_dialog(self):
        messagebox.showinfo(
            "Welcome to Mastermind",
            "Welcome to Mastermind!\n\n"
            "HOW TO PLAY:\n\n"
            "- A secret code of 4 colors has been chosen.\n"
            "- Colors may repeat, no blank slots.\n"
            "- Click colors in the palette to build your guess.\n"
            "- After each guess, you will receive feedback:\n"
            "   • 🟢 GREEN = Correct color in the correct position.\n"
            "   • 🟡 YELLOW = Correct color in the wrong position.\n"
            "   • 🔴 RED = Color not included in the code.\n\n"
            "Try to crack the code within 10 attempts!\n\n"
            "Ready?"
        )
    
    def _create_rows(self):
        """Create MAX_TRIES row canvases at startup. Only current_try row is interactive."""
        for r in range(MAX_TRIES):
            frame = tk.Frame(self.board_frame, pady=ROW_PAD_Y, bg=self.board_color, bd=0, highlightthickness=0)
            grid_row = MAX_TRIES - 1 - r
            frame.grid(row=grid_row, column=0, sticky="ew")

            guess_w = (LARGE_PEG_DIAM * CODE_LENGTH) + (LARGE_PEG_GAP * (CODE_LENGTH - 1)) + 8
            guess_h = LARGE_PEG_DIAM + 8
            guess_canvas = tk.Canvas(frame, width=guess_w, height=guess_h, bg=self.board_color, highlightthickness=0, bd=0)
            guess_canvas.pack(side="left")

            peg_items = []
            x = 4
            y = 4
            for i in range(CODE_LENGTH):
                oval = guess_canvas.create_oval(x, y, x + LARGE_PEG_DIAM, y + LARGE_PEG_DIAM,
                                               fill="lightgray", outline="lightgray")
                peg_items.append(oval)
                x += LARGE_PEG_DIAM + LARGE_PEG_GAP

            # feedback block: 2x2 small indicator pegs
            fb_canvas = tk.Canvas(frame, width=FEEDBACK_BLOCK_SIZE, height=FEEDBACK_BLOCK_SIZE,
                                  bg=self.board_color, highlightthickness=0, bd=0)
            fb_canvas.pack(side="left", padx=(12, 0))

            fb_items = []
            small_x0 = (FEEDBACK_BLOCK_SIZE - (2 * SMALL_PEG_DIAM + SMALL_PEG_GAP)) // 2
            small_y0 = (FEEDBACK_BLOCK_SIZE - (2 * SMALL_PEG_DIAM + SMALL_PEG_GAP)) // 2
            for rr in range(2):
                for cc in range(2):
                    sx = small_x0 + cc * (SMALL_PEG_DIAM + SMALL_PEG_GAP)
                    sy = small_y0 + rr * (SMALL_PEG_DIAM + SMALL_PEG_GAP)
                    soval = fb_canvas.create_oval(sx, sy, sx + SMALL_PEG_DIAM, sy + SMALL_PEG_DIAM,
                                                  fill="lightgray", outline="lightgray")
                    fb_items.append(soval)

            row_state = {
                "guess_canvas": guess_canvas,
                "peg_items": peg_items,
                "guess_state": [None] * CODE_LENGTH,
                "fb_canvas": fb_canvas,
                "fb_items": fb_items,
                "solved": False
            }
            self.rows.append(row_state)

        self.board_frame.grid_columnconfigure(0, weight=1)

        # update status once rows are created
        self._update_status_label()

    # palette click
    def _palette_click(self, color: str):
        """Fill the next empty peg in the current row with `color`."""
        if self.game_over:
            return

        row = self.rows[self.current_try]
        # find first empty peg
        try:
            pos = row["guess_state"].index(None)
        except ValueError:
            # Row full: ignore palette clicks
            return

        # set state and draw peg
        row["guess_state"][pos] = color
        canvas = row["guess_canvas"]
        oval_id = row["peg_items"][pos]
        canvas.itemconfig(oval_id, fill=color, outline=color)
        canvas.update_idletasks()

        # if row now full -> compute feedback immediately
        if None not in row["guess_state"]:
            black, white = check_guess(self.secret, row["guess_state"])
            fb = format_feedback(black, white, CODE_LENGTH)
            self._draw_feedback(row["fb_canvas"], row["fb_items"], fb)

            if black == CODE_LENGTH:
                self.rows[self.current_try]["solved"] = True
                self.game_over = True
                self._reveal_win()
                return

            # advance to next row or end game
            self.current_try += 1
            if self.current_try >= MAX_TRIES:
                self.game_over = True
                self._reveal_loss()
                return

            self._update_status_label()

    # draw feedback (2x2 small pegs)
    # feedback peg color meaning (display only):
    #   "black" → correct color in correct position  → shown as GREEN  (#39ff14)
    #   "white" → correct color in wrong position   → shown as YELLOW (#f8ff00)
    #   "empty" → no match                          → shown as RED    (#ff5555)
    #
    # note: names "black" and "white" are *mastermind rule terms* and remain in logic.
    # only the visual colors differ.
    def _draw_feedback(self, fb_canvas: tk.Canvas, fb_items: List[int], feedback: List[str]):
        for i, v in enumerate(feedback):
            oid = fb_items[i]
            if v == "black":
                fb_canvas.itemconfig(oid, fill="#39ff14", outline="#39ff14")
            elif v == "white":
                fb_canvas.itemconfig(oid, fill="#f8ff00", outline="#f8ff00")
            else:
                fb_canvas.itemconfig(oid, fill="#ff5555", outline="#ff5555")
        fb_canvas.update_idletasks()

    # win / loss dialogs
    def _reveal_win(self):
        names = ", ".join(DISPLAY_NAMES[c] for c in self.secret)
        if messagebox.askyesno(
            "You Win Mastermind!", 
            f"YOU WIN MASTERMIND!\n\nYou cracked the code on try #{self.current_try + 1}!\n\nThe code was:\n{names}\n\nPlay again?"
        ):
            self._reset_game()

    def _reveal_loss(self):
        names = ", ".join(DISPLAY_NAMES[c] for c in self.secret)
        if messagebox.askyesno(
            "Game Over", 
            f"GAME OVER\n\nYou used all {MAX_TRIES} tries.\n\nThe code was:\n{names}\n\nPlay again?"
        ):
            self._reset_game()

    # helpers: status & reset
    def _update_status_label(self):
        self.status_label.config(text=f"{self.current_try + 1} / {MAX_TRIES}")

    def _reset_game(self):
        self.secret = generate_code()
        self.current_try = 0
        self.game_over = False
        for row in self.rows:
            for oid in row["peg_items"]:
                row["guess_canvas"].itemconfig(oid, fill="lightgray", outline="lightgray")
            row["guess_state"] = [None] * CODE_LENGTH
            for oid in row["fb_items"]:
                row["fb_canvas"].itemconfig(oid, fill="lightgray", outline="lightgray")
            row["solved"] = False
        self._update_status_label()

    # helper to reveal secret without dialog (for debugging)
    def reveal_secret_quiet(self):
        return [DISPLAY_NAMES[c] for c in self.secret]

# entrypoint
def main():
    root = tk.Tk()
    try:
        icon = tk.PhotoImage(file="mastermind.png")
        root.iconphoto(True, icon)
    except:
        pass
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    app = MastermindGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
