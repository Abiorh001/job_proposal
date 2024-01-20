import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests

endpoint_url = "http://127.0.0.1:8001/generate_proposal"


def generate_proposal():
    # Prepare the data payload from user input
    data = {
        "job_title": job_title_entry.get(),
        "company_name": company_name_entry.get(),
        "job_description": job_description_text.get("1.0", "end-1c"),
        "your_name": your_name_entry.get(),
        "your_contact": your_contact_entry.get()
    }

    # Send the POST request
    response = requests.post(endpoint_url, json=data)

    # Check the HTTP status code
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            response_data = response.json()

            # Display the response in the response_text widget
            response_text.config(state=tk.NORMAL)
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, response_data['response'])
            response_text.config(state=tk.DISABLED)

        except requests.exceptions.JSONDecodeError as json_error:
            print(f"Error decoding JSON: {json_error}")

    else:
        print(f"Request failed with status code: {response.status_code}")


def copy_response():
    response_content = response_text.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(response_content)
    root.update()


# Create the main window
root = tk.Tk()
root.title("Job Proposal Generator")

# Set the window size
root.geometry("500x550")

# Configure column and row weights
for i in range(6):
    root.columnconfigure(i, weight=1)
    root.rowconfigure(i, weight=1)

# Create and set up input fields
job_title_label = ttk.Label(root, text="Job Title:")
job_title_entry = ttk.Entry(root)

company_name_label = ttk.Label(root, text="Company Name:")
company_name_entry = ttk.Entry(root)

job_description_label = ttk.Label(root, text="Job Description:")
job_description_text = tk.Text(root, height=8, width=40)  # Expanded the text widget

your_name_label = ttk.Label(root, text="Your Name:")
your_name_entry = ttk.Entry(root)

your_contact_label = ttk.Label(root, text="Your Contact:")
your_contact_entry = ttk.Entry(root)

# Create and set up the generate button
generate_button = ttk.Button(root, text="Generate Proposal", command=generate_proposal)

# Create the response text widget
response_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
response_label = ttk.Label(root, text="Response:")

# Create the copy response button
copy_response_button = ttk.Button(root, text="Copy Response", command=copy_response)

# Arrange widgets in the grid
job_title_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
job_title_entry.grid(row=0, column=1, columnspan=4, sticky="W", padx=5, pady=5)

company_name_label.grid(row=1, column=0, sticky="W", padx=5, pady=5)
company_name_entry.grid(row=1, column=1, columnspan=4, sticky="W", padx=5, pady=5)

job_description_label.grid(row=2, column=0, sticky="W", padx=5, pady=5)
job_description_text.grid(row=2, column=1, columnspan=4, sticky="W", padx=5, pady=5)

your_name_label.grid(row=3, column=0, sticky="W", padx=5, pady=5)
your_name_entry.grid(row=3, column=1, columnspan=4, sticky="W", padx=5, pady=5)

your_contact_label.grid(row=4, column=0, sticky="W", padx=5, pady=5)
your_contact_entry.grid(row=4, column=1, columnspan=4, sticky="W", padx=5, pady=5)

generate_button.grid(row=5, column=0, columnspan=5, pady=10)

response_label.grid(row=6, column=0, columnspan=5, pady=5)
response_text.grid(row=7, column=0, columnspan=5, pady=5)

# Copy response button
copy_response_button.grid(row=8, column=0, columnspan=5, pady=10)

# Start the main loop
root.mainloop()
