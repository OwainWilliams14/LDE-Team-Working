"""
Password Strength Checker (single file, Tkinter GUI)
----------------------------------------------------
Run with:  python password_checker_app.py

Concepts used:
  - Variables : min_length, good_length, symbols, colours, score
  - Arrays    : common_passwords, tips
  - Loops     : character checks, refilling the tips list
  - If        : every rule, the rating, button actions
  - Functions : each check, scoring, rating, generator, GUI actions

NOTE: Never store or log real passwords. This tool only checks
them in memory and forgets them straight away.
"""

import random
import string
import tkinter as tk
from tkinter import ttk

# =====================================================
# Variables and arrays
# =====================================================
common_passwords = ["password", "123456", "qwerty", "letmein", "admin", "welcome"]
min_length = 8
good_length = 12
symbols = "!@#$%^&*()-_=+?"
MAX_SCORE = 6

colours = {
    "Weak": "#d9534f",
    "Medium": "#f0ad4e",
    "Strong": "#5cb85c",
}


# =====================================================
# Check functions
# =====================================================
def check_length(password):
    return len(password) >= min_length


def has_uppercase(password):
    for char in password:
        if char.isupper():
            return True
    return False


def has_lowercase(password):
    for char in password:
        if char.islower():
            return True
    return False


def has_digit(password):
    for char in password:
        if char.isdigit():
            return True
    return False


def has_symbol(password):
    for char in password:
        if char in symbols:
            return True
    return False


def is_common(password):
    return password.lower() in common_passwords


def has_repeats(password):
    """True if the same character appears 3+ times in a row (e.g. 'aaa')."""
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1
            if count >= 3:
                return True
        else:
            count = 1
    return False


# =====================================================
# Scoring and rating
# =====================================================
def check_strength(password):
    """Return (score out of 6, list of tips)."""
    score = 0
    tips = []

    if is_common(password):
        return 0, ["This is a very common password. Pick something else."]

    if check_length(password):
        score += 1
    else:
        tips.append(f"Use at least {min_length} characters.")

    if len(password) >= good_length:
        score += 1
    else:
        tips.append(f"{good_length}+ characters is even better.")

    if has_uppercase(password) and has_lowercase(password):
        score += 1
    else:
        tips.append("Mix uppercase and lowercase letters.")

    if has_digit(password):
        score += 1
    else:
        tips.append("Add a number.")

    if has_symbol(password):
        score += 1
    else:
        tips.append("Add a symbol like ! or @.")

    if not has_repeats(password):
        score += 1
    else:
        tips.append("Avoid repeating the same character 3+ times.")

    return score, tips


def get_rating(score):
    if score >= 6:
        return "Strong"
    elif score >= 4:
        return "Medium"
    else:
        return "Weak"


# =====================================================
# Password generator
# =====================================================
def generate_password(length=14):
    all_chars = string.ascii_letters + string.digits + symbols
    # guarantee at least one of each type
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(symbols),
    ]
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    random.shuffle(password)
    return "".join(password)


# =====================================================
# GUI
# =====================================================
class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        root.title("Password Strength Checker")
        root.geometry("440x420")
        root.resizable(False, False)

        self.password_var = tk.StringVar()
        self.show_var = tk.BooleanVar(value=False)

        # Update results every time the text changes
        self.password_var.trace_add("write", self.update_result)

        self.build_widgets()
        self.update_result()

    def build_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame, text="Password Strength Checker", font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")
        ttk.Label(
            frame, text="Type a password to see how strong it is."
        ).pack(anchor="w", pady=(0, 12))

        # Entry box
        self.entry = ttk.Entry(
            frame, textvariable=self.password_var, show="*", font=("Segoe UI", 12)
        )
        self.entry.pack(fill="x")
        self.entry.focus()

        ttk.Checkbutton(
            frame,
            text="Show password",
            variable=self.show_var,
            command=self.toggle_show,
        ).pack(anchor="w", pady=(6, 12))

        # Strength bar and rating
        self.bar = ttk.Progressbar(frame, maximum=MAX_SCORE, length=380)
        self.bar.pack(fill="x")

        self.rating_label = tk.Label(frame, text="", font=("Segoe UI", 12, "bold"))
        self.rating_label.pack(anchor="w", pady=(6, 8))

        # Tips
        ttk.Label(frame, text="Tips:").pack(anchor="w")
        self.tips_box = tk.Listbox(
            frame, height=6, activestyle="none", borderwidth=1, relief="solid"
        )
        self.tips_box.pack(fill="x", pady=(2, 12))

        # Buttons
        button_row = ttk.Frame(frame)
        button_row.pack(fill="x")

        ttk.Button(
            button_row, text="Generate strong password", command=self.generate
        ).pack(side="left")
        ttk.Button(button_row, text="Copy", command=self.copy_password).pack(
            side="left", padx=8
        )
        ttk.Button(button_row, text="Clear", command=self.clear).pack(side="left")

        self.status = ttk.Label(frame, text="")
        self.status.pack(anchor="w", pady=(10, 0))

    def toggle_show(self):
        if self.show_var.get():
            self.entry.config(show="")
        else:
            self.entry.config(show="*")

    def update_result(self, *args):
        password = self.password_var.get()

        # Empty box: reset the display
        if password == "":
            self.bar["value"] = 0
            self.rating_label.config(text="Enter a password", fg="gray")
            self.tips_box.delete(0, tk.END)
            return

        score, tips = check_strength(password)
        rating = get_rating(score)

        self.bar["value"] = score
        self.rating_label.config(
            text=f"{rating} ({score}/{MAX_SCORE})", fg=colours[rating]
        )

        # Loop to refill the tips list
        self.tips_box.delete(0, tk.END)
        if len(tips) == 0:
            self.tips_box.insert(tk.END, "No weaknesses found. Nice work!")
        for tip in tips:
            self.tips_box.insert(tk.END, "- " + tip)

    def generate(self):
        self.password_var.set(generate_password())
        self.show_var.set(True)
        self.toggle_show()
        self.status.config(text="Generated a new password.")

    def copy_password(self):
        password = self.password_var.get()
        if password == "":
            self.status.config(text="Nothing to copy.")
        else:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.status.config(text="Copied to clipboard.")

    def clear(self):
        self.password_var.set("")
        self.status.config(text="")


def main():
    root = tk.Tk()
    PasswordCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()