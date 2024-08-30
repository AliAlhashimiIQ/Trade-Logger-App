# Trade Logger App
 
## Overview
The **Trade Logger App** is a Python-based GUI application designed to automate the process of logging trades from MetaTrader 5 (MT5) into a Notion database. This app fetches trades executed over a user-specified period and logs them to a Notion database, enabling easy tracking and analysis of your trading performance.

## Features
- Connects to MetaTrader 5 to fetch recent trades.
- Logs trade details to a Notion database.
- Saves your MetaTrader 5 and Notion credentials for easy reuse.
- Simple and intuitive GUI built with Tkinter.

## Requirements
- Python 3.6+
- MetaTrader 5
- A Notion account and an API integration token

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/trade-logger-app.git
    cd trade-logger-app
    ```

2. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application:**
    ```bash
    python trade_logger_app.py
    ```

## Setting Up Notion

1. Create a new database in Notion.
2. Add the following properties with exact names:
   - **Entry Time**: Type `Title`
   - **Entry Level**: Type `Number`
   - **Sell Level**: Type `Number`
   - **Quantity**: Type `Number`
   - **Profit/Loss**: Type `Number`
3. Copy the Database ID from the URL of the database page.
4. Generate an Integration Token from Notion and ensure the integration has access to the database.
5. Paste the Database ID and API token into the app's fields.

## Usage

- Enter your MetaTrader 5 account details, Notion API token, and Notion Database ID in the application.
- Specify the number of days to fetch trades from.
- Click on "Fetch and Log Trades" to start the process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## Acknowledgments

- [MetaTrader 5](https://www.metatrader5.com/en) for their trading platform and API.
- [Notion](https://www.notion.so/) for their powerful productivity tool.

## Contact

For questions or support, please contact (alia20042003@gmail.com).
