import os
from tkinter import Tk, filedialog, Button, Label, Frame, StringVar, OptionMenu, messagebox
from PIL import Image
from PyPDF2 import PdfMerger

def convert_images_to_pdf():
    # Open a file dialog to select images
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    
    if not file_paths:
        return
    
    images = []
    for file_path in file_paths:
        img = Image.open(file_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        if orientation_var.get() == 'Landscape':
            img = img.rotate(90, expand=True)
        images.append(img)
    
    # Ask the user to select the location to save the PDF
    pdf_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if pdf_path:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        status_label.config(text=f"PDF saved at {pdf_path}")

def merge_pdfs():
    # Open a file dialog to select PDF files
    pdf_paths = filedialog.askopenfilenames(
        title="Select PDF Files to Merge",
        filetypes=[("PDF Files", "*.pdf")]
    )
    
    if len(pdf_paths) < 2:
        status_label.config(text="Please select at least two PDF files.")
        return
    
    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    
    # Ask the user to select the location to save the merged PDF
    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if output_path:
        merger.write(output_path)
        merger.close()
        status_label.config(text=f"Merged PDF saved at {output_path}")

def toggle_theme():
    current_theme = theme_var.get()
    if current_theme == 'Dark':
        root.config(bg="gray")
        frame.config(bg="gray")
        status_label.config(bg="gray", fg="white")
        btn_convert.config(bg="gray", fg="white")
        btn_merge.config(bg="gray", fg="white")
        orientation_menu.config(bg="gray", fg="white")
        theme_menu.config(bg="gray", fg="white")
    else:
        root.config(bg="white")
        frame.config(bg="white")
        status_label.config(bg="white", fg="black")
        btn_convert.config(bg="lightgray", fg="black")
        btn_merge.config(bg="lightgray", fg="black")
        orientation_menu.config(bg="lightgray", fg="black")
        theme_menu.config(bg="lightgray", fg="black")

# Initialize the Tkinter window
root = Tk()
root.title("PDF Tools")
root.geometry("500x450")

# Create a frame to hold the buttons
frame = Frame(root)
frame.pack(pady=20)

# Add a button to convert images to PDF
btn_convert = Button(frame, text="Convert Images to PDF", command=convert_images_to_pdf)
btn_convert.grid(row=0, column=0, padx=10)

# Add a button to merge PDFs
btn_merge = Button(frame, text="Merge PDFs", command=merge_pdfs)
btn_merge.grid(row=0, column=1, padx=10)

# Add a dropdown menu to select orientation
orientation_var = StringVar(value="Portrait")
orientation_menu = OptionMenu(frame, orientation_var, "Portrait", "Landscape")
orientation_menu.grid(row=1, column=0, columnspan=2, pady=10)

# Add a label to show the status
status_label = Label(root, text="")
status_label.pack(pady=10)

# Add a dropdown menu to select theme
theme_var = StringVar(value="Light")
theme_menu = OptionMenu(root, theme_var, "Light", "Dark", command=lambda _: toggle_theme())
theme_menu.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
