from PyPDF2 import PdfMerger, PdfReader
from tkinter import filedialog, Tk
import os

def merge_pdfs(paths, output):
    merger = PdfMerger()
    
    for path in paths:
        try:
            # Ensure the file is not empty by checking its size
            if os.path.getsize(path) > 0:
                with open(path, 'rb') as fileobj:
                    reader = PdfReader(fileobj)
                    if reader.pages:
                        merger.append(fileobj)
                    else:
                        print(f"The file {path} appears to be a PDF without pages. Skipping.")
            else:
                print(f"The file {path} is empty. Skipping.")
        except Exception as e:
            print(f"Error processing {path}: {e}. Skipping.")
    
    with open(output, 'wb') as fileobj:
        merger.write(fileobj)

def main():
    root = Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    root.attributes('-topmost', True)  # open dialogs on top of other windows

    file_paths = filedialog.askopenfilenames(title="Select PDF files to merge", filetypes=[("PDF files", "*.pdf")])
    if not file_paths:
        print("No files selected, exiting.")
        return

    save_directory = filedialog.askdirectory(title="Select directory to save merged PDF")
    if not save_directory:
        print("No directory selected, exiting.")
        return

    combined_name = '_'.join([os.path.splitext(os.path.basename(path))[0] for path in file_paths]) + '.pdf'
    output_path = os.path.join(save_directory, combined_name)

    merge_pdfs(file_paths, output_path)

    print(f"Merged PDF saved as: {output_path}")

if __name__ == "__main__":
    main()
