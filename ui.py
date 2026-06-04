import tkinter as tk
from tkinter import messagebox


class BankingSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Banking System UI")
        self.root.geometry("400x520")
        self.root.configure(bg="#f4f6f9")

        self.balance = 0.00
        self.balance_hidden = True
        self.history = []


        self.title_label = tk.Label(
            root,
            text="PHILIPPINE NATIONAL BANK",
            font=("Helvetica", 16, "bold"),
            bg="#1a365d",
            fg="white",
            pady=15,
        )
        self.title_label.pack(fill=tk.X)

        self.balance_frame = tk.Frame(root, bg="#e2e8f0", bd=2, relief="groove")
        self.balance_frame.pack(pady=20, padx=20, fill=tk.X)

        self.balance_title = tk.Label(
            self.balance_frame,
            text="Current Balance",
            font=("Helvetica", 10),
            bg="#e2e8f0",
            fg="#4a5568",
        )
        self.balance_title.pack(pady=(5, 0))

        self.balance_display = tk.Label(
            self.balance_frame,
            text="₱ *******",
            font=("Helvetica", 18, "bold"),
            bg="#e2e8f0",
            fg="#2d3748",
        )
        self.balance_display.pack(pady=(0, 5))

        self.input_label = tk.Label(
            root,
            text="Enter Amount (₱):",
            font=("Helvetica", 11, "bold"),
            bg="#f4f6f9",
            fg="#4a5568",
        )
        self.input_label.pack(pady=(10, 2))

        self.amount_entry = tk.Entry(
            root, font=("Helvetica", 14), justify="center", bd=2, relief="solid"
        )
        self.amount_entry.pack(pady=5, ipady=4, padx=40, fill=tk.X)

        btn_config = {
            "font": ("Helvetica", 11, "bold"),
            "fg": "white",
            "activebackground": "#2b6cb0",
            "activeforeground": "white",
            "bd": 0,
            "height": 2,
            "cursor": "hand2",
        }

        self.btn_balance = tk.Button(
            root,
            text="Show Balance",
            bg="#4a5568",
            command=self.toggle_balance, 
            **btn_config
        )
        self.btn_balance.pack(pady=6, padx=40, fill=tk.X)

        self.btn_deposit = tk.Button(
            root,
            text="Deposit Money",
            bg="#38a169",
            command=self.deposit,
            **btn_config
        )
        self.btn_deposit.pack(pady=6, padx=40, fill=tk.X)

        self.btn_withdraw = tk.Button(
            root,
            text="Withdraw Money",
            bg="#e53e3e",
            command=self.withdraw,
            **btn_config
        )
        self.btn_withdraw.pack(pady=6, padx=40, fill=tk.X)

        self.btn_history = tk.Button(
            root,
            text="Transaction History",
            bg="#d69e2e",
            command=self.show_history,
            **btn_config
        )
        self.btn_history.pack(pady=6, padx=40, fill=tk.X)

    def toggle_balance(self):
        """Toggles the visibility of the balance and updates button text."""
        if self.balance_hidden:
            self.balance_display.config(text=f"₱{self.balance:,.2f}")
            self.btn_balance.config(text="Hide Balance")
            self.balance_hidden = False
        else:
            self.balance_display.config(text="₱ *******")
            self.btn_balance.config(text="Show Balance")
            self.balance_hidden = True

    def update_balance_ui(self):
        """Helper to refresh the numbers on display if the balance is currently shown."""
        if not self.balance_hidden:
            self.balance_display.config(text=f"₱{self.balance:,.2f}")

    def get_amount(self):
        """Helper function to validate and return the input amount."""
        input_value = self.amount_entry.get().strip()

        if not input_value:
            messagebox.showerror("Error", "Please enter an amount.")
            return None

        try:
            amount = float(input_value)
            if amount <= 0:
                messagebox.showerror(
                    "Error", "Amount must be greater than zero."
                )
                return None
            return amount
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid input. Please enter a valid number."
            )
            return None

    def deposit(self):
        """Adds funds to the balance and records it in transaction history."""
        amount = self.get_amount()
        if amount is not None:
            self.balance += amount
            self.history.append(f"Deposited: +₱{amount:,.2f}")
            
            messagebox.showinfo(
                "Success", f"Successfully deposited ₱{amount:,.2f}"
            )
            self.amount_entry.delete(0, tk.END)
            self.update_balance_ui()

    def withdraw(self):
        """Deducts funds from the balance if sufficient funds exist and records history."""
        amount = self.get_amount()
        if amount is not None:
            if amount > self.balance:
                messagebox.showerror(
                    "Declined", "Insufficient funds for this withdrawal."
                )
            else:
                self.balance -= amount
                
                self.history.append(f"Withdrew: -₱{amount:,.2f}")
                
                messagebox.showinfo(
                    "Success", f"Successfully withdrew ₱{amount:,.2f}"
                )
                self.amount_entry.delete(0, tk.END)
                self.update_balance_ui()

    def show_history(self):
        """Creates a pop-up window showing all historical account activity."""
        if not self.history:
            messagebox.showinfo("History", "No transactions found yet.")
            return

        history_win = tk.Toplevel(self.root)
        history_win.title("Transaction History")
        history_win.geometry("300x350")
        history_win.configure(bg="#f4f6f9")

        label = tk.Label(
            history_win, text="Past Transactions", font=("Helvetica", 12, "bold"), bg="#f4f6f9", pady=10
        )
        label.pack()

        txt_area = tk.Text(history_win, font=("Helvetica", 10), bd=1, relief="solid")
        txt_area.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)

        history_text = "\n".join([f"{i+1}. {record}" for i, record in enumerate(self.history)])
        txt_area.insert(tk.END, history_text)
        txt_area.config(state=tk.DISABLED) 

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()