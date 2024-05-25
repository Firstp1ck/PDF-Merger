import logging
import os
from tkinter import filedialog, Tk
from typing import List, Optional
from PyPDF2 import PdfMerger, PdfReader

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_pdfs(paths: List[str], output: str) -> None:
    """Merge multiple PDF files into a single PDF file."""
    merger = PdfMerger()
    
    for path in paths:
        try:
            if os.path.getsize(path) > 0:
                with open(path, 'rb') as fileobj:
                    reader = PdfReader(fileobj)
                    if reader.pages:
                        merger.append(fileobj)
                        logging.info(f"Added {path} to merger.")
                    else:
                        logging.warning(f"The file {path} appears to be a PDF without pages. Skipping.")
            else:
                logging.warning(f"The file {path} is empty. Skipping.")
        except FileNotFoundError:
            logging.error(f"File not found: {path}. Skipping.")
        except Exception as e:
            logging.error(f"Error processing {path}: {e}. Skipping.")
    
    with open(output, 'wb') as fileobj:
        merger.write(fileobj)
        logging.info(f"Merged PDF saved as: {output}")

def select_files() -> Optional[List[str]]:
    """Open a file dialog to select PDFs to merge."""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_paths = filedialog.askopenfilenames(title="Select PDF files to merge", filetypes=[("PDF files", "*.pdf")])
    root.destroy()
    if not file_paths:
        logging.info("No files selected.")
        return None
    return list(file_paths)

def select_save_directory() -> Optional[str]:
    """Open a directory dialog to select the save directory."""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    save_directory = filedialog.askdirectory(title="Select directory to save merged PDF")
    root.destroy()
    if not save_directory:
        logging.info("No directory selected.")
        return None
    return save_directory

def main():
    file_paths = select_files()
    if not file_paths:
        return
    
    save_directory = select_save_directory()
    if not save_directory:
        return
    
    combined_name = '_'.join([os.path.splitext(os.path.basename(path))[0] for path in file_paths]) + '.pdf'
    output_path = os.path.join(save_directory, combined_name)
    merge_pdfs(file_paths, output_path)

if __name__ == "__main__":
    main()
