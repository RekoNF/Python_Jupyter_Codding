# ...existing code...
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

class CoffeeCassierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Code Cassier")
        self.root.geometry("900x700")

        self.coffee_menu = {
            "Espresso": 2.50,
            "Latte": 3.50,
            "Cappuccino": 3.00,
            "Mocha": 4.00,
            "Americano": 2.00,
        }

        self.non_coffee_menu = {
            "Iced Tea": 1.50,
            "Milk Tea": 3.00,
            "Soda": 1.50,
            "Thai Tea": 3.00,
        }

        self.snack_menu = {
            "Cookies & Cream": 5.00,
            "French Fries": 3.00,
            "Chicken Bites": 4.00,
            "Croissant": 2.50,
            "Waffle": 3.00,
            "Cookies": 1.50
        }

        self.orders = []
        self.total_revenue = 0.0

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

        title = ttk.Label(main_frame, text="Coffee Code Cassier", font=("Poppins", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0,10))

        # Coffee selector
        ttk.Label(main_frame, text="Select Coffee:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.coffee_var = tk.StringVar()
        self.coffee_combobox = ttk.Combobox(main_frame, textvariable=self.coffee_var, state="readonly",
                                            values=list(self.coffee_menu.keys()))
        self.coffee_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Non-coffee selector
        ttk.Label(main_frame, text="Select non-Coffee:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.noncoffee_var = tk.StringVar()
        self.noncoffee_combobox = ttk.Combobox(main_frame, textvariable=self.noncoffee_var, state="readonly",
                                               values=list(self.non_coffee_menu.keys()))
        self.noncoffee_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Snack selector
        ttk.Label(main_frame, text="Select Snack:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.snack_var = tk.StringVar()
        self.snack_combobox = ttk.Combobox(main_frame, textvariable=self.snack_var, state="readonly",
                                           values=list(self.snack_menu.keys()))
        self.snack_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Quantity
        ttk.Label(main_frame, text="Quantity:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.qty_var = tk.IntVar(value=1)
        self.qty_spin = tk.Spinbox(main_frame, from_=1, to=100, textvariable=self.qty_var, width=6)
        self.qty_spin.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Order", command=self.place_order).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_selection).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Print Receipt", command=self.print_receipt).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Export to PDF", command=self.export_pdf).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Reset All", command=self.reset_all).grid(row=0, column=4, padx=5)

        # Receipt area
        struk_frame = ttk.LabelFrame(main_frame, text="Struk Pembelian", padding=10)
        struk_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        struk_frame.columnconfigure(0, weight=1)
        struk_frame.rowconfigure(0, weight=1)

        self.receipt_text = tk.Text(struk_frame, wrap="word", height=15, font=("Courier", 10))
        self.receipt_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar = ttk.Scrollbar(struk_frame, orient="vertical", command=self.receipt_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.receipt_text.configure(yscrollcommand=scrollbar.set)

        self.summary_var = tk.StringVar(value="Total Orders: 0 | Total Revenue: $0.00")
        summary_label = ttk.Label(main_frame, textvariable=self.summary_var, anchor="w", font=("Arial", 10, "bold"))
        summary_label.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=(6,0))

    def place_order(self):
        # Determine which menu the user selected
        item = None
        price = None
        name = None

        if self.coffee_var.get():
            name = self.coffee_var.get()
            price = self.coffee_menu.get(name)
        elif self.noncoffee_var.get():
            name = self.noncoffee_var.get()
            price = self.non_coffee_menu.get(name)
        elif self.snack_var.get():
            name = self.snack_var.get()
            price = self.snack_menu.get(name)

        if name is None or price is None:
            messagebox.showwarning("Selection Error", "Please select an item from one of the menus.")
            return

        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except Exception:
            messagebox.showwarning("Input Error", "Quantity harus integer > 0.")
            return

        subtotal = price * qty
        self.orders.append({"type": name, "qty": qty, "price": price, "subtotal": subtotal})
        self.total_revenue += subtotal

        receipt = f"Order #{len(self.orders)}\n"
        receipt += f"  Item : {name}\n"
        receipt += f"  Price: ${price:.2f}\n"
        receipt += f"  Qty  : {qty}\n"
        receipt += f"  Subt : ${subtotal:.2f}\n"
        receipt += "-" * 35 + "\n"

        self.receipt_text.insert(tk.END, receipt)
        self.receipt_text.see(tk.END)

        self.update_summary()
        self.clear_selection()

    def clear_selection(self):
        # Clear all selectors
        self.coffee_combobox.set("")
        self.noncoffee_combobox.set("")
        self.snack_combobox.set("")
        self.qty_var.set(1)

    def update_summary(self):
        self.summary_var.set(f"Total Orders: {len(self.orders)} | Total Revenue: ${self.total_revenue:.2f}")

    def print_receipt(self):
        if not self.orders:
            messagebox.showwarning("Warning", "Tidak ada pesanan untuk dicetak.")
            return

        receipt_content = self.get_full_receipt()
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, receipt_content)
        messagebox.showinfo("Print", "Struk siap dicetak. Gunakan Ctrl+P untuk print atau Export to PDF.")

    def export_pdf(self):
        if not self.orders:
            messagebox.showwarning("Warning", "Tidak ada pesanan untuk diexport.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        if not file_path:
            return

        try:
            self.create_pdf(file_path)
            messagebox.showinfo("Success", f"PDF berhasil disimpan:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat PDF:\n{e}")

    def create_pdf(self, file_path):
        doc = SimpleDocTemplate(file_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#8B4513'),
            spaceAfter=6,
            alignment=1
        )

        elements.append(Paragraph("COFFEE CODE", title_style))
        elements.append(Paragraph("Receipt / Struk Pembelian", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"<b>Date/Tanggal:</b> {timestamp}", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

        data = [["No.", "Item", "Price", "Qty", "Subtotal"]]
        for i, order in enumerate(self.orders, 1):
            data.append([
                str(i),
                order["type"],
                f"${order['price']:.2f}",
                str(order['qty']),
                f"${order['subtotal']:.2f}"
            ])

        table = Table(data, colWidths=[0.8*inch, 1.5*inch, 0.8*inch, 0.6*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4513')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

        elements.append(Paragraph(f"<b>TOTAL: ${self.total_revenue:.2f}</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("Terima kasih atas pembelian Anda! 😊", styles['Normal']))

        doc.build(elements)

    def get_full_receipt(self):
        receipt = "=" * 40 + "\n"
        receipt += "       COFFEE CODE\n"
        receipt += "       Receipt / Struk\n"
        receipt += "=" * 40 + "\n"
        receipt += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "-" * 40 + "\n"

        for i, order in enumerate(self.orders, 1):
            receipt += f"{i}. {order['type']}\n"
            receipt += f"   Price: ${order['price']:.2f}\n"
            receipt += f"   Qty  : {order['qty']}\n"
            receipt += f"   Sub  : ${order['subtotal']:.2f}\n"
            receipt += "-" * 40 + "\n"

        receipt += f"TOTAL REVENUE: ${self.total_revenue:.2f}\n"
        receipt += "=" * 40 + "\n"
        receipt += "Thank you! 😊\n"
        return receipt

    def reset_all(self):
        if messagebox.askyesno("Confirm", "Reset semua pesanan?"):
            self.orders = []
            self.total_revenue = 0.0
            self.receipt_text.delete(1.0, tk.END)
            self.update_summary()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeCassierApp(root)
    root.mainloop()
# ...existing code...