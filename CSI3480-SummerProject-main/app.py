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
import streamlit as st

# Constants
COMMON_PASSWORD_LIST = "small-password-list/smallpasswordlist.txt" #Changed from rockyou file path to secret_password path
TARGET_PASSWORD = "secret_user_info/secret_password.txt"

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

def perform_2fa() -> bool:
    """
    Performs 2FA by generating a random 4-digit number and asking user to input it.
    Returns True if user enters correct number, False if they cancel or enter wrong number.
    """

    # Generate random 4-digit number
    random_number = random.randint(1000, 9999)

    # Ask user to input the number (simplified for web)
    st.write(f"2FA Verification: Please type {random_number}:")
    user_input = st.text_input("Enter the number:", key=f"twofa_{random_number}")

    if st.button("Verify", key=f"verify_{random_number}"):
        try:
            if int(user_input) == random_number:
                st.success("2FA Verification Successful!")
                return True
            else:
                st.error("Incorrect number entered!")
                return False
        except ValueError:
            st.error("Please enter a valid number!")
            return False
    
    return False

def main(labels, twofa_checkbox) -> None:
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
        passwordDetectedLabel.write("No valid password in file") #Updates passwordDetectedLabel
        return
    
    # Loop through passwords
    if len(password_list_array) > 0:
        attempt = 0
        for word in password_list_array:
            attempt += 1
            print(f"{attempt}. Trying: \"{word}\"")            
            attemptNumberLabel.write(f"Attempt: #{attempt} | ") #Updates attemptNumberLabel
            passwordAttemptLabel.write(f"Password: {word}") #Updates passwordAttemptLabel
            
            # Check if 2FA is enabled
            if twofa_checkbox:
                print("2FA enabled - requesting verification...")
                
                if not perform_2fa():
                    print("2FA verification failed or cancelled. Stopping attack.")
                    passwordDetectedLabel.write("Attack cancelled (2FA failed)")
                    return

            if word == target_word:
                print(f"\nSuccess, the password word was: \"{word}\"")
                passwordDetectedLabel.write("Password found!") #updates passwordDetectedLabel
                break
        else:
            print("\nFailed: The Common Password List doesn't contain the user's password.")
            passwordDetectedLabel.write("Password was not found") #updates passwordDetectedLabel
    
    else:
        print("\nFailed: The common password list is empty.")
        passwordDetectedLabel.write("Password list was empty") #updates passwordDetectedLabel
    
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"\nFinished in {elapsed_time} seconds.\n")
    elapsedTimeLabel.write(f"{elapsed_time} s") #updates elapsedTimeLabel

def user_Interface():
    st.title("Brute Force Attack") # Equivalent to root.title()
    
    #Creates a checkbox for 2FA option
    twoFACheckbox = st.checkbox("Enable 2FA")

    #Creates a button called "Start Attack" and places it on the grid
    if st.button("Start Attack"):
        
        #Creates labels - Using Streamlit containers instead of labels
        elapsedTimeLabel = st.empty()
        attemptNumberLabel = st.empty()  
        passwordAttemptLabel = st.empty()
        passwordDetectedLabel = st.empty()
        
        labels = [elapsedTimeLabel, attemptNumberLabel, passwordAttemptLabel, passwordDetectedLabel] #Array of all the labels to pass to main to update them as the program runs
        
        # Call main function with the same parameters as original
        main(labels, twoFACheckbox)

if __name__ == "__main__":
    #main()
    user_Interface() #Temporarily until we move things around to the UI instead of being in the terminal
