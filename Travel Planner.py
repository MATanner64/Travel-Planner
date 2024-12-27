# Matt Tanner
# CIS289 Python II Final Project
# Travel Planner v1.0
# Dec 11th, 2024
# matanner3@dmacc.edu

import tkinter as tk
from tkinter import Toplevel, messagebox, ttk, Scrollbar, PhotoImage, Frame, Label
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import requests

class TravelApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planner v1.0")
        root.geometry("700x550")

        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('travel_planning.db')
        self.cursor = self.conn.cursor()

        # Create trips table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY,
                city TEXT,
                country TEXT,
                travel_dates TEXT,
                num_people INTEGER,
                total_budget REAL
            )
        ''')

        # Create expenses table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                trip_id INTEGER,
                description TEXT,
                type TEXT,
                quantity INTEGER,
                unit_cost REAL,
                amount REAL,
                FOREIGN KEY (trip_id) REFERENCES trips (id)
            )
        ''')

        self.conn.commit()

        # Create a frame for the photo
        self.photo_frame = tk.Frame(self.root)
        self.photo_frame.pack(fill="both", expand=True)

        # Load and resize the photos
        self.image_paths = [
            "MainMenuImages/Tokyo1.png",
            "MainMenuImages/Rome.jpeg",
            "MainMenuImages/Paris.jpeg",
            "MainMenuImages/SanFran.png",
            "MainMenuImages/NYC.png",
            "MainMenuImages/London.jpeg"
        ]
        self.photos = [ImageTk.PhotoImage(Image.open(img_path).resize((625, 425), Image.Resampling.LANCZOS)) for img_path in self.image_paths]

        # Create the photo label
        self.photo_label = tk.Label(self.photo_frame, image=self.photos[0])
        self.photo_label.pack(expand=True)

        # Set the current image index
        self.current_image = 0

        # Call the fade function
        self.fade_images()

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # Define predefined width and height for the buttons
        button_width = 20  # Predefined width for buttons
        button_height = 2  # Predefined height for buttons

        # Main Menu Buttons
        self.add_trip_button = tk.Button(self.button_frame, text="Add New Trip", command=self.open_add_trip_window, width=button_width, height=button_height)
        self.add_trip_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.view_trips_button = tk.Button(self.button_frame, text="View Trips", command=self.view_trips, width=button_width, height=button_height)
        self.view_trips_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.add_expenses_button = tk.Button(self.button_frame, text="Add Expenses", command=self.prompt_for_trip_selection, width=button_width, height=button_height)
        self.add_expenses_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.about_button = tk.Button(self.button_frame, text="About", command=self.show_about_window, width=button_width, height=button_height)
        self.about_button.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        # Configure grid columns to expand evenly
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        # Configure grid rows to have equal weight
        self.button_frame.grid_rowconfigure(0, weight=1)


    def open_add_trip_window(self):
        # Open the Add Trip window
        add_trip_window = Toplevel(self.root)
        add_trip_window.title("Add New Trip")

        # Set the size of the window (width x height)
        add_trip_window.geometry("600x335")

        # Configure grid columns to center widgets
        add_trip_window.grid_columnconfigure(0, weight=1, uniform="equal")
        add_trip_window.grid_columnconfigure(1, weight=3, uniform="equal")

        # Predefined font size
        font_size = 30

        # City Entry
        tk.Label(add_trip_window, text="City:", anchor='w', font=('Helvetica', font_size)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        city_entry = tk.Entry(add_trip_window, font=('Helvetica', font_size))
        city_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        # Country Entry
        tk.Label(add_trip_window, text="Country:", anchor='w', font=('Helvetica', font_size)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        country_entry = tk.Entry(add_trip_window, font=('Helvetica', font_size))
        country_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        # Travel Dates Entry
        tk.Label(add_trip_window, text="Travel Dates:", anchor='w', font=('Helvetica', font_size)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        travel_dates_entry = tk.Entry(add_trip_window, font=('Helvetica', font_size))
        travel_dates_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

        # Number of People Entry
        tk.Label(add_trip_window, text="Number of People:", anchor='w', font=('Helvetica', font_size)).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        num_people_entry = tk.Spinbox(add_trip_window, from_=1, to=100, font=('Helvetica', font_size))
        num_people_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

        # Total Budget Entry
        tk.Label(add_trip_window, text="Total Budget:", anchor='w', font=('Helvetica', font_size)).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        total_budget_entry = tk.Entry(add_trip_window, font=('Helvetica', font_size))
        total_budget_entry.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

        # Submit Button to Save the Data
        def save_trip():
            city = city_entry.get()
            country = country_entry.get()
            travel_dates = travel_dates_entry.get()
            num_people = num_people_entry.get()
            total_budget = total_budget_entry.get()

            if city and country and travel_dates and num_people and total_budget:
                try:
                    # Insert the trip data into the database
                    self.cursor.execute('''
                        INSERT INTO trips (city, country, travel_dates, num_people, total_budget)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (city, country, travel_dates, int(num_people), float(total_budget)))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Trip added successfully!")
                    add_trip_window.destroy()  # Close the window
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save trip: {e}")
            else:
                messagebox.showerror("Error", "Please fill all fields.")

        # Predefined width and height for the buttons
        button_width = 20
        button_height = 2

        # Create the Save Trip button and set the same size as the About button
        submit_button = tk.Button(add_trip_window, text="Save Trip", command=save_trip, width=button_width, height=button_height)
        submit_button.grid(row=5, column=0, pady=5, padx=5, sticky="nsew")

        # Create the Close button to close the add_trip_window
        close_button = tk.Button(add_trip_window, text="Close", command=add_trip_window.destroy, width=button_width, height=button_height)
        close_button.grid(row=5, column=1, pady=5, padx=5, sticky="nsew")

        # Ensure the grid expands evenly for both buttons
        add_trip_window.grid_columnconfigure(0, weight=1)
        add_trip_window.grid_columnconfigure(1, weight=1)

    def prompt_for_trip_selection(self):
        # Create a prompt window to select a trip
        trip_selection_window = Toplevel(self.root)
        trip_selection_window.title("Select a Trip")

        # Fetch all trips from the database
        self.cursor.execute("SELECT id, city, country FROM trips")
        trips = self.cursor.fetchall()

        if not trips:
            messagebox.showinfo("No Trips", "No trips available. Please add a trip first.")
            return

        # Display trips in a listbox with trip IDs
        trip_listbox = tk.Listbox(trip_selection_window)
        for trip in trips:
            trip_listbox.insert(tk.END, f"{trip[0]}: {trip[1]}, {trip[2]}")  # Format: ID: City, Country
        trip_listbox.pack(padx=10, pady=10)

        # Button to proceed to add expenses
        def add_expenses():
            selected_trip = trip_listbox.curselection()
            if selected_trip:
                trip_id = trips[selected_trip[0]][0]
                trip_selection_window.destroy()
                self.open_add_expenses_window(trip_id)
            else:
                messagebox.showerror("Error", "Please select a trip.")

        select_button = tk.Button(trip_selection_window, text="Select Trip", command=add_expenses)
        select_button.pack(pady=10)

    def open_add_expenses_window(self, trip_id):
        # Open the Add Expenses window
        add_expenses_window = Toplevel(self.root)
        add_expenses_window.title("Travel Budget")

        # Fetch trip details for the header
        self.cursor.execute("SELECT city, country, total_budget FROM trips WHERE id=?", (trip_id,))
        trip_details = self.cursor.fetchone()
        city, country, total_budget = trip_details

        # Assuming trip_id is already defined or passed to the function
        self.cursor.execute("SELECT travel_dates, num_people FROM trips WHERE id=?", (trip_id,))
        trip_data = self.cursor.fetchone()

        if trip_data:
            travel_dates, num_people = trip_data
        else:
            travel_dates, num_people = "N/A", "N/A"

        # Heading with additional trip info
        header_label = tk.Label(
            add_expenses_window, 
            text=f"Travel Budget - {city}, {country}\nDates: {travel_dates} Travelers: {num_people}", 
            font=("Arial", 40, "bold")
        )
        header_label.pack(pady=10, padx=10)


        # Create a frame to hold both the budget info and pie chart side by side
        main_frame = tk.Frame(add_expenses_window)
        main_frame.pack(pady=1)

        # Left frame for the budget information
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Create a top frame inside the left frame for "My Budget & Expenses"
        top_frame = tk.Frame(left_frame)
        top_frame.pack(fill="x", pady=1)

        # Centered "My Budget & Expenses" label
        tk.Label(top_frame, text="My Budget & Expenses", font=("Arial", 41, "bold"), anchor='w').pack(pady=1, padx=1)

        # Create the middle frame inside the left frame for budget details
        middle_frame = tk.Frame(left_frame)
        middle_frame.pack(fill="x", pady=10)

        # Create two frames: one for the left side and one for the right side
        middle_left_frame = tk.Frame(middle_frame)
        middle_left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        middle_right_frame = tk.Frame(middle_frame)
        middle_right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # "Total Budget" label and value with white background (left side)
        tk.Label(middle_left_frame, text="Total Budget", font=("Arial", 30)).grid(row=0, column=0, padx=9, pady=5, sticky='w')
        tk.Label(middle_right_frame, text=f"${total_budget:,.2f}", font=("Arial", 14, "bold"), bg="black", fg="white", width=23, height=2, relief="solid", anchor="center").grid(row=0, column=0, padx=6, pady=6, sticky='w')

        # Fetch total expenses for the selected trip
        self.cursor.execute("SELECT SUM(amount) FROM expenses WHERE trip_id=?", (trip_id,))
        total_expenses = self.cursor.fetchone()[0] or 0.0
        difference = total_budget - total_expenses

        # "Total Expenses" label and value with white background (left side)
        tk.Label(middle_left_frame, text="Total Expenses", font=("Arial", 30)).grid(row=1, column=0, padx=9, pady=5, sticky='w')
        total_expenses_label = tk.Label(middle_right_frame, text=f"${total_expenses:,.2f}", font=("Arial", 14, "bold"), bg="black", fg="white", width=23, height=2, relief="solid", anchor="center")
        total_expenses_label.grid(row=1, column=0, padx=6, pady=6, sticky='w')

        # "Difference" label and value with white background (left side)
        tk.Label(middle_left_frame, text="Difference", font=("Arial", 30)).grid(row=2, column=0, padx=9, pady=5, sticky='w')
        difference_label = tk.Label(middle_right_frame, text=f"${difference:,.2f}", font=("Arial", 14, "bold"), bg="black", fg="white", width=23, height=2, relief="solid", anchor="center")
        difference_label.grid(row=2, column=0, padx=6, pady=6, sticky='w')


        # Create a bottom frame inside the left frame for buttons
        bottom_frame = tk.Frame(left_frame)
        bottom_frame.pack(fill="x", pady=20)

        # Create a bottom left frame for the buttons
        bottom_left_frame = tk.Frame(bottom_frame)
        bottom_left_frame.pack(side="left", fill="y", padx=10)

        # Create a bottom right frame
        bottom_right_frame = tk.Frame(bottom_frame)
        bottom_right_frame.pack(side="right", fill="y", padx=10)

        # Function to open Wikivoyage page
        def open_wikivoyage_page():
            city_name = city
            if city_name:
                formatted_city = city_name.replace(" ", "_")  # Format city name for the URL
                url = f"https://en.wikivoyage.org/wiki/{formatted_city}"
                webbrowser.open(url)

        # Function to open Google Maps page
        def open_google_maps_page():
            city_name = city
            if city_name:
                formatted_city = city_name.replace(" ", "+")  # Format city name for the URL
                url = f"https://www.google.com/maps/place/{formatted_city}"
                webbrowser.open(url)

        # Set the width and height for both buttons
        button_width = 22
        button_height = 2

        # Add buttons to the bottom left frame
        wikivoyage_button = tk.Button(bottom_left_frame, text="Open Wikivoyage Page", font=("Arial", 14), command=open_wikivoyage_page, width=button_width, height=button_height)
        wikivoyage_button.pack(side="top", anchor="center", pady=5, padx=9)

        googlemaps_button = tk.Button(bottom_left_frame, text="Open Google Maps", font=("Arial", 14), command=open_google_maps_page, width=button_width, height=button_height)
        googlemaps_button.pack(side="top", anchor="center", pady=5, padx=9)


        # Function to fetch weather data
        def get_weather(city):
            api_key = 'Enter API Key Here'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'
            response = requests.get(url)
            data = response.json()

            if data['cod'] == 200:
                weather_info = f"Weather in {city}:\n"
                weather_info += f"Temperature: {data['main']['temp']}°F\n"
                weather_info += f"Weather: {data['weather'][0]['description']}"
                return weather_info
            else:
                return "City not found or API error."

        
        weather_info = get_weather(city)  # Get the weather data for the selected city
        weather_label = tk.Label(bottom_right_frame, text=weather_info, font=("Arial", 18))

        # Pack the label in the center of the frame
        weather_label.pack(expand=True, pady=5, padx=10)  # This makes the label expand and center both horizontally and vertically

        # Store labels for updating
        self.total_expenses_label = total_expenses_label
        self.difference_label = difference_label

        # Right frame for the pie chart
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=0, fill="both", expand=True)

        # Pie chart for expenses (grouped by type)
        self.cursor.execute("""
            SELECT type, SUM(amount) 
            FROM expenses 
            WHERE trip_id=? 
            GROUP BY type
        """, (trip_id,))
        expenses_data = self.cursor.fetchall()

        if expenses_data:
            labels = [expense[0] for expense in expenses_data]
            sizes = [expense[1] for expense in expenses_data]
        else:
            labels = ['No Expenses']
            sizes = [1]

        # Create a pie chart (make it smaller by adjusting the figure size)
        fig, ax = plt.subplots(figsize=(4.5, 3.7))
        ax.pie(sizes, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

        # Add a legend
        ax.legend(labels, title="Expense Types", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        # Adjust layout to prevent the legend from being cut off
        plt.tight_layout()

        # Render the pie chart on the canvas
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.get_tk_widget().pack(pady=10, expand=True)

        # Draw the canvas
        canvas.draw()

        # Expense Dataframe (Treeview)
        tree_frame = tk.Frame(add_expenses_window)
        tree_frame.pack(anchor="center", pady=5, padx=55)

        tree = ttk.Treeview(tree_frame, columns=("Expense ID", "Description", "Type", "Quantity", "Unit Cost", "Amount"), show="headings", height=10)
        tree.pack()

        # Set column headings
        tree.heading("Expense ID", text="Expense ID")
        tree.heading("Description", text="Description")
        tree.heading("Type", text="Type")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Unit Cost", text="Unit Cost")
        tree.heading("Amount", text="Amount")

        # Set column widths
        tree.column("Expense ID", width=150)   # Set the width for "Expense ID"
        tree.column("Description", width=150)  # Set the width for "Description"
        tree.column("Type", width=150)         # Set the width for "Type"
        tree.column("Quantity", width=150)     # Set the width for "Quantity"
        tree.column("Unit Cost", width=150)    # Set the width for "Unit Cost"
        tree.column("Amount", width=150)       # Set the width for "Amount"

        # Fetch data from database and insert into Treeview
        self.cursor.execute("SELECT id, description, type, quantity, unit_cost, amount FROM expenses WHERE trip_id=?", (trip_id,))
        for expense in self.cursor.fetchall():
            tree.insert("", "end", values=expense)

        # Expense Form Frame (Left and Right)
        expense_form_frame = tk.Frame(add_expenses_window)
        expense_form_frame.pack(pady=5)

        # Create two frames: one for the left side (entries) and one for the right side (buttons)
        left_frame = tk.Frame(expense_form_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        right_frame = tk.Frame(expense_form_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        # Predefined font size
        font_size = 20

        # Left Frame - Expense Entries

        # Description Entry
        tk.Label(left_frame, text="Description:", anchor='w', font=('Helvetica', font_size)).grid(row=0, column=0, sticky='w', padx=3, pady=3)
        description_entry = tk.Entry(left_frame, font=('Helvetica', font_size))
        description_entry.grid(row=0, column=1, sticky='ew', padx=3, pady=3)

        # Type Dropdown (Combobox)
        tk.Label(left_frame, text="Type:", anchor='w', font=('Helvetica', font_size)).grid(row=1, column=0, sticky='w', padx=3, pady=3)
        type_entry = ttk.Combobox(left_frame, values=["Transportation", "Lodging", "Food", "Entertainment", "Other"], font=('Helvetica', font_size))
        type_entry.grid(row=1, column=1, sticky='ew', padx=3, pady=3)

        # Quantity Entry
        tk.Label(left_frame, text="Quantity:", anchor='w', font=('Helvetica', font_size)).grid(row=2, column=0, sticky='w', padx=3, pady=3)
        quantity_entry = tk.Entry(left_frame, font=('Helvetica', font_size))
        quantity_entry.grid(row=2, column=1, sticky='ew', padx=3, pady=3)

        # Unit Cost Entry
        tk.Label(left_frame, text="Unit Cost:", anchor='w', font=('Helvetica', font_size)).grid(row=3, column=0, sticky='w', padx=3, pady=3)
        unit_cost_entry = tk.Entry(left_frame, font=('Helvetica', font_size))
        unit_cost_entry.grid(row=3, column=1, sticky='ew', padx=3, pady=3)

        def add_expense_to_db():
            description = description_entry.get()
            expense_type = type_entry.get()  # Get selected value from dropdown
            quantity = quantity_entry.get()
            unit_cost = unit_cost_entry.get()

            if description and expense_type and quantity and unit_cost:
                try:
                    # Validate and convert input values
                    quantity = int(quantity)
                    unit_cost = float(unit_cost)
                    amount = quantity * unit_cost

                    # Insert into the database
                    self.cursor.execute('''
                        INSERT INTO expenses (trip_id, description, type, quantity, unit_cost, amount)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (trip_id, description, expense_type, quantity, unit_cost, amount))
                    self.conn.commit()

                    # Fetch the ID of the newly inserted expense
                    expense_id = self.cursor.lastrowid

                    # Clear form fields
                    description_entry.delete(0, tk.END)
                    type_entry.set("")  # Clear dropdown
                    quantity_entry.delete(0, tk.END)
                    unit_cost_entry.delete(0, tk.END)

                    # Update the treeview with the new expense (include Expense ID)
                    tree.insert("", "end", values=(expense_id, description, expense_type, quantity, unit_cost, amount))

                    # Update the budget labels
                    self.update_budget_labels(trip_id, total_budget)

                    # Update pie chart
                    self.update_pie_chart(trip_id, canvas, fig, ax)

                    messagebox.showinfo("Success", "Expense added successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add expense: {e}")
            else:
                messagebox.showerror("Error", "Please fill all fields.")

        # Right Frame - Buttons

        # Submit button for adding expense
        submit_expense_button = tk.Button(right_frame, text="Add Expense", command=add_expense_to_db, width=20, height=2, font=("Arial", 12))
        submit_expense_button.grid(row=0, column=0, padx=5, pady=10, sticky='ew')

        # Close button for closing the add_expenses_window
        close_button = tk.Button(right_frame, text="Close", command=add_expenses_window.destroy, width=20, height=2, font=("Arial", 12))
        close_button.grid(row=2, column=0, padx=5, pady=10, sticky='ew')

        def delete_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select an expense to delete.")
                return

            # Prompt for confirmation before deleting
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure? This cannot be undone.")
            if confirmation:
                item_id = tree.item(selected_item)["values"][0]
                try:
                    # Delete from the expenses table in the database
                    self.cursor.execute("DELETE FROM expenses WHERE id=?", (item_id,))
                    self.conn.commit()

                    tree.delete(selected_item)

                    # Fetch the remaining expenses to update the pie chart and total expenses
                    self.update_pie_chart(trip_id, canvas, fig, ax)  # Update the pie chart
                    self.update_budget_labels(trip_id, total_budget)  # Update the labels with new budget data

                    messagebox.showinfo("Deleted", "Expense deleted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting expense: {e}")
            else:
                messagebox.showinfo("Cancelled", "Expense deletion cancelled.")


        # Delete button for deleting an expense
        delete_button = tk.Button(right_frame, text="Delete Expense", font=("Arial", 12), command=delete_selected, width=20, height=2)
        delete_button.grid(row=1, column=0, padx=5, pady=10, sticky='ew')   

    def update_pie_chart(self, trip_id, canvas, fig, ax):
        # Group expenses by type and sum amounts
        self.cursor.execute("""
            SELECT type, SUM(amount) 
            FROM expenses 
            WHERE trip_id=? 
            GROUP BY type
        """, (trip_id,))
        expenses_data = self.cursor.fetchall()

        if expenses_data:
            labels = [expense[0] for expense in expenses_data]  # Expense types (categories)
            sizes = [expense[1] for expense in expenses_data]   # Total amounts
        else:
            labels = ['No Expenses']
            sizes = [1]

        # Clear the existing chart
        ax.clear()

        # Create a pie chart with updated figure size
        ax.pie(sizes, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

        # Add a legend for expense types
        ax.legend(labels, title="Expense Types", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')

        # Adjust layout to prevent the legend from being cut off
        plt.tight_layout()

        # Draw the updated pie chart on the canvas
        canvas.draw()



    def update_budget_labels(self, trip_id, total_budget):
        # Fetch updated totals from the database after an expense deletion
        self.cursor.execute("SELECT SUM(amount) FROM expenses WHERE trip_id=?", (trip_id,))
        new_total_expenses = self.cursor.fetchone()[0] or 0.0
        new_difference = total_budget - new_total_expenses

        # Update the labels
        self.total_expenses_label.config(text=f"${new_total_expenses:,.2f}")
        self.difference_label.config(text=f"${new_difference:,.2f}")


    def view_trips(self):
        # Open the View Trips window
        view_window = Toplevel(self.root)
        view_window.title("View Trips")

        # Create a Treeview widget to display the trips
        tree = ttk.Treeview(view_window, columns=("ID", "City", "Country", "Travel Dates", "People", "Budget"), show="headings")
        
        tree.heading("ID", text="ID")
        tree.heading("City", text="City")
        tree.heading("Country", text="Country")
        tree.heading("Travel Dates", text="Travel Dates")
        tree.heading("People", text="Number of People")
        tree.heading("Budget", text="Total Budget")

        tree.grid(row=0, column=0, padx=10, pady=10)

        # Add a scrollbar
        scrollbar = Scrollbar(view_window, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.config(yscrollcommand=scrollbar.set)

        # Fetch the data from the database
        try:
            self.cursor.execute("SELECT * FROM trips")
            rows = self.cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching trips: {e}")

        def on_double_click(event):
            selected_item = tree.selection()
            if not selected_item:
                return

            values = tree.item(selected_item)["values"]
            if values:
                # Open a new window with the current values to edit
                edit_window = Toplevel(view_window)
                edit_window.title("Edit Trip")

                # Set the size of the window (width x height)
                edit_window.geometry("600x335")  # Adjust the width and height as needed

                # Configure grid columns to center widgets
                edit_window.grid_columnconfigure(0, weight=1, uniform="equal")
                edit_window.grid_columnconfigure(1, weight=3, uniform="equal")

                # Predefined font size
                font_size = 30

                # City Entry
                tk.Label(edit_window, text="City:", anchor='w', font=('Helvetica', font_size)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
                city_entry = tk.Entry(edit_window, font=('Helvetica', font_size))
                city_entry.insert(0, values[1])
                city_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

                # Country Entry
                tk.Label(edit_window, text="Country:", anchor='w', font=('Helvetica', font_size)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
                country_entry = tk.Entry(edit_window, font=('Helvetica', font_size))
                country_entry.insert(0, values[2])
                country_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

                # Travel Dates Entry
                tk.Label(edit_window, text="Travel Dates:", anchor='w', font=('Helvetica', font_size)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
                travel_dates_entry = tk.Entry(edit_window, font=('Helvetica', font_size))
                travel_dates_entry.insert(0, values[3])
                travel_dates_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

                # Number of People Entry
                tk.Label(edit_window, text="Number of People:", anchor='w', font=('Helvetica', font_size)).grid(row=3, column=0, sticky='w', padx=5, pady=5)
                num_people_entry = tk.Spinbox(edit_window, from_=1, to=100, font=('Helvetica', font_size))
                num_people_entry.insert(0, values[4])
                num_people_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

                # Total Budget Entry
                tk.Label(edit_window, text="Total Budget:", anchor='w', font=('Helvetica', font_size)).grid(row=4, column=0, sticky='w', padx=5, pady=5)
                total_budget_entry = tk.Entry(edit_window, font=('Helvetica', font_size))
                total_budget_entry.insert(0, values[5])
                total_budget_entry.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

                # Save changes
                def save_changes():
                    city = city_entry.get()
                    country = country_entry.get()
                    travel_dates = travel_dates_entry.get()
                    num_people = num_people_entry.get()
                    total_budget = total_budget_entry.get()

                    if city and country and travel_dates and num_people and total_budget:
                        try:
                            updated_values = (city, country, travel_dates, num_people, total_budget, values[0])
                            self.cursor.execute("""UPDATE trips SET city=?, country=?, travel_dates=?, num_people=?, total_budget=? WHERE id=?""", updated_values)
                            self.conn.commit()
                            self.refresh_treeview(tree)  # Refresh the list
                            edit_window.destroy()  # Close the edit window
                        except Exception as e:
                            messagebox.showerror("Error", f"Error updating trip: {e}")
                    else:
                        messagebox.showerror("Error", "Please fill all fields.")

                # Predefined width and height for the buttons
                button_width = 20
                button_height = 2

                # Create the Save Changes button
                save_button = tk.Button(edit_window, text="Save Changes", command=save_changes, width=button_width, height=button_height)
                save_button.grid(row=5, column=0, pady=5, padx=5, sticky="nsew")

                # Create the Close button to close the edit_window
                close_button = tk.Button(edit_window, text="Close", command=edit_window.destroy, width=button_width, height=button_height)
                close_button.grid(row=5, column=1, pady=5, padx=5, sticky="nsew")

                # Ensure the grid expands evenly for both buttons
                edit_window.grid_columnconfigure(0, weight=1)
                edit_window.grid_columnconfigure(1, weight=1)


        # Bind double-click event to make rows editable
        tree.bind("<Double-1>", on_double_click)

        # Delete the selected row with confirmation
        def delete_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a trip to delete.")
                return

            # Prompt for confirmation before deleting
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure? This cannot be undone.")
            if confirmation:
                item_id = tree.item(selected_item)["values"][0]
                try:
                    # Delete from database
                    self.cursor.execute("DELETE FROM trips WHERE id=?", (item_id,))
                    self.conn.commit()
                    tree.delete(selected_item)
                    messagebox.showinfo("Deleted", "Trip deleted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting trip: {e}")
            else:
                messagebox.showinfo("Cancelled", "Trip deletion cancelled.")

        # Delete Button
        delete_button = tk.Button(view_window, text="Delete Selected Trip", command=delete_selected)
        delete_button.grid(row=1, column=0, padx=10, pady=10)


        # Refresh the Treeview widget to show the latest data
        def refresh_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            try:
                self.cursor.execute("SELECT * FROM trips")
                rows = self.cursor.fetchall()
                for row in rows:
                    tree.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Error fetching trips: {e}")

    def fade_images(self):
        # Switch to the next image in the list
        self.current_image = (self.current_image + 1) % len(self.photos)
        
        # Update the image on the label
        self.photo_label.configure(image=self.photos[self.current_image])

        # Set the transition speed (1000 ms = 1 second)
        self.root.after(3000, self.fade_images)

    def show_about_window(self):
        # Create a simple About window
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x500")

        # Load the image
        image = Image.open("Matt1.png")  # Replace with your image file path
        
        # Scale the image to the size of the label using LANCZOS filter
        image = image.resize((200, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Create a label with the image
        photo_label = tk.Label(about_window, image=photo)
        photo_label.image = photo
        photo_label.pack(pady=10)

        # Add labels with different font styles
        about_label1 = tk.Label(about_window, text="Trip Planner", font=('Helvetica', 30, 'bold'))
        about_label1.pack(pady=5)

        about_label2 = tk.Label(about_window, text="v1.0", font=('Helvetica', 20, 'bold'))
        about_label2.pack(pady=5)

        about_label3 = tk.Label(about_window, text="Created by Matt Tanner", font=('Helvetica', 25, 'bold'))
        about_label3.pack(pady=5)

        # Define predefined width and height for the buttons
        button_width = 20
        button_height = 2

        # Function to reset the database (drop and recreate tables)
        def reset_database():
            # Ask for confirmation before proceeding with the reset
            confirm_reset = messagebox.askyesno(
                "Are you sure?", 
                "This cannot be undone. Do you want to reset the database?"
            )

            if confirm_reset:
                # Drop the existing tables if they exist
                self.cursor.execute('DROP TABLE IF EXISTS expenses')
                self.cursor.execute('DROP TABLE IF EXISTS trips')

                # Recreate the tables
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS trips (
                        id INTEGER PRIMARY KEY,
                        city TEXT,
                        country TEXT,
                        travel_dates TEXT,
                        num_people INTEGER,
                        total_budget REAL
                    )
                ''')

                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        trip_id INTEGER,
                        description TEXT,
                        type TEXT,
                        quantity INTEGER,
                        unit_cost REAL,
                        amount REAL,
                        FOREIGN KEY (trip_id) REFERENCES trips (id)
                    )
                ''')

                # Commit the changes to the database
                self.conn.commit()

                # Show a confirmation message
                messagebox.showinfo("Success", "Database has been reset!")
            else:
                # Show a cancellation message if reset is not confirmed
                messagebox.showinfo("Cancelled", "Database reset was cancelled.")

        # Add a Reset Database button
        reset_button = tk.Button(about_window, text="Reset Database", command=reset_database, width=button_width, height=button_height)
        reset_button.pack(pady=10)

        # Add a close button
        close_button = tk.Button(about_window, text="Close", command=about_window.destroy, width=button_width, height=button_height)
        close_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()
