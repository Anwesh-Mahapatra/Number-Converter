import tkinter as tk
from tkinter import ttk

def convert(event=None):
    user_input = entry.get().strip()
    num_bytes = current_num_bytes.get()

    if user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
        decimal_value = int(user_input)
        binary_value = decimal_to_binary(decimal_value, num_bytes)
        hexadecimal_value = decimal_to_hexadecimal(decimal_value).lstrip('-')  # Remove the minus sign
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {binary_value}\nDecimal: {user_input}\nHexadecimal: {hexadecimal_value}")

    elif user_input.lower().startswith("0b"):
        binary_value = user_input[2:]
        decimal_value = binary_to_decimal(binary_value)
        hexadecimal_value = binary_to_hexadecimal(binary_value)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {binary_value}\nDecimal: {decimal_value}\nHexadecimal: {hexadecimal_value}")

    elif user_input.lower().startswith("0x"):
        hexadecimal_value = user_input
        decimal_value = hexadecimal_to_decimal(hexadecimal_value)
        binary_value = hexadecimal_to_binary(hexadecimal_value[2:])
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {binary_value}\nDecimal: {decimal_value}\nHexadecimal: {user_input}")

    else:
        result_text.delete(1.0, tk.END)  # Clear the result text

        # Dynamically adjust the height of the result_text widget
        result_text.config(height=8)

def update_bytes(*args):
    # This function is called when the number of bytes is changed
    convert()

# Conversion functions (modified for two's complement representation)
def decimal_to_binary(decimal, num_bytes=1):
    # Ensure num_bytes is always positive
    num_bytes = max(1, num_bytes)

    # Format binary string with leading zeros
    binary_str = format(decimal if decimal >= 0 else (1 << (num_bytes * 8)) + decimal, f"0>{num_bytes * 8}b")
    return binary_str[-num_bytes * 8:]  # Keep only the last num_bytes * 8 characters

def decimal_to_hexadecimal(decimal):
    return hex(decimal)

def binary_to_decimal(binary):
    num_bits = len(binary)
    decimal_value = int(binary, 2)

    # Check if the most significant bit is set (indicating a negative value)
    if binary[0] == '1':
        decimal_value -= 1 << num_bits

    return decimal_value

def hexadecimal_to_decimal(hexadecimal):
    # Remove the '0x' prefix and handle empty string
    if hexadecimal.lower().startswith("0x"):
        hexadecimal = hexadecimal[2:]
    if not hexadecimal:
        return 0

    decimal_value = int(hexadecimal, 16)

    # Check if the most significant bit is set (indicating a negative value)
    if decimal_value & (1 << (len(hexadecimal) * 4 - 1)):
        decimal_value -= 1 << (len(hexadecimal) * 4)

    return decimal_value

def binary_to_hexadecimal(binary):
    decimal_value = binary_to_decimal(binary)
    return decimal_to_hexadecimal(decimal_value)

def hexadecimal_to_binary(hexadecimal):
    decimal_value = hexadecimal_to_decimal(hexadecimal)
    return decimal_to_binary(decimal_value, len(hexadecimal) - 2)

# GUI setup with a simple style
root = tk.Tk()
root.title("Number Converter")

# Additional variable to track the selected number of bytes
current_num_bytes = tk.IntVar()
current_num_bytes.set(1)
current_num_bytes.trace_add("write", update_bytes)  # Call update_bytes when the variable is written

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

result_text = tk.Text(frame, wrap=tk.WORD, height=8, width=50, background="#444", foreground="white")
result_text.grid(column=0, row=2, pady=5, sticky=tk.W)

# Option menu for selecting the number of bytes
byte_options = [1, 2, 4, 8]
byte_menu = ttk.OptionMenu(frame, current_num_bytes, byte_options[0], *byte_options)
ttk.Label(frame, text="Select number of bytes:", style="TLabel").grid(column=1, row=1, pady=5, sticky=tk.E)
byte_menu.grid(column=2, row=1, pady=5, sticky=tk.W)
byte_menu.configure(style="TButton")  # Apply the style to the option menu button

# Set window resizable and minimum size
root.resizable(True, True)
root.minsize(600, 400)  # Set a minimum size for the window

# Set focus to the entry widget
entry.focus()

root.mainloop()
