
import tkinter as tk
from tkinter import messagebox, simpledialog  # Import simpledialog for askstring
import random

class InsufficientFundsError(Exception):
    pass

class Account:
    def __init__(self):
        self.holder_name = ""
        self.account_number = ""
        self.balance = 0
        self.transactions = []
        self.current_otp = None

    def set_account_info(self, holder_name, account_number, initial_balance):
        self.holder_name = holder_name
        self.account_number = account_number
        self.balance = initial_balance
        self.transactions = []  # Reset transactions on setup
        self.add_transaction("Account setup", initial_balance)

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction("Deposit", amount)
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.add_transaction("Withdrawal", -amount)
        return self.balance

    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for transfer.")
        self.balance -= amount
        self.add_transaction(f"Transfer to {recipient_account}", -amount)
        return self.balance

    def add_transaction(self, transaction_type, amount):
        transaction_id = f"TXN{random.randint(100000, 999999)}"
        self.transactions.append(f"{transaction_id} - {transaction_type}: ${amount:.2f}")

    def get_transaction_history(self):
        return "\n".join(self.transactions) if self.transactions else "No transactions."

    def generate_otp(self):
        self.current_otp = str(random.randint(1000, 9999))
        return self.current_otp

def setup_account():
    holder_name = entry_name.get()
    account_number = entry_account.get()
    initial_balance = float(entry_balance.get())
    account.set_account_info(holder_name, account_number, initial_balance)
    messagebox.showinfo("Account Setup", "Account setup complete!")
    update_account_info()

def make_deposit():
    try:
        amount = float(entry_amount.get())
        account.deposit(amount)
        messagebox.showinfo("Deposit", f"Deposit successful! New balance: ${account.balance:.2f}")
        display_receipt("Deposit", amount)
        update_account_info()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")

def make_withdrawal():
    otp_input = simpledialog.askstring("OTP Verification", "Enter OTP:")  # Use simpledialog here
    if otp_input == account.current_otp:
        try:
            amount = float(entry_amount.get())
            remaining_balance = account.withdraw(amount)
            messagebox.showinfo("Withdrawal", f"Withdrawal successful! Remaining balance: ${remaining_balance:.2f}")
            display_receipt("Withdrawal", amount)
            update_account_info()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        except InsufficientFundsError as e:
            messagebox.showerror("Insufficient Funds", str(e))
    else:
        messagebox.showerror("OTP Failed", "Incorrect OTP entered.")

def make_transfer():
    otp_input = simpledialog.askstring("OTP Verification", "Enter OTP:")  # Use simpledialog here
    if otp_input == account.current_otp:
        try:
            amount = float(entry_amount.get())
            recipient_account = entry_recipient.get()
            remaining_balance = account.transfer(amount, recipient_account)
            messagebox.showinfo("Transfer", f"Transfer successful! Remaining balance: ${remaining_balance:.2f}")
            display_receipt("Transfer", amount, recipient_account)
            update_account_info()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        except InsufficientFundsError as e:
            messagebox.showerror("Insufficient Funds", str(e))
    else:
        messagebox.showerror("OTP Failed", "Incorrect OTP entered.")

def display_receipt(transaction_type, amount, recipient_account=None):
    receipt = f"--- Receipt ---\n"
    receipt += f"Transaction Type: {transaction_type}\n"
    if recipient_account:
        receipt += f"Recipient Account: {recipient_account}\n"
    receipt += f"Amount: ${amount:.2f}\n"
    receipt += f"Remaining Balance: ${account.balance:.2f}\n"
    receipt += f"----------------"
    messagebox.showinfo("Receipt", receipt)

def generate_and_display_otp():
    otp = account.generate_otp()
    messagebox.showinfo("Generated OTP", f"Your OTP is: {otp}")

def update_account_info():
    account_info_label.config(text=f"Account Holder: {account.holder_name}\nAccount Number: {account.account_number}\nBalance: ${account.balance:.2f}")
    transaction_history_label.config(text=account.get_transaction_history())

# GUI setup
root = tk.Tk()
root.title("Bank Account Setup, Deposit, Withdrawal, and Transfer")
root.geometry("500x700")
root.config(bg="#f0f0f5")

account = Account()

# Account Setup
label_title = tk.Label(root, text="Account Setup", font=("Helvetica", 16, "bold"), bg="#f0f0f5")
label_title.pack(pady=10)

frame_setup = tk.Frame(root, bg="#f0f0f5")
frame_setup.pack(pady=10)

label_name = tk.Label(frame_setup, text="Account Holder Name:", bg="#f0f0f5")
label_name.grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_setup, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_account = tk.Label(frame_setup, text="Account Number:", bg="#f0f0f5")
label_account.grid(row=1, column=0, padx=5, pady=5)
entry_account = tk.Entry(frame_setup, width=30)
entry_account.grid(row=1, column=1, padx=5, pady=5)

label_balance = tk.Label(frame_setup, text="Initial Balance:", bg="#f0f0f5")
label_balance.grid(row=2, column=0, padx=5, pady=5)
entry_balance = tk.Entry(frame_setup, width=30)
entry_balance.grid(row=2, column=1, padx=5, pady=5)

button_setup = tk.Button(root, text="Set Up Account", command=setup_account, bg="#4CAF50", fg="white", width=20)
button_setup.pack(pady=10)

# Account Information Display
account_info_label = tk.Label(root, text="Account Details", font=("Helvetica", 14), bg="#f0f0f5")
account_info_label.pack(pady=10)

# Transaction Section
label_transaction = tk.Label(root, text="Transaction", font=("Helvetica", 14, "bold"), bg="#f0f0f5")
label_transaction.pack(pady=10)

frame_transaction = tk.Frame(root, bg="#f0f0f5")
frame_transaction.pack(pady=5)

label_amount = tk.Label(frame_transaction, text="Amount:", bg="#f0f0f5")
label_amount.grid(row=0, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_transaction, width=20)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

label_recipient = tk.Label(frame_transaction, text="Recipient Acc:", bg="#f0f0f5")
label_recipient.grid(row=0, column=2, padx=5, pady=5)
entry_recipient = tk.Entry(frame_transaction, width=20)
entry_recipient.grid(row=0, column=3, padx=5, pady=5)


# Transaction Buttons
frame_buttons = tk.Frame(root, bg="#f0f0f5")
frame_buttons.pack(pady=5)

button_deposit = tk.Button(frame_buttons, text="Deposit", command=make_deposit, bg="#3CB371", fg="white", width=10)
button_deposit.grid(row=0, column=0, padx=5)

button_withdraw = tk.Button(frame_buttons, text="Withdraw", command=make_withdrawal, bg="#FF5722", fg="white", width=10)
button_withdraw.grid(row=0, column=1, padx=5)

button_transfer = tk.Button(frame_buttons, text="Transfer", command=make_transfer, bg="#1E90FF", fg="white", width=10)
button_transfer.grid(row=0, column=2, padx=5)

# Generate OTP Button
button_generate_otp = tk.Button(root, text="Generate OTP", command=generate_and_display_otp, bg="#FFA500", fg="white", width=20)
button_generate_otp.pack(pady=10)

# Transaction History
label_transactions = tk.Label(root, text="Transaction History", font=("Helvetica", 14), bg="#f0f0f5")
label_transactions.pack(pady=10)

transaction_history_label = tk.Label(root, text="No transactions.", bg="#f0f0f5", font=("Helvetica", 10))
transaction_history_label.pack()

root.mainloop()
