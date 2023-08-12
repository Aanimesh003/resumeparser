import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import spacy
import fitz  # PyMuPDF

def process_resume():
    # Getting the PDF resume path from the input field
    pdf_path = pdf_path_entry.get()
    
    # Loading the PDF and extracting text
    pdf_document = fitz.open(pdf_path)
    resume_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        resume_text += page.get_text("text")
    pdf_document.close()
    
    # Getting the spaCy model path from the input field
    spacy_model_path = spacy_model_path_entry.get()
    
    # Loading the custom spaCy model
    nlp = spacy.load(spacy_model_path)
    
    # Processing the resume using spaCy
    doc = nlp(resume_text)
    
    # Extracting entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Displaying the extracted entities
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    for entity, label in entities:
        result_text.insert(tk.END, f"Entity: {entity} - Label: {label}\n")
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Resume Entity Extraction")
root.geometry("600x600") 

# Creating and positioning GUI elements
pdf_path_label = tk.Label(root, text="Enter PDF Resume Path:")
pdf_path_label.pack(pady=(10, 0))

pdf_path_entry = tk.Entry(root, width=40)
pdf_path_entry.pack()

spacy_model_path_label = tk.Label(root, text="Enter spaCy Model Path:")
spacy_model_path_label.pack(pady=(10, 0))

spacy_model_path_entry = tk.Entry(root, width=40)
spacy_model_path_entry.pack()

load_pdf_button = tk.Button(root, text="Load PDF", command=lambda: pdf_path_entry.insert(0, filedialog.askopenfilename()))
load_pdf_button.pack(pady=(10, 0))

process_button = tk.Button(root, text="Process Resume", command=process_resume)
process_button.pack(pady=(10, 0))

result_text = scrolledtext.ScrolledText(root, height=10, width=50, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED)
result_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

root.mainloop()
