# Brute Force Attack Simulator

A cybersecurity educational tool that demonstrates brute force password attacks.

## Educational Purpose Only
This application is designed for educational and demonstration purposes only. It simulates a brute force attack to demonstrate password security concepts.

## Team
- Authors: Andrae Taylor, Christina Carvalho, Alexander Sekulski
- Course: CSI3480 Summer Project
- Date: 7/24/2025

## Project Structure
```
├── app.py                    # Streamlit web application
├── src/main.py              # Desktop GUI application
├── requirements.txt          # Python dependencies
├── secret_user_info/         # Target password file
└── small-password-list/      # Common passwords for testing
```

## How to Run

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation
1. Clone or download this repository
2. Navigate to the project directory:
   ```
   cd CSI3480-SummerProject-main
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Applications

#### Option 1: Desktop GUI Application (main.py)
Run the desktop version with a graphical user interface:
```
python src/main.py
```

Features:
- Interactive GUI with attack controls
- Real-time attack progress tracking
- 2FA (Two-Factor Authentication) demonstration
- Password strength analysis
- Login testing system
- Attack method selection (Dictionary/Incremental)

#### Option 2: Web Application (app.py)
Run the web-based Streamlit application:
```
streamlit run app.py
```

Features:
- Web-based interface accessible via browser
- Real-time attack simulation
- Password strength analysis
- Educational demonstrations
- Responsive design

## Security Note
This tool is for educational purposes only. Do not use for unauthorized access attempts.