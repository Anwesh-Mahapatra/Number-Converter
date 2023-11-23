import tkinter as tk
from tkinter import ttk

# Function to get Intel's terminology for data sizes
def get_size_name(bit_length):
    if bit_length <= 8:
        return 'Byte'
    elif bit_length <= 16:
        return 'Word'
    elif bit_length <= 32:
        return 'Double Word'
    elif bit_length <= 64:
        return 'Quad Word'
    else:
        return 'Larger than Quad Word'

def convert():
    user_input = entry.get().strip()
    num_bytes = current_num_bytes.get()
    
    # Clear any existing bits_label to avoid duplicates
    if hasattr(convert, 'bits_label'):
        convert.bits_label.grid_forget()

    is_binary_input = binary_var.get()
    is_signed_input = signed_var.get()

    if is_binary_input:
        binary_value = user_input
        decimal_value = binary_to_decimal(binary_value) if is_signed_input else int(binary_value, 2)
        hexadecimal_value = binary_to_hexadecimal(binary_value)
        bit_length = len(binary_value)  # Calculate the bit length
        size_name = get_size_name(bit_length)  # Get the size name
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {binary_value}\nDecimal: {decimal_value}\nHexadecimal: {hexadecimal_value}\nNumber of Bits: {bit_length} ({size_name})\n")
    elif user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
        decimal_value = int(user_input)
        binary_value = decimal_to_binary(decimal_value, num_bytes)
        hexadecimal_value = decimal_to_hexadecimal(decimal_value).lstrip('-')  # Remove the minus sign
        bit_length = num_bytes * 8
        size_name = get_size_name(bit_length)  # Get the size name
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Binary: {binary_value}\nDecimal: {user_input}\nHexadecimal: {hexadecimal_value}\nNumber of Bits: {bit_length} ({size_name})\n")
    else:
        try:
            # Attempt to treat the input as hexadecimal
            hexadecimal_value = user_input
            decimal_value = int(hexadecimal_value, 16)
            binary_value = hexadecimal_to_binary(hexadecimal_value[2:], num_bytes)
            bit_length = num_bytes * 8
            size_name = get_size_name(bit_length)  # Get the size name
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Binary: {binary_value}\nDecimal: {decimal_value}\nHexadecimal: {user_input}\nNumber of Bits: {bit_length} ({size_name})\n")
        except ValueError:
            result_text.delete(1.0, tk.END)  # Clear the result text
            result_text.config(height=8)  # Dynamically adjust the height of the result_text widget
            return  # Exit the function if conversion fails

def update_bytes(*args):
    # This function is called when the number of bytes is changed
    convert()

# Conversion functions
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
    if signed_var.get() and binary[0] == '1':
        decimal_value -= 1 << num_bits

    return decimal_value

def binary_to_hexadecimal(binary, num_bytes=1):
    decimal_value = binary_to_decimal(binary) if signed_var.get() else int(binary, 2)
    return decimal_to_hexadecimal(decimal_value)

def hexadecimal_to_binary(hexadecimal, num_bytes=1):
    decimal_value = int(hexadecimal, 16)
    return decimal_to_binary(decimal_value, num_bytes)

# GUI setup with a simple style
root = tk.Tk()
root.title("Number Converter")

# Additional variable to track the selected number of bytes
current_num_bytes = tk.IntVar()
current_num_bytes.set(1)
current_num_bytes.trace_add("write", update_bytes)  # Call update_bytes when the variable is written

# Variable to track whether the input is binary or not
binary_var = tk.BooleanVar()
binary_var.set(False)

# Variable to track whether the input is to be treated as signed
signed_var = tk.BooleanVar()
signed_var.set(False)

# Styling
style = ttk.Style()
style.configure("TFrame", background="#333")
style.configure("TLabel", background="#333", foreground="white")
style.configure("TButton", background="#4CAF50", foreground="white")
style.configure("TEntry", fieldbackground="#ddd", foreground="#333", padding=5)
style.configure("TText", background="#444", foreground="white")

frame = ttk.Frame(root, padding="10", style="TFrame")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Enter a number (binary, decimal, or hexadecimal):", style="TLabel").grid(column=0, row=0, sticky=tk.W)
entry = ttk.Entry(frame, width=30, style="TEntry")
entry.grid(column=0, row=1, pady=5, sticky=tk.W)
entry.bind("<KeyRelease>", lambda event: convert())  # Bind the convert function to KeyRelease event

# Checkbox for binary input
binary_checkbox = ttk.Checkbutton(frame, text="Binary Input", variable=binary_var, style="TCheckbutton", command=convert)
binary_checkbox.grid(column=0, row=3, pady=5, sticky=tk.W)

# Checkbox for signed interpretation
signed_checkbox = ttk.Checkbutton(frame, text="Signed Interpretation", variable=signed_var, style="TCheckbutton", command=convert)
signed_checkbox.grid(column=0, row=5, pady=5, sticky=tk.W)

result_text = tk.Text(frame, wrap=tk.WORD, height=8, width=50, background="#444", foreground="white")
result_text.grid(column=0, row=6, pady=5, sticky=tk.W)

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
