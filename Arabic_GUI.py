import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
import pytesseract
import pyperclip
import arabic_reshaper
from bidi.algorithm import get_display
import arabicnlp.core as nlp_core
import arabicnlp.data as nlp_data
import arabicnlp.correction as nlp_correction
import arabicnlp.porter as nlp_porter
import arabicnlp.pos_tagger as nlp_pos_tagger

# Function to extract text from image
def extract_text():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            image = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(image, lang='ara')
            processed_text = preprocess_arabic_text(extracted_text)
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, processed_text)
            display_image(image)
            status_bar.config(text="Text extracted successfully.", fg="#2ecc71")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text: {str(e)}")

# Function to preprocess Arabic text
def preprocess_arabic_text(text):
    # Normalize Arabic text and shape it for correct display
    reshaped_text = arabic_reshaper.reshape(text)
    # Apply bidi algorithm for correct text direction
    processed_text = get_display(reshaped_text)
    # Example of using ArabicNLP functionalities
    # You can replace these with actual text processing tasks from ArabicNLP
    processed_text = nlp_correction.correct(processed_text)
    processed_text = nlp_core.remove_diacritics(processed_text)
    processed_text = nlp_porter.stem(processed_text)
    # You can explore other functionalities from ArabicNLP as needed
    return processed_text

# Function to display selected image
def display_image(image):
    img_label.config(image='')
    image.thumbnail((300, 300))
    img = ImageTk.PhotoImage(image)
    img_label.config(image=img)
    img_label.image = img

# Function to clear extracted text
def clear_text():
    text_output.delete(1.0, tk.END)
    img_label.config(image='')
    status_bar.config(text="", fg="#333")

# Function to copy text to clipboard
def copy_text():
    text = text_output.get(1.0, tk.END)
    pyperclip.copy(text)
    status_bar.config(text="Text copied to clipboard.", fg="#2ecc71")

# Create the main window
root = tk.Tk()
root.title("Arabic Text Extraction")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

# Custom Fonts
title_font = ("Helvetica", 18, "bold")
button_font = ("Helvetica", 12)

# Create a frame for the widgets
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Create a button to select image
select_button = tk.Button(frame, text="Select Image", command=extract_text, font=button_font, bg="#3498db", fg="#ffffff", relief=tk.FLAT)
select_button.grid(row=0, column=0, padx=(0, 5), pady=(0, 10), sticky="ew")

# Create a button to clear text
clear_button = tk.Button(frame, text="Clear Text", command=clear_text, font=button_font, bg="#e74c3c", fg="#ffffff", relief=tk.FLAT)
clear_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 10), sticky="ew")

# Create a button to copy text
copy_button = tk.Button(frame, text="Copy Text", command=copy_text, font=button_font, bg="#2ecc71", fg="#ffffff", relief=tk.FLAT)
copy_button.grid(row=0, column=2, padx=(0, 5), pady=(0, 10), sticky="ew")

# Create a label for displaying the image
img_label = tk.Label(root, bg="#ffffff", bd=3, relief=tk.SUNKEN)
img_label.pack(pady=10)

# Create a text widget with scrollbars to display extracted text
text_output = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD, bg="#ffffff", fg="#333", relief=tk.FLAT)
text_output.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Create a status bar
status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#f0f0f0", fg="#333")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Run the application
root.mainloop()
