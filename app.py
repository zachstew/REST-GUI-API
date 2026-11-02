# app.py - Tkinter GUI that collects purchase data and POSTs it as JSON
import json
import tkinter as tk
import urllib.error
import urllib.request
from decimal import Decimal, InvalidOperation
from tkinter import messagebox, ttk

API_URL = "http://localhost:5001/submit"
MAX_PRICE = Decimal("1000.00")

root = tk.Tk()
root.title("Purchase Form")

# ---------- FORM VARIABLES ----------
product_id_var = tk.StringVar()
description_var = tk.StringVar()
price_var = tk.StringVar()
name_var = tk.StringVar()
email_var = tk.StringVar()
online_var = tk.BooleanVar(value=True)  # checked = online, unchecked = in-store

# ---------- LAYOUT ----------
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

fields = [
    ("Product ID:", product_id_var),
    ("Description:", description_var),
    ("Price ($):", price_var),
    ("Customer Name:", name_var),
    ("Customer Email:", email_var),
]
for row, (label, var) in enumerate(fields):
    ttk.Label(frame, text=label).grid(column=0, row=row, sticky=tk.W, pady=2)
    ttk.Entry(frame, width=35, textvariable=var).grid(column=1, row=row, pady=2)

online_cb = ttk.Checkbutton(frame, text="Online purchase (uncheck for in-store)",
                            variable=online_var)
online_cb.grid(columnspan=2, row=len(fields), sticky=tk.W, pady=(6, 0))

submit_btn = ttk.Button(frame, text="Submit", command=lambda: submit_form())
submit_btn.grid(row=len(fields) + 1, columnspan=2, pady=(10, 0))


# ---------- LOCAL VALIDATION ----------
def parse_price():
    """Return the price as a Decimal, or None if it isn't a valid number."""
    try:
        return Decimal(price_var.get().strip()).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None


def validate() -> bool:
    """Return True if all fields are valid; otherwise show an error."""
    if not product_id_var.get().strip():
        messagebox.showerror("Validation Error", "Product ID cannot be empty.")
        return False
    if not description_var.get().strip():
        messagebox.showerror("Validation Error", "Description cannot be empty.")
        return False

    price = parse_price()
    if price is None:
        messagebox.showerror("Validation Error", "Price must be a number, e.g. 19.99.")
        return False
    if price < 0 or price > MAX_PRICE:
        messagebox.showerror("Validation Error",
                             "Price must be between $0.00 and $1,000.00.")
        return False

    if not name_var.get().strip():
        messagebox.showerror("Validation Error", "Customer name cannot be empty.")
        return False

    email = email_var.get().strip()
    if not email or "@" not in email:
        messagebox.showerror("Validation Error", "Enter a valid email address.")
        return False
    return True

# ---------- FORM DATA -> DICT (JSON-ready) ----------
def collect_data() -> dict:
    return {
        "product_id": product_id_var.get().strip(),
        "description": description_var.get().strip(),
        "price": float(parse_price()),
        "name": name_var.get().strip(),
        "email": email_var.get().strip(),
        "online": online_var.get(),
    }

# ---------- POST TO THE API ----------
def submit_form() -> None:
    if not validate():
        return  # abort if validation failed
    json_payload = json.dumps(collect_data()).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=json_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
        messagebox.showinfo("Success", f"Server replied: {result}")
    except urllib.error.HTTPError as e:
        messagebox.showerror("API Error", f"{e.code} -- {e.read().decode()}")
    except Exception as exc:
        messagebox.showerror("Connection Error", str(exc))
# ---------- START THE GUI LOOP ----------
if __name__ == "__main__":
    root.mainloop()