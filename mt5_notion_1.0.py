import tkinter as tk
from tkinter import messagebox
import MetaTrader5 as mt5
import requests
import json
from datetime import datetime, timedelta
import os

class TradeLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Logger App")

        # Load saved data if available
        self.saved_data = self.load_saved_data()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Instructions Button
        self.instructions_button = tk.Button(self.root, text="Instructions", command=self.show_instructions)
        self.instructions_button.pack(pady=10)

        # Account Number
        self.account_label = tk.Label(self.root, text="Account Number:")
        self.account_label.pack(pady=5)
        self.account_entry = tk.Entry(self.root)
        self.account_entry.pack(pady=5)
        self.account_entry.insert(0, self.saved_data.get("account", ""))  # Load saved account number

        # Password
        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, self.saved_data.get("password", ""))  # Load saved password

        # Server
        self.server_label = tk.Label(self.root, text="Server:")
        self.server_label.pack(pady=5)
        self.server_entry = tk.Entry(self.root)
        self.server_entry.pack(pady=5)
        self.server_entry.insert(0, self.saved_data.get("server", ""))  # Load saved server

        # Notion API Token
        self.notion_token_label = tk.Label(self.root, text="Notion API Token:")
        self.notion_token_label.pack(pady=5)
        self.notion_token_entry = tk.Entry(self.root)
        self.notion_token_entry.pack(pady=5)
        self.notion_token_entry.insert(0, self.saved_data.get("notion_token", ""))  # Load saved Notion token

        # Notion Database ID
        self.notion_db_id_label = tk.Label(self.root, text="Notion Database ID:")
        self.notion_db_id_label.pack(pady=5)
        self.notion_db_id_entry = tk.Entry(self.root)
        self.notion_db_id_entry.pack(pady=5)
        self.notion_db_id_entry.insert(0, self.saved_data.get("notion_db_id", ""))  # Load saved Notion database ID

        # Time Range (Days)
        self.days_label = tk.Label(self.root, text="Fetch Trades from Last X Days:")
        self.days_label.pack(pady=5)
        self.days_entry = tk.Entry(self.root)
        self.days_entry.pack(pady=5)
        self.days_entry.insert(0, "1")  # Default to 1 day

        # Fetch and Log Trades Button
        self.start_button = tk.Button(self.root, text="Fetch and Log Trades", command=self.fetch_and_log_trades)
        self.start_button.pack(pady=20)

    def show_instructions(self):
        instructions = (
            "To set up your Notion database, follow these instructions:\n\n"
            "1. Create a new database in Notion.\n"
            "2. Add the following properties with the exact names:\n\n"
            "- **Entry Time**: Type `Title`\n"
            "- **Entry Level**: Type `Number`\n"
            "- **Sell Level**: Type `Number`\n"
            "- **Quantity**: Type `Number`\n"
            "- **Profit/Loss**: Type `Number`\n\n"
            "3. Copy the Database ID from the URL of the database page and paste it into the 'Notion Database ID' field in this app.\n"
            "4. Generate an Integration Token from Notion and paste it into the 'Notion API Token' field in this app.\n"
            "5. Save your database and ensure your integration has access to it.\n"
        )
        messagebox.showinfo("Notion Setup Instructions", instructions)

    def save_data(self, data):
        with open("saved_data.json", "w") as f:
            json.dump(data, f)

    def load_saved_data(self):
        if os.path.exists("saved_data.json"):
            with open("saved_data.json", "r") as f:
                return json.load(f)
        return {}

    def fetch_and_log_trades(self):
        # Retrieve account details from the entries
        account = self.account_entry.get()
        password = self.password_entry.get()
        server = self.server_entry.get()
        NOTION_TOKEN = self.notion_token_entry.get()
        NOTION_DATABASE_ID = self.notion_db_id_entry.get()
        days = self.days_entry.get()

        # Validate account details
        if not account or not password or not server or not NOTION_TOKEN or not NOTION_DATABASE_ID or not days:
            messagebox.showerror("Error", "Please enter all required details")
            return

        # Save data
        data_to_save = {
            "account": account,
            "password": password,
            "server": server,
            "notion_token": NOTION_TOKEN,
            "notion_db_id": NOTION_DATABASE_ID
        }
        self.save_data(data_to_save)

        # Initialize MetaTrader 5
        if not mt5.initialize():
            messagebox.showerror("Error", "MetaTrader 5 initialization failed")
            mt5.shutdown()
            return

        # Log in to your trading account
        login_status = mt5.login(int(account), password, server=server)
        if not login_status:
            messagebox.showerror("Error", f"Login failed. Error code: {mt5.last_error()}")
            mt5.shutdown()
            return

        # Function to log trade to Notion
        def log_trade_to_notion(entry_time, entry_level, sell_level, points, profit_loss):
            url = "https://api.notion.com/v1/pages"
            headers = {
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }

            data = {
                "parent": {"database_id": NOTION_DATABASE_ID},
                "properties": {
                    "Entry Time": {
                        "title": [
                            {
                                "text": {
                                    "content": entry_time
                                }
                            }
                        ]
                    },
                    "Entry Level": {
                        "number": entry_level
                    },
                    "Sell Level": {
                        "number": sell_level
                    },
                    "Quantity": {
                        "number": points
                    },
                    "Profit/Loss": {
                        "number": profit_loss
                    }
                }
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)

            # Check for detailed errors if any
            try:
                response_json = response.json()
                print("Response JSON:", json.dumps(response_json, indent=2))
            except json.JSONDecodeError:
                print("Failed to decode response as JSON")

        # Function to fetch recent trades and log to Notion
        def fetch_and_log_trades():
            # Fetch trades from the specified time range
            try:
                days_int = int(days)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for the days.")
                return

            to_time = datetime.now()
            from_time = to_time - timedelta(days=days_int)

            trades = mt5.history_deals_get(from_time, to_time)
            if trades is None or len(trades) == 0:
                messagebox.showinfo("Info", "No trades found.")
                return

            for trade in trades:
                # Print trade details for debugging
                print(f"Trade Details - Time: {trade.time}, Price: {trade.price}, Volume: {trade.volume}, Profit: {trade.profit}")

                # Check if the trade has zero profit
                if trade.profit != 0:
                    trade_time = datetime.fromtimestamp(trade.time)
                    entry_time = trade_time.strftime("%m-%d-%A")  # Format as Month-Day-DayOfWeek (e.g., 08-23-Monday)
                    entry_level = trade.price  # Entry level
                    sell_level = trade.price  # Sell level; modify this as needed
                    points = trade.volume  # Adjust this as necessary
                    profit_loss = trade.profit

                    # Log the trade to Notion
                    log_trade_to_notion(entry_time, entry_level, sell_level, points, profit_loss)
                else:
                    # Skip trades with zero profit
                    print(f"Trade with zero profit ignored - Time: {trade.time}, Profit: {trade.profit}")

            # Shutdown MetaTrader 5 when done
            mt5.shutdown()

        # Call the fetch_and_log_trades function
        fetch_and_log_trades()

# Create the main window
root = tk.Tk()
app = TradeLoggerApp(root)
root.mainloop()
