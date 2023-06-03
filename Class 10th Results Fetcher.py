import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import time

import pdfkit
from pypdf import PdfMerger


# Set the path to wkhtmltopdf executable
wkhtmltopdf_path = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

# Configure pdfkit
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


def fetch_results():
    try:
        os.mkdir(".Results")
    except Exception as e:
        pass


    starting_range = int(start_range_entry.get())
    ending_range = int(end_range_entry.get())

    rollnos = [rollno for rollno in range(starting_range, ending_range + 1)]

    base_url = "http://rajeduboard.rajasthan.gov.in/RESULT2023/SEV/Roll_Output.asp?roll_no="

    def result(rollno):
        try:
            pdfkit.from_url(f"{base_url}{rollno}", os.path.join(os.getcwd(), ".Results", f'{rollno}.pdf'),
                            configuration=config)
            return f'{rollno}.pdf', "Done"
        except Exception as e:
            return e

    print("Fetching Results.....")
    init_time = time.time()

    with ThreadPoolExecutor() as executor:
        results = executor.map(result, rollnos)
        for result in results:
            print(result)

    pdfs = sorted([os.path.join(os.getcwd(), ".Results", pdf) for pdf in os.listdir(os.path.join(os.getcwd(), ".Results"))])

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    output_filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                   filetypes=[("PDF Files", "*.pdf")],
                                                   initialfile=f"RBSE Class 10th Result {rollnos[0]}-{rollnos[-1]}.pdf")
    if output_filename:
        merger.write(output_filename)
        merger.close()
        shutil.rmtree(os.path.join(os.getcwd(), ".Results"), ignore_errors=True)

        final_time = time.time()
        print(f"Results Fetched In: {time.strftime('%H:%M:%S', time.gmtime(final_time - init_time))}")


# Create the Tkinter windowai
window = tk.Tk()
window.title("RBSE Class 10th Results Fetcher")

# Create and place the input fields and labels
start_range_label = tk.Label(window, text="Enter starting range of Roll No.:")
start_range_label.pack()
start_range_entry = tk.Entry(window)
start_range_entry.pack()

end_range_label = tk.Label(window, text="Enter ending range of Roll No.:")
end_range_label.pack()
end_range_entry = tk.Entry(window)
end_range_entry.pack()

# Create the fetch button
fetch_button = tk.Button(window, text="Fetch Results", command=fetch_results)
fetch_button.pack()

# Start the Tkinter event loop
window.mainloop()
