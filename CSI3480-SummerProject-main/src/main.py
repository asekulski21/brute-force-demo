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

# Constants
COMMON_PASSWORD_LIST = "../small-password-list/smallpasswordlist.txt" #Changed from rockyou file path to secret_password path
TARGET_PASSWORD = "../secret_user_info/secret_password.txt"

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

def get_target(filename: str) -> str:
    # Get the target word from the secret file
    try:
        with open(filename, "r") as file:
            word = file.readline().strip()
            
            if word: # If the word isn't null/empty
                return word
            else:
                print(f"Error: File '{filename}' is empty!")
                return ""
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return ""
    except Exception as e:
        print(f"An error occured: {e}")
        return ""

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


def user_Interface():
    root = ctk.CTk() # Initializes the User Interface window
    ctk.set_appearance_mode("dark")
    root.title("Brute Force Attack")
    root.geometry("1280x720")
    frame = ctk.CTkFrame(master=root, width=500, height=500) #Sets a frame in the window to utalize a grid for label & button placement
    frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside') #places the frame in the center of the window

    #Creates a checkbox for 2FA option
    twoFACheckbox = ctk.CTkCheckBox(frame, text="Enable 2FA", font=("Arial", 16), text_color="white")
    twoFACheckbox.grid(column = 0, row = 0, pady = 5, padx = 10, columnspan = 2)

    #Creates a button called "Start Attack" and places it on the grid
    startAttackButton = ctk.CTkButton(frame, text="Start Attack", font=("Arial", 24), text_color="white", fg_color="black", width=20, command=lambda: main(labels, twoFACheckbox, root))
    startAttackButton.grid(column = 0, row = 1, pady = 15, padx = 10, columnspan = 2)

    #Creates a label called "attemptNumber" and places it on the grid. Will be updated with the current attempt number.
    attemptNumberLabel = ctk.CTkLabel(frame, text="--", font=("Arial", 24), text_color="white")
    attemptNumberLabel.grid(column = 0, row = 2, pady = 3, padx = 3, sticky="e")

    #Creates a label called "passwordAttempt" and places it on the grid. Will be updated with the current password attempt.
    passwordAttemptLabel = ctk.CTkLabel(frame, text="--", font=("Arial", 24), text_color="white")
    passwordAttemptLabel.grid(column = 1, row = 3, pady = 3, padx = 3)
    
    #Creates a label called "elapsedTime" and places it on the grid. Will be updated with the current elapsed time.
    elapsedTimeLabel = ctk.CTkLabel(frame, text="00:00", font=("Arial", 24), text_color="white")
    elapsedTimeLabel.grid(column = 0, row = 4, pady = 3, padx = 3, columnspan = 2)

    #Creates a label called "passwordDetected" and places it on the grid. Will be updated to say if the password was found or not.
    passwordDetectedLabel = ctk.CTkLabel(frame, text="Click \"Start Attack\"", font=("Arial", 24), text_color="white")
    passwordDetectedLabel.grid(column = 0, row = 5, pady = 15, padx = 3, columnspan = 2)

    labels = [elapsedTimeLabel, attemptNumberLabel, passwordAttemptLabel, passwordDetectedLabel] #Array of all the labels to pass to main to update them as the program runs

    root.mainloop() #Runs the user interface


def main(labels, twofa_checkbox, root_window) -> None:
    start_time = time.time() # Start program run timer
    print("\nStarting Brute Force Attack...\n")

    password_list_array = read_passwords_from_file(COMMON_PASSWORD_LIST)
    target_word = get_target(TARGET_PASSWORD)
    
    #Assigns the corresponding labels from the labels array
    elapsedTimeLabel = labels[0]
    attemptNumberLabel = labels[1]
    passwordAttemptLabel = labels[2]
    passwordDetectedLabel = labels[3]

    if not target_word:
        print("\nFailed: No valid target password in password secret password file.")
        passwordDetectedLabel.configure(text="No valid password in file") #Updates passwordDetectedLabel
        return
    
    # Loop through passwords
    if len(password_list_array) > 0:
        attempt = 0
        for word in password_list_array:
            attempt += 1
            print(f"{attempt}. Trying: \"{word}\"")            
            attemptNumberLabel.configure(text=f"Attempt: #{attempt} | ") #Updates attemptNumberLabel
            passwordAttemptLabel.configure(text=f"Password: {word}") #Updates passwordAttemptLabel
            
            root_window.update()  # Refresh UI to show current attempt

            # Check if 2FA is enabled
            if twofa_checkbox.get():
                print("2FA enabled - requesting verification...")

                if not perform_2fa(root_window):
                    print("2FA verification failed or cancelled. Stopping attack.")
                    passwordDetectedLabel.configure(text="Attack cancelled (2FA failed)")
                    return

            if word == target_word:
                print(f"\nSuccess, the password word was: \"{word}\"")
                passwordDetectedLabel.configure(text="Password found!") #updates passwordDetectedLabel
                break
        else:
            print("\nFailed: The Common Password List doesn't contain the user's password.")
            passwordDetectedLabel.configure(text="Password was not found") #updates passwordDetectedLabel
    
    else:
        print("\nFailed: The common password list is empty.")
        passwordDetectedLabel.configure(text="Password list was empty") #updates passwordDetectedLabel
    
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"\nFinished in {elapsed_time} seconds.\n")
    elapsedTimeLabel.configure(text=f"{elapsed_time} s") #updates elapsedTimeLabel

if __name__ == "__main__":
    #main()
    user_Interface() #Temporarily until we move things around to the UI instead of being in the terminal