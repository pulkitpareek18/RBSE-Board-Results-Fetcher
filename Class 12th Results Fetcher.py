import os
import shutil
import pdfkit
from PyPDF2 import PdfMerger
from concurrent.futures import ThreadPoolExecutor
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

try:
    os.mkdir(".Results")
except Exception as e:
    pass

try:
    os.mkdir("Output")
except Exception as e:
    pass

# Configure pdfkit to point to the installation of wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

# Function to fetch results
def fetch_results():
    try:
        starting_range = int(start_range_entry.get())
        ending_range = int(end_range_entry.get())

        rollnos = [rollno for rollno in range(starting_range, ending_range + 1)]

        base_urls = [
            "https://rajeduboard.rajasthan.gov.in/RESULT2023/SCIENCE/Roll_Output.asp?roll_no=",
            "https://rajeduboard.rajasthan.gov.in/RESULT2023/COMM/Roll_Output.asp?roll_no=",
            "https://rajeduboard.rajasthan.gov.in/RESULT2023/ARTS/Roll_Output.asp?roll_no="
        ]
        stream_names = ["Science", "Commerce", "Arts"]

        base_url = base_urls[choice_var.get()-1]

        def result(rollno):
            try:
                pdfkit.from_url(f"{base_url}{rollno}",
                                os.path.join(os.getcwd(), ".Results", f'{rollno}.pdf'), configuration=config)
                return f'{rollno}.pdf', "Done"
            except Exception as e:
                return e

        print("Fetching Results.....")
        init_time = time.time()

        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(result, rollnos)
            for result in results:
                print(result)

        pdfs = sorted([os.path.join(os.getcwd(), ".Results", pdf) for pdf in
                       os.listdir(os.path.join(os.getcwd(), ".Results"))])

        merger = PdfMerger()

        for pdf in pdfs:
            merger.append(pdf)

        output_file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                        filetypes=[("PDF Files", "*.pdf")],
                                                        title="Save Output PDF File",
                                                        initialfile=f"RBSE Class 12th {stream_names[choice_var.get()-1]} Result {rollnos[0]}-{rollnos[-1]}.pdf")
        if output_file_path:
            merger.write(output_file_path)
            messagebox.showinfo("Success", "Results fetched and saved successfully!")
        else:
            messagebox.showwarning("Warning", "Output file path not selected. Results fetched but not saved.")

        merger.close()
        shutil.rmtree(os.path.join(os.getcwd(), ".Results"), ignore_errors=True)

        final_time = time.time()
        print(f"Results Fetched In: {time.strftime('%H:%M:%S', time.gmtime(final_time - init_time))}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the tkinter GUI
root = tk.Tk()
root.title("RBSE Class 12th Results Fetcher")

# Create the choice variable
choice_var = tk.IntVar()

# Function to enable/disable input fields based on choice
def update_input_fields():
    if choice_var.get() in [1,2,3]:
        start_range_entry.config(state=tk.NORMAL)
        end_range_entry.config(state=tk.NORMAL)
    else:
        start_range_entry.delete(0, tk.END)
        end_range_entry.delete(0, tk.END)
        start_range_entry.config(state=tk.DISABLED)
        end_range_entry.config(state=tk.DISABLED)


# Create the choice label and radio buttons
choice_label = tk.Label(root, text="Select Stream:")
choice_label.pack()

science_radio = tk.Radiobutton(root, text="Science", variable=choice_var, value=1, command=update_input_fields)
science_radio.pack()

commerce_radio = tk.Radiobutton(root, text="Commerce", variable=choice_var, value=2, command=update_input_fields)
commerce_radio.pack()

arts_radio = tk.Radiobutton(root, text="Arts", variable=choice_var, value=3, command=update_input_fields)
arts_radio.pack()

# Create the roll number range inputs
range_label = tk.Label(root, text="Enter Roll No. Range:")
range_label.pack()

start_range_entry = tk.Entry(root, state=tk.DISABLED)
start_range_entry.pack()

end_range_entry = tk.Entry(root, state=tk.DISABLED)
end_range_entry.pack()

# Create the fetch results button
fetch_button = tk.Button(root, text="Fetch Results", command=fetch_results)
fetch_button.pack()

root.mainloop()
