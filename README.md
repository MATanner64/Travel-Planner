# Travel Planner

The Travel Planner is a Python-based desktop application designed to simplify travel planning and budgeting. Built using Tkinter for the user interface, the app allows users to manage travel details, track expenses, and visualize their travel plans interactively. This tool is ideal for organizing trip information, budgeting, and planning trips efficiently.

## Features
- User-Friendly Interface: Built with Tkinter, the app offers an intuitive and visually appealing interface for seamless navigation.
- Trip Management: Add new trips with details such as city, country, travel dates, number of people, and total budget. View and edit existing trips with ease.
- Expense Tracking: Record and manage travel-related expenses for each trip, with automatic calculations for total costs based on quantity and unit price.
- Data Storage: Leverages SQLite for persistent storage of trip details and expenses.
- Visualizations: Create insightful expense graphs using Matplotlib, including pie charts for a clear breakdown of spending.
- Web Integration: Features an embedded browser for quick access to travel-related information, including Wikivoyage and Google Maps pages for the selected city.
- Weather Integration: Fetch and display weather information for the selected city to help with travel planning.

## Installation

### Prerequisites
- Python 3.10 or newer
- tkinter (comes pre-installed with Python)
- PIL (Python Imaging Library)
- sqlite3 (built-in with Python)
- matplotlib
- requests

## Steps

1. Clone or download this repository.

2. Install required libraries:

```
pip install pillow matplotlib requests
```

3. Run the script:

```
python Travel\ Planner.py
```

## Usage

1. Launch the application by running the Python script.

<img src="Screenshots/Main Menu.png" alt="Alt text" width="300">

2. Add a Trip:
- Enter details such as city, country, travel dates, number of people, and total budget.

<img src="Screenshots/Add New Trip.png" alt="Alt text" width="300">

3. Track Expenses:
- Add expenses for the trip by specifying the category, quantity, unit cost, and other relevant details.

<img src="Screenshots/Viewing and Adding Expenses.png" alt="Alt text" width="300">

4. Visualize Expenses:
- Use the built-in graph feature to view expense distribution.
  
5. Browse Information:
- Open travel-related websites directly within the application for seamless research.
  
## File Structure
- Travel Planner.py: Main application file containing the code for the Travel Planner.
- database: SQLite database storing trip and expense data (created automatically upon first run).

## Future Enhancements
- Integration with external APIs for real-time flight, hotel, and activity suggestions.
- Enhanced visualizations, including pie charts for expense categories.
- Cross-platform compatibility.
- Mobile-friendly version.
