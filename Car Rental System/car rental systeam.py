import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector


# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RAHUL123",
        database="car_rental_system"
    )


# ---------------- MAIN CLASS ----------------
class CarRentalSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental Management System")
        self.root.geometry("1200x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        title = ctk.CTkLabel(root, text="CAR RENTAL SYSTEM",
                             font=("Arial Black", 28, "bold"))
        title.pack(pady=10)

        self.create_dashboard()
        self.create_search()
        self.create_table()
        self.create_form()

        self.fetch_data()
        self.update_dashboard()

    # ---------------- DASHBOARD ----------------
    def create_dashboard(self):
        dash = ctk.CTkFrame(self.root)
        dash.pack(fill="x", padx=20, pady=5)

        self.lbl_total = ctk.CTkLabel(dash, text="Total Cars: 0", font=("Arial", 16))
        self.lbl_total.grid(row=0, column=0, padx=20)

        self.lbl_available = ctk.CTkLabel(dash, text="Available: 0", font=("Arial", 16))
        self.lbl_available.grid(row=0, column=1, padx=20)

        self.lbl_rented = ctk.CTkLabel(dash, text="Rented: 0", font=("Arial", 16))
        self.lbl_rented.grid(row=0, column=2, padx=20)

        self.lbl_return_today = ctk.CTkLabel(dash, text="Returning Today: 0", font=("Arial", 16))
        self.lbl_return_today.grid(row=0, column=3, padx=20)

    # ---------------- SEARCH ----------------
    def create_search(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="x", padx=20, pady=5)

        self.search_var = tk.StringVar()

        ctk.CTkEntry(frame, textvariable=self.search_var, width=300).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Search", command=self.search_car).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Show All", command=self.fetch_data).pack(side="left", padx=10)

    # ---------------- TABLE ----------------
    def create_table(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Brand", "Year", "Price", "Status",
                   "Fuel", "Seats", "Number")

        self.table = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120)

        self.table.pack(fill="both", expand=True)
        self.table.bind("<ButtonRelease-1>", self.auto_fill)

    # ---------------- FORM ----------------
    def create_form(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="x", padx=20, pady=10)

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_brand = tk.StringVar()
        self.var_year = tk.StringVar()
        self.var_price = tk.StringVar()
        self.var_status = tk.StringVar()
        self.var_fuel = tk.StringVar()
        self.var_seats = tk.StringVar()
        self.var_number = tk.StringVar()

        labels = ["Car Name", "Brand", "Year", "Price/Day",
                  "Status", "Fuel", "Seats", "Car Number"]

        variables = [self.var_name, self.var_brand, self.var_year,
                     self.var_price, self.var_status, self.var_fuel,
                     self.var_seats, self.var_number]

        for i, (label, var) in enumerate(zip(labels, variables)):
            ctk.CTkLabel(frame, text=label).grid(row=i // 4, column=(i % 4) * 2, padx=10, pady=5)

            if label == "Status":
                combo = ttk.Combobox(frame, textvariable=self.var_status,
                                     values=["Available", "Rented"],
                                     state="readonly", width=18)
                combo.grid(row=i // 4, column=(i % 4) * 2 + 1)
                combo.current(0)
            else:
                ctk.CTkEntry(frame, textvariable=var, width=200).grid(
                    row=i // 4, column=(i % 4) * 2 + 1)

        ctk.CTkButton(frame, text="Add Car", command=self.add_car).grid(row=2, column=0, pady=20)
        ctk.CTkButton(frame, text="Update", command=self.update_car).grid(row=2, column=1)
        ctk.CTkButton(frame, text="Delete", command=self.delete_car).grid(row=2, column=2)
        ctk.CTkButton(frame, text="Clear", command=self.clear_form).grid(row=2, column=3)

    # ---------------- FUNCTIONS ----------------
    def fetch_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cars")
        rows = cur.fetchall()

        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", tk.END, values=row)

        conn.close()

    def search_car(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM cars WHERE car_name LIKE %s OR brand LIKE %s",
            (f"%{self.search_var.get()}%", f"%{self.search_var.get()}%")
        )
        rows = cur.fetchall()

        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", tk.END, values=row)

        conn.close()

    def add_car(self):
        conn = get_connection()
        cur = conn.cursor()

        # Check duplicate
        cur.execute("SELECT * FROM cars WHERE car_number=%s", (self.var_number.get(),))
        if cur.fetchone():
            messagebox.showerror("Error", "Car number already exists!")
            conn.close()
            return

        try:
            cur.execute("""
                INSERT INTO cars
                (car_name, brand, model_year, price_per_day, status,
                 fuel_type, seating_capacity, car_number)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.var_name.get(),
                self.var_brand.get(),
                self.var_year.get(),
                self.var_price.get(),
                self.var_status.get(),
                self.var_fuel.get(),
                self.var_seats.get(),
                self.var_number.get()
            ))

            conn.commit()
            messagebox.showinfo("Success", "Car Added Successfully")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        conn.close()
        self.fetch_data()
        self.update_dashboard()

    def update_car(self):
        if not self.var_id.get():
            messagebox.showerror("Error", "Select a car first")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE cars SET
            car_name=%s, brand=%s, model_year=%s,
            price_per_day=%s, status=%s,
            fuel_type=%s, seating_capacity=%s,
            car_number=%s
            WHERE car_id=%s
        """, (
            self.var_name.get(),
            self.var_brand.get(),
            self.var_year.get(),
            self.var_price.get(),
            self.var_status.get(),
            self.var_fuel.get(),
            self.var_seats.get(),
            self.var_number.get(),
            self.var_id.get()
        ))

        conn.commit()
        conn.close()
        self.fetch_data()
        self.update_dashboard()

    def delete_car(self):
        if not self.var_id.get():
            messagebox.showerror("Error", "Select a car first")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM cars WHERE car_id=%s", (self.var_id.get(),))
        conn.commit()
        conn.close()

        self.fetch_data()
        self.update_dashboard()
        self.clear_form()

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_brand.set("")
        self.var_year.set("")
        self.var_price.set("")
        self.var_status.set("Available")
        self.var_fuel.set("")
        self.var_seats.set("")
        self.var_number.set("")

    def auto_fill(self, event):
        selected = self.table.selection()
        if selected:
            data = self.table.item(selected[0])["values"]
            self.var_id.set(data[0])
            self.var_name.set(data[1])
            self.var_brand.set(data[2])
            self.var_year.set(data[3])
            self.var_price.set(data[4])
            self.var_status.set(data[5])
            self.var_fuel.set(data[6])
            self.var_seats.set(data[7])
            self.var_number.set(data[8])

    def update_dashboard(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM cars")
        self.lbl_total.configure(text=f"Total Cars: {cur.fetchone()[0]}")

        cur.execute("SELECT COUNT(*) FROM cars WHERE status='Available'")
        self.lbl_available.configure(text=f"Available: {cur.fetchone()[0]}")

        cur.execute("SELECT COUNT(*) FROM cars WHERE status='Rented'")
        self.lbl_rented.configure(text=f"Rented: {cur.fetchone()[0]}")

        cur.execute("""
            SELECT COUNT(*) FROM rentals
            WHERE return_date = CURDATE() AND status='Ongoing'
        """)
        self.lbl_return_today.configure(text=f"Returning Today: {cur.fetchone()[0]}")

        conn.close()


# ---------------- RUN ----------------
root = ctk.CTk()
app = CarRentalSystem(root)
root.mainloop()
