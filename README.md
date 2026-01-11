# Baris' Mastermind 2025 - Harvard CS50P Final Project  

## 🎥 Video Demo: https://youtu.be/vfDunIeKVpU

---

## 📑 Table of Contents
- [Description](#-description)
- [Project Overview](#-project-overview)
- [File Structure](#-file-structure)
- [Design Choices](#-design-choices)
- [Final Notes](#-final-notes)
- [Part of a Learning Journey](#-part-of-a-learning-journey)
- [Links](#-links)
- [License](#-license)

---

## 📝 Description:

Baris' Mastermind is a fully featured, modernized recreation of the classic Mastermind logic game, implemented entirely in Python using Tkinter, Pillow (PIL), and standard libraries. This project is designed both as a functional game and as a demonstration of structured Python design, GUI development, state management, and clean architecture. It is submitted as my Final Project for CS50P.

This README explains the purpose of the project, its files, the architectural decisions I made, and the reasoning behind the design choices. It is intentionally detailed—over 500 words—to meet the project requirements and also to serve as documentation for anyone wishing to understand or extend the game.

---

## 🧠 Project Overview

Baris' Mastermind recreates the original deduction game where a player attempts to guess a secret color code within a limited number of tries. My version features a custom-designed graphical interface with rounded boards, smooth palette interaction, fullscreen support, keyboard shortcuts, and helpful dialogs. The project includes:

- A polished Tkinter GUI with rounded-corner boards created using PIL.
- A full game loop with guess rows, feedback pegs, win/loss dialogs, and a reset system.
- A clean separation between **game logic** and **GUI code**, allowing the core functions to be tested independently via pytest.
- A main entrypoint (`main()`) in `project.py` exactly as required by CS50P.
- Three required logic functions (`generate_code`, `check_guess`, `format_feedback`) each with corresponding tests in `test_project.py`.
- Use of constants to ensure maintainability.
- A README that explains structure, design reasoning, and implementation details.

---

## 📁 File Structure

### **project.py**
This is the main file and contains:

#### **`main()`**
The program’s entrypoint.  
Creates the Tk root window, configures fullscreen behavior, places the window icon, and initializes the `MastermindGUI` class.

#### **Game Logic Functions**
These three functions are required by the assignment, are pure (side-effect free), and are tested:

1. **`generate_code(colors, length)`**  
   Returns a random secret code list. Tests verify length, allowed values, and randomness.

2. **`check_guess(secret, guess)`**  
   Implements official Mastermind scoring rules: “black pegs” for correct color and position, “white pegs” for correct color in wrong position. Tests verify correctness with varied inputs.

3. **`format_feedback(black, white, length)`**  
   Converts black/white peg counts into a list of feedback labels. Tests ensure order and validity.

All three appear at top-level scope in `project.py`, as required.

#### **GUI Class: `MastermindGUI`**
This class handles all visual and user-interaction elements:

- Building the header bar with logo, title, and help button.
- Drawing a rounded board using PIL-generated transparent PNGs.
- Creating 10 guess rows with feedback indicators.
- Handling palette clicks and peg coloring.
- Displaying the status counter.
- Tracking current guess, game state, and resetting.
- Showing dialogs (welcome, win, loss) via `messagebox`.

The GUI uses Frames, Canvas widgets, PIL images, and Tkinter geometry managers to create a polished and efficient interface.

### test_project.py

This file contains pytest tests for the three required functions:

- `test_generate_code`
- `test_check_guess`
- `test_format_feedback`

The tests ensure correct behavior, proper exceptions, and rule compliance. The GUI is intentionally **not tested**, since CS50P only requires tests for the three logic functions.

### requirements.txt

Contains the following dependencies:

Pillow

Tkinter is part of Python’s standard library and requires no installation.

---

## 🎨 Design Choices

### **1. Rounded Boards Using PIL**
Tkinter cannot natively draw antialiased rounded rectangles for background frames, so I used Pillow to generate smooth-edge PNGs with alpha channels. These are composited behind frames to simulate modern UI panels.

### **2. Constants for Layout**
Values like board width, height, palette height, peg diameters, and colors are defined once at the top. This allows resizing, theme changes, or mobile adaptation without code rewrites.

### **3. Consistent Color System**
All colors are hex values. Tkinter behaves differently across OSes if named colors (like “red”) are used, so hex ensures consistency.

### **4. Preservation of Mastermind Terminology**
The logic still uses “black” and “white” to represent the official scoring, but visually the pegs use green/yellow/red for better clarity.

### **5. Fullscreen Experience**
The GUI launches in fullscreen and displays the welcome dialog *after* the interface has rendered, resulting in a professional first impression.

---

## 🎬 Final Notes

This project took significant design, iteration, and debugging, especially in the GUI. Creating the rounded panels, spacing elements precisely, and ensuring resizing stability were some of the trickiest aspects. The project satisfies each requirement of the CS50P Final Project specification and is structured for readability, maintainability, and future expansion (themes, multisize boards, difficulty modes, animations, sound, etc.).

I am proud of the final result and consider it a polished, complete Python application demonstrating both functional design and aesthetic UI implementation.

---

## 🧵 Part of a Learning Journey

This project is one of the key milestone projects from:

- Stanford Code in Place (CS106A)  
- Harvard CS50P  
- University of Michigan (SI206, SI364)  
- Google Data Analytics  
- Kaggle x Google: Generative AI Intensive  
- And my current work as a Data Scientist / Full Stack Developer  

Each project shows how far I’ve come and how every step built toward the next.

---

## 🔗 Links

**See the Game in Action:**  
https://youtu.be/vfDunIeKVpU

## 📜 License

This project was created for educational purposes as part of the Harvard CS50P program.  
All code is free to read, modify, and learn from.

---
