#!/usr/bin/env python3

"""
Project Name: Brute Force Demo Project
Description: Simulates a brute force attack to guess a password
Author: Andrae Taylor, Christina Carvalho, Alexander Sekulski
Date: 7/24/2025
"""

"""
The "rockyou.txt" file is a big text file of most commonly used passwords and it's used
in a lot of official places.
But it's a big file (100MB) and GitHub only allows 25MB upload so a lot had to be deleted.
"""

import time
import random
import customtkinter as ctk
from tkinter import simpledialog, messagebox
import string
from itertools import product

# Constants
COMMON_PASSWORD_LIST = "../small-password-list/smallpasswordlist.txt" #Changed from rockyou file path to secret_password path
TARGET_PASSWORD = "../secret_user_info/secret_password.txt"

def analyze_password_strength(password: str) -> dict:
    """Analyze password strength and provide detailed feedback"""
    if not password:
        return {"strength": "Very Weak", "score": 0, "feedback": ["No password provided"]}
    
    score = 0
    feedback = []
    
    # Length analysis
    if len(password) < 8:
        feedback.append("❌ Too short (less than 8 characters)")
    elif len(password) < 12:
        feedback.append("⚠️ Moderate length (8-11 characters)")
        score += 1
    else:
        feedback.append("✅ Good length (12+ characters)")
        score += 2
    
    # Character variety analysis
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    char_types = sum([has_lower, has_upper, has_digit, has_special])
    if char_types == 1:
        feedback.append("❌ Only one character type used")
    elif char_types == 2:
        feedback.append("⚠️ Two character types used")
        score += 1
    elif char_types == 3:
        feedback.append("✅ Three character types used")
        score += 2
    else:
        feedback.append("✅ All four character types used")
        score += 3
    
    # Common patterns
    if password.lower() in ['password', '123456', 'qwerty', 'admin']:
        feedback.append("❌ Very common password")
        score -= 2
    
    # Overall strength rating
    if score <= 0:
        strength = "Very Weak"
    elif score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    elif score <= 6:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback,
        "length": len(password),
        "char_types": char_types
    }

def generate_incremental_passwords(max_length: int = 4) -> list[str]:
    """Generate passwords using incremental attack method"""
    passwords = []
    chars = string.ascii_lowercase + string.digits  # 36 characters
    
    # Generate all combinations up to max_length
    for length in range(1, max_length + 1):
        # Generate combinations of current length
        for combo in product(chars, repeat=length):
            passwords.append(''.join(combo))
    
    return passwords

def calculate_attack_speed(attempts: int, elapsed_time: float) -> dict:
    """Calculate and format attack speed metrics"""
    if elapsed_time <= 0:
        return {
            "passwords_per_second": 0,
            "passwords_per_minute": 0
        }
    
    passwords_per_second = attempts / elapsed_time
    passwords_per_minute = passwords_per_second * 60
    
    return {
        "passwords_per_second": round(passwords_per_second, 2),
        "passwords_per_minute": round(passwords_per_minute, 2)
    }

def read_passwords_from_file(filename: str) -> list[str]:
    # Read all the words in the text file and adds it to the array for testing.

    try:
        # "rockyou.txt" uses latin-1 encoding so it has to be specified.
        with open(filename, "r", encoding="latin-1") as file:
            return [line.strip() for line in file]
    
    except FileNotFoundError:
        print("Error: File not found!")
        return []
    except Exception as e:
        print(f"An error occured: {e}")
        return []

def get_password(user):
    # Returns the password of the specified user called. Each password increases in complexity.
    user_passwords = {"user1":"123", "user2":"sight", "user3":"horizon372" }
    return user_passwords.get(user, None) # Returns None if username isnt found

