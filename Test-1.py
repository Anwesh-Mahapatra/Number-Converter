import tkinter as tk
from tkinter import ttk

def convert(event=None):
    user_input = entry.get().strip()

    if user_input.isdigit():
        decimal_value = int(user_input)
        binary_value = decimal_to_binary(decimal_value)
        hexadecimal_value = decimal_to_hexadecimal(decimal_value)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {user_input}\nDecimal: {binary_value}\nHexadecimal: {hexadecimal_value}")

    elif user_input.lower().startswith("0b"):
        binary_value = user_input[2:]
        decimal_value = binary_to_decimal(binary_value)
        hexadecimal_value = binary_to_hexadecimal(binary_value)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {user_input}\nDecimal: {decimal_value}\nHexadecimal: {hexadecimal_value}")

    elif user_input.lower().startswith("0x"):
        hexadecimal_value = user_input
        decimal_value = hexadecimal_to_decimal(hexadecimal_value)
        binary_value = hexadecimal_to_binary(hexadecimal_value[2:])
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {binary_value}\nDecimal: {decimal_value}\nHexadecimal: {user_input}")

    else:
        result_text.delete(1.0, tk.END)  # Clear the result text

# Conversion functions (unchanged)
def decimal_to_binary(decimal):
    return bin(decimal)[2:]

def decimal_to_hexadecimal(decimal):
    return hex(decimal)

def binary_to_decimal(binary):
    return int(binary, 2)

def hexadecimal_to_decimal(hexadecimal):
    return int(hexadecimal, 16)

def binary_to_hexadecimal(binary):
    decimal_value = binary_to_decimal(binary)
    return decimal_to_hexadecimal(decimal_value)

def hexadecimal_to_binary(hexadecimal):
    decimal_value = hexadecimal_to_decimal(hexadecimal)
    return decimal_to_binary(decimal_value)

def start_animation():
    for i in range(0, 101, 10):
        root.after(i, update_opacity, i)

def update_opacity(value):
    opacity = value / 100.0
    root.attributes('-alpha', opacity)

# GUI setup with a simple style
root = tk.Tk()
root.title("Number Converter")
root.attributes('-alpha', 0.0)  # Set initial transparency

# Styling
style = ttk.Style()
style.configure("TFrame", background="#333")
style.configure("TLabel", background="#333", foreground="white")
style.configure("TButton", background="#4CAF50", foreground="white")
style.configure("TEntry", fieldbackground="#ddd", foreground="#333", padding=5)  # Change the text color
style.configure("TText", background="#444", foreground="white")

frame = ttk.Frame(root, padding="10", style="TFrame")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Enter a number (binary, decimal, or hexadecimal):", style="TLabel").grid(column=0, row=0, sticky=tk.W)
entry = ttk.Entry(frame, width=30, style="TEntry")
entry.grid(column=0, row=1, pady=5, sticky=tk.W)
entry.bind("<KeyRelease>", convert)  # Bind the convert function to KeyRelease event

result_text = tk.Text(frame, wrap=tk.WORD, height=5, width=50, background="#444", foreground="white")
result_text.grid(column=0, row=2, pady=5, sticky=tk.W)

# Set focus to the entry widget
entry.focus()

# Start the animation after a delay (adjust the delay as needed)
root.after(500, start_animation)

root.mainloop()