def get_password_selection_options() -> dict:
    """Get password selection options for different difficulty levels"""
    password_list = read_passwords_from_file(COMMON_PASSWORD_LIST)
    
    return {
        "Easy (Top of list)": password_list[0] if password_list else "123",  # "123"
        "Medium (Middle of list)": password_list[len(password_list)//2] if password_list else "password",  # Middle password
        "Hard (End of list)": password_list[-1] if password_list else "horizon372",  # "horizon372"
        "Very Hard (Complex)": "meadow408",  # Original target
        "Custom Selection": None  # Will be handled in UI
    }

def perform_2fa(root_window) -> bool:
    """
    Performs 2FA by generating a random 4-digit number and asking user to input it.
    Returns True if user enters correct number, False if they cancel or enter wrong number.
    """

    # Generate random 4-digit number
    random_number = random.randint(1000, 9999)

    # Ask user to input the number
    user_input = simpledialog.askstring(
        "2FA Verification", 
        f"Please type {random_number}:", 
        parent=root_window
    )

    # Check if user cancelled or entered wrong number
    if user_input is None:  # User cancelled
        return False

    try:
        if int(user_input) == random_number:
            return True

        else:
            messagebox.showerror("2FA Failed", "Incorrect number entered!", parent=root_window)
            return False

    except ValueError:
        messagebox.showerror("2FA Failed", "Please enter a valid number!", parent=root_window)
        return False

# Global variables for attack control
attack_paused = False
attack_finished = False

def user_interface():
    root = ctk.CTk() # Initializes the User Interface window
    ctk.set_appearance_mode("dark")
    root.title("Brute Force Attack")
    root.geometry("600x800")  # Made window bigger to accommodate new features
    frame = ctk.CTkFrame(master=root, width=600, height=700) #Sets a frame in the window to utalize a grid for label & button placement
    frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside') #places the frame in the center of the window

    #Creates a checkbox for 2FA option
    twoFACheckbox = ctk.CTkCheckBox(frame, border_color = "black", text="Enable 2FA", font=("Arial", 20), text_color="white")
    twoFACheckbox.grid(column = 0, row = 0, pady = (20,5), padx = 125)

    # Password selection section
    password_selection_label = ctk.CTkLabel(frame, text="Target Password Selection:", font=("Arial", 16), text_color="white")
    password_selection_label.grid(column = 0, row = 1, pady = 5, padx = 10)
    
    # Password difficulty selection
    password_options = get_password_selection_options()
    password_choice_var = ctk.StringVar(value=list(password_options.keys())[0])
    
    def update_selected_password(*args):
        choice = password_choice_var.get()
        if choice == "Custom Selection":
            try:
                custom_index = int(custom_index_var.get())
                password_list = read_passwords_from_file(COMMON_PASSWORD_LIST)
                if 0 <= custom_index < len(password_list):
                    selected_password_label.configure(text=f"Selected: {password_list[custom_index]} (Index: {custom_index})")
                else:
                    selected_password_label.configure(text=f"Selected: -- (Invalid index)")
            except ValueError:
                selected_password_label.configure(text=f"Selected: -- (Invalid index)")
        else:
            target_word = password_options[choice]
            selected_password_label.configure(text=f"Selected: {target_word}")
    
    password_choice_var.trace("w", update_selected_password)
    
    password_choice_menu = ctk.CTkOptionMenu(frame, font=("Arial", 16), fg_color = "black", button_color = "black", 
                                           values=list(password_options.keys()), variable=password_choice_var, command=update_selected_password)
    password_choice_menu.grid(column = 0, row = 2, pady = 5, padx = 10)
    
    # Custom password selection
    custom_frame = ctk.CTkFrame(frame, fg_color="transparent")
    custom_frame.grid(column = 0, row = 3, pady = 5, padx = 10)
    
    custom_label = ctk.CTkLabel(custom_frame, text="Custom Index:", font=("Arial", 14), text_color="white")
    custom_label.grid(column = 0, row = 0, pady = 2, padx = 5)
    
    custom_index_var = ctk.StringVar(value="0")
    custom_index_entry = ctk.CTkEntry(custom_frame, placeholder_text="0-2024", width=100, textvariable=custom_index_var)
    custom_index_entry.grid(column = 1, row = 0, pady = 2, padx = 5)
    custom_index_var.trace("w", update_selected_password)
    
    # Selected password display
    selected_password_label = ctk.CTkLabel(frame, text="Selected: --", font=("Arial", 14), text_color="lightgreen")
    selected_password_label.grid(column = 0, row = 4, pady = 5, padx = 10)
    
    # User selection (keeping original for compatibility)
    user_selection_label = ctk.CTkLabel(frame, text="User Selection (for login testing):", font=("Arial", 16), text_color="white")
    user_selection_label.grid(column = 0, row = 5, pady = 5, padx = 10)
    
    optionmenu = ctk.CTkOptionMenu(frame, font=("Arial", 20), fg_color = "black", button_color = "black", values=["user1", "user2", "user3"])
    optionmenu.grid(column = 0, row = 6, pady = 5, padx = 10)

    # Attack method selection
    attack_method_label = ctk.CTkLabel(frame, text="Attack Method:", font=("Arial", 16), text_color="white")
    attack_method_label.grid(column = 0, row = 7, pady = 5, padx = 10)
    
    attack_method_var = ctk.StringVar(value="dictionary")
    attack_method_dictionary = ctk.CTkRadioButton(frame, text="Dictionary Attack", variable=attack_method_var, value="dictionary", font=("Arial", 14), text_color="white")
    attack_method_dictionary.grid(column = 0, row = 8, pady = 2, padx = 10)
    
    attack_method_incremental = ctk.CTkRadioButton(frame, text="Incremental Attack", variable=attack_method_var, value="incremental", font=("Arial", 14), text_color="white")
    attack_method_incremental.grid(column = 0, row = 9, pady = 2, padx = 10)

    # Attack control buttons
    button_frame = ctk.CTkFrame(frame, fg_color="transparent")
    button_frame.grid(column = 0, row = 10, pady = 10, padx = 10)

    #Creates a button called "Start Attack" and places it on the grid. Runs the main function to start the attack
    startAttackButton = ctk.CTkButton(button_frame, text="Start Attack", font=("Arial", 20), text_color="white", fg_color="black", width=120, command=lambda: start_attack(elements, twoFACheckbox, root, attack_method_var, password_choice_var, custom_index_var))
    startAttackButton.grid(column = 0, row = 0, pady = 5, padx = 5)

    pauseAttackButton = ctk.CTkButton(button_frame, text="Pause", font=("Arial", 20), text_color="white", fg_color="orange", width=120, command=lambda: pause_attack())
    pauseAttackButton.grid(column = 1, row = 0, pady = 5, padx = 5)

    finishAttackButton = ctk.CTkButton(button_frame, text="Finish", font=("Arial", 20), text_color="white", fg_color="red", width=120, command=lambda: finish_attack())
    finishAttackButton.grid(column = 2, row = 0, pady = 5, padx = 5)

    #Creates a label called "attemptNumber" and places it on the grid. Will be updated with the current attempt number.
    attemptNumberLabel = ctk.CTkLabel(frame, text="--", font=("Arial", 24), text_color="white")
    attemptNumberLabel.grid(column = 0, row = 11, pady = 3, padx = 3)

    #Creates a label called "passwordAttempt" and places it on the grid. Will be updated with the current password attempt.
    passwordAttemptLabel = ctk.CTkLabel(frame, text="--", font=("Arial", 24), text_color="white")
    passwordAttemptLabel.grid(column = 0, row = 12, pady = 3, padx = 3)
    
    #Creates a label called "elapsedTime" and places it on the grid. Will be updated with the current elapsed time.
    elapsedTimeLabel = ctk.CTkLabel(frame, text="00:00", font=("Arial", 24), text_color="white")
    elapsedTimeLabel.grid(column = 0, row = 13, pady = 3, padx = 3)

    # Attack speed label
    attackSpeedLabel = ctk.CTkLabel(frame, text="Speed: -- pwd/sec", font=("Arial", 18), text_color="white")
    attackSpeedLabel.grid(column = 0, row = 14, pady = 3, padx = 3)

    # Password strength label
    passwordStrengthLabel = ctk.CTkLabel(frame, text="Strength: --", font=("Arial", 18), text_color="white")
    passwordStrengthLabel.grid(column = 0, row = 15, pady = 3, padx = 3)

    #Creates a label called "passwordDetected" and places it on the grid. Will be updated to say if the password was found or not.
    passwordDetectedLabel = ctk.CTkLabel(frame, text="Click \"Start Attack\"", font=("Arial", 24), text_color="white")
    passwordDetectedLabel.grid(column = 0, row = 16, pady = (20,5), padx = 3)

    #Creates a button called "Test login". 
    testLoginButton = ctk.CTkButton(frame, text="Test Login", font=("Arial", 24), text_color="white", fg_color="black", width=20, command=lambda: login_page(root, frame))
    testLoginButton.grid(column = 0, row = 17, pady = (5,20), padx = 10)

    elements = [elapsedTimeLabel, attemptNumberLabel, passwordAttemptLabel, passwordDetectedLabel, optionmenu, attackSpeedLabel, passwordStrengthLabel, selected_password_label, password_choice_var, custom_index_var] #Array of all the elements to pass to main to update them as the program runs

    root.mainloop() #Runs the user interface

def start_attack(elements, twofa_checkbox, root_window, attack_method_var, password_choice_var, custom_index_var):
    global attack_paused, attack_finished
    attack_paused = False
    attack_finished = False
    main(elements, twofa_checkbox, root_window, attack_method_var, password_choice_var, custom_index_var)

def pause_attack():
    global attack_paused
    attack_paused = True

def finish_attack():
    global attack_finished
    attack_finished = True

def login_page(root, frame):
    frame.place_forget() # Hides the user_interface frame

    login_frame = ctk.CTkFrame(master=root, width=500, height=600) #Sets a frame in the window to utalize a grid for label & button placement
    login_frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside') #places the frame in the center of the window

    # Title
    title_label = ctk.CTkLabel(login_frame, text="Test Login System", font=("Arial", 28, "bold"), text_color="white")
    title_label.grid(column = 0, row = 0, pady = 20, padx = 10, columnspan = 2)

    #Creates a button that calls the "hide_login_page" function to switch to the main user interface
    back_button = ctk.CTkButton(login_frame, text="← Back to Main", font=("Arial", 18), text_color="white", fg_color="gray", width=150, command=lambda: hide_login_page(frame, login_frame))
    back_button.grid(column = 0, row = 1, pady = 10, padx = 10, columnspan = 2)

    # Help text
    help_label = ctk.CTkLabel(login_frame, text="Available users: user1, user2, user3", font=("Arial", 14), text_color="lightblue")
    help_label.grid(column = 0, row = 2, pady = 5, padx = 10, columnspan = 2)

    #Creates a username label and places it on the grid
    username_label = ctk.CTkLabel(login_frame, text="Username: ", font=("Arial", 20), text_color="white")
    username_label.grid(column = 0, row = 3, pady = 15, padx = 10)

    #Creates a username text box for the user to enter a username
    username_text_box = ctk.CTkEntry(login_frame, placeholder_text="Enter username (user1/user2/user3)", width=250)
    username_text_box.grid(column = 1, row = 3, pady = 15, padx = (0,10))

    #Creates a password label and places it on the grid
    password_label = ctk.CTkLabel(login_frame, text="Password: ", font=("Arial", 20), text_color="white")
    password_label.grid(column = 0, row = 4, pady = 15, padx = 10)

    #Creates a password text box for the user to enter a password
    password_text_box = ctk.CTkEntry(login_frame, placeholder_text="Enter password", width=250, show="*")
    password_text_box.grid(column = 1, row = 4, pady = 15, padx = (0,10))

    #Creates a label that will update depending on if the login was a success
    login_success = ctk.CTkLabel(login_frame, text="Enter credentials and click Login", font=("Arial", 18), text_color="white")
    login_success.grid(column = 0, row = 5, pady = 20, padx = 10, columnspan = 2)

    #Creates a login button to run the "test_login" function to test if the inputted username and password work
    login_button = ctk.CTkButton(login_frame, text="Login", font=("Arial", 20), text_color="white", fg_color="green", width=150, command=lambda: test_login(username_text_box, password_text_box, login_success))
    login_button.grid(column = 0, row = 6, pady = 20, padx = 10, columnspan = 2)

    # Password hints
    hints_label = ctk.CTkLabel(login_frame, text="Hints: user1=123 (easy), user2=sight (medium), user3=horizon372 (hard)", font=("Arial", 12), text_color="yellow")
    hints_label.grid(column = 0, row = 7, pady = 10, padx = 10, columnspan = 2)

def hide_login_page(frame, login_frame):
    #Hides the login page and places the main user interface page
    login_frame.place_forget()
    frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside')

def test_login(username_text_box, password_text_box, login_success):
    username = username_text_box.get() #Gets the username from the username text box
    test_password = password_text_box.get() #Gets the password from the password text box
    actual_password = get_password(username) #Gets the actual password of the target user
    
    # Debug information
    print(f"Login attempt - Username: '{username}', Test Password: '{test_password}', Actual Password: '{actual_password}'")
    
    # Check if username is valid
    if not username:
        login_success.configure(text_color = "red", text="Please enter a username!")
        return
    
    # Check if password was entered
    if not test_password:
        login_success.configure(text_color = "red", text="Please enter a password!")
        return
    
    # Check if username exists
    if actual_password is None:
        login_success.configure(text_color = "red", text=f"User '{username}' not found!")
        return
    
    #Changes the login_success label depending on if the right username and password were entered
    if test_password == actual_password:
        login_success.configure(text_color = "green", text="Login success!")
        print("Login successful!")
    else:
        login_success.configure(text_color = "red", text="Login failed - wrong password!")
        print("Login failed - wrong password!")

def main(elements, twofa_checkbox, root_window, attack_method_var, password_choice_var, custom_index_var) -> None:
    global attack_paused, attack_finished
    
    start_time = time.time() # Start program run timer
    print("\nStarting Brute Force Attack...\n")   
    
    #Assigns the corresponding labels from the labels array
    elapsedTimeLabel = elements[0]
    attemptNumberLabel = elements[1]
    passwordAttemptLabel = elements[2]
    passwordDetectedLabel = elements[3]
    optionmenu = elements[4]
    attackSpeedLabel = elements[5]
    passwordStrengthLabel = elements[6]
    selected_password_label = elements[7]
    password_choice_var = elements[8]
    custom_index_var = elements[9]

    # Get password list based on attack method
    attack_method = attack_method_var.get()
    if attack_method == "dictionary":
        password_list_array = read_passwords_from_file(COMMON_PASSWORD_LIST)
        print(f"Using Dictionary Attack with {len(password_list_array)} passwords")
    else:
        password_list_array = generate_incremental_passwords(4)
        print(f"Using Incremental Attack with {len(password_list_array)} combinations")
    
    # Determine target password based on user selection
    password_choice = password_choice_var.get()
    password_options = get_password_selection_options()
    
    if password_choice == "Custom Selection":
        try:
            custom_index = int(custom_index_var.get())
            if 0 <= custom_index < len(password_list_array):
                target_word = password_list_array[custom_index]
                selected_password_label.configure(text=f"Selected: {target_word} (Index: {custom_index})")
            else:
                target_word = "password"  # Default fallback
                selected_password_label.configure(text=f"Selected: {target_word} (Invalid index)")
        except ValueError:
            target_word = "password"  # Default fallback
            selected_password_label.configure(text=f"Selected: {target_word} (Invalid index)")
    else:
        target_word = password_options[password_choice]
        selected_password_label.configure(text=f"Selected: {target_word}")
    
    print(f"Target password: {target_word}")
    
    # Analyze password strength
    strength_analysis = analyze_password_strength(target_word)
    passwordStrengthLabel.configure(text=f"Strength: {strength_analysis['strength']} (Score: {strength_analysis['score']})")
    
    passwordDetectedLabel.configure(text_color = "white", text="Running Attack...")

    if not target_word:
        print("\nFailed: No valid target password in password secret password file.")
        passwordDetectedLabel.configure(text_color = "red", text="No valid password in file") #Updates passwordDetectedLabel
        return
    
    # Loop through passwords
    if len(password_list_array) > 0:
        attempt = 0
        for word in password_list_array:
            # Check if attack is paused or finished
            if attack_paused:
                passwordDetectedLabel.configure(text_color = "orange", text="Attack Paused")
                return
            if attack_finished:
                passwordDetectedLabel.configure(text_color = "red", text="Attack Finished")
                return
                
            attempt += 1
            print(f"{attempt}. Trying: \"{word}\"")            
            attemptNumberLabel.configure(text=f"Attempt: #{attempt} ") #Updates attemptNumberLabel
            passwordAttemptLabel.configure(text=f"Password: {word}") #Updates passwordAttemptLabel

            # Calculate and display attack speed
            current_time = time.time()
            elapsed_time = current_time - start_time
            speed_metrics = calculate_attack_speed(attempt, elapsed_time)
            attackSpeedLabel.configure(text=f"Speed: {speed_metrics['passwords_per_second']} pwd/sec")
            
            print(f"Time: {round(elapsed_time, 2)} seconds.")
            elapsedTimeLabel.configure(text=f"{round(elapsed_time, 2)} s") #updates elapsedTimeLabel
            
            root_window.update()  # Refresh UI to show current attempt

            # Check if 2FA is enabled
            if twofa_checkbox.get():
                print("2FA enabled - requesting verification...")

                if not perform_2fa(root_window):
                    print("2FA verification failed or cancelled. Stopping attack.")
                    passwordDetectedLabel.configure(text_color = "red", text="Attack cancelled (2FA failed)")
                    return

            if word == target_word:
                print(f"\nSuccess, the password word was: \"{word}\"")
                passwordDetectedLabel.configure(text_color = "green", text="Password found!") #updates passwordDetectedLabel
                break
        else:
            print("\nFailed: The Common Password List doesn't contain the user's password.")
            passwordDetectedLabel.configure(text_color = "red", text="Password was not found") #updates passwordDetectedLabel
    
    else:
        print("\nFailed: The common password list is empty.")
        passwordDetectedLabel.configure(text_color = "red", text="Password list was empty") #updates passwordDetectedLabel

if __name__ == "__main__":
    #main()
    user_interface() #Temporarily until we move things around to the UI instead of being in the terminal