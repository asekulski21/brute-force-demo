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
import os

# Constants - file paths for Replit
COMMON_PASSWORD_LIST = "small-password-list/smallpasswordlist.txt"
TARGET_PASSWORD = "secret_user_info/secret_password.txt"

def read_passwords_from_file(filename: str) -> list[str]:
    # Read all the words in the text file and adds it to the array for testing.

    try:
        # "rockyou.txt" uses latin-1 encoding so it has to be specified.
        with open(filename, "r", encoding="latin-1") as file:
            return [line.strip() for line in file]
    
    except FileNotFoundError:
        print("Error: File not found!")
        st.error(f"Error: File '{filename}' not found!")
        return []
    except Exception as e:
        print(f"An error occured: {e}")
        st.error(f"An error occurred: {e}")
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
                st.error(f"Error: File '{filename}' is empty!")
                return ""
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        st.error(f"Error: File '{filename}' not found!")
        return ""
    except Exception as e:
        print(f"An error occured: {e}")
        st.error(f"An error occurred: {e}")
        return ""

def perform_2fa() -> bool:
    """
    Performs 2FA by generating a random 4-digit number and asking user to input it.
    Returns True if user enters correct number, False if they cancel or enter wrong number.
    """

    # Generate random 4-digit number
    if 'twofa_number' not in st.session_state:
        st.session_state.twofa_number = random.randint(1000, 9999)
    
    random_number = st.session_state.twofa_number

    # Ask user to input the number
    st.write(f"🔐 **2FA Verification**: Please type {random_number}")
    user_input = st.text_input("Enter the number:", key="twofa_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verify 2FA"):
            try:
                if user_input and int(user_input) == random_number:
                    st.success("2FA Successful!")
                    # Reset for next time
                    if 'twofa_number' in st.session_state:
                        del st.session_state.twofa_number
                    return True
                else:
                    st.error("2FA Failed: Incorrect number entered!")
                    return False
            except ValueError:
                st.error("2FA Failed: Please enter a valid number!")
                return False
    
    with col2:
        if st.button("Skip 2FA"):
            if 'twofa_number' in st.session_state:
                del st.session_state.twofa_number
            return False
    
    return False

def user_Interface():
    st.set_page_config(page_title="Brute Force Demo", page_icon="🔓")
    st.title("🔓 Brute Force Attack Simulator")
    
    # Educational disclaimer
    st.warning("⚠️ **Educational Purpose Only**: This tool demonstrates password security concepts for learning purposes.")
    
    # Debug info
    st.expander("📁 File Status").write({
        "Current directory": os.getcwd(),
        "Files available": os.listdir("."),
        "Password file exists": os.path.exists(TARGET_PASSWORD),
        "Password list exists": os.path.exists(COMMON_PASSWORD_LIST)
    })
    
    # Creates a checkbox for 2FA option
    twoFACheckbox = st.checkbox("Enable 2FA")
    
    # Creates a button called "Start Attack"
    if st.button("🎯 Start Attack", type="primary"):
        # Create placeholders for labels that will be updated
        with st.container():
            elapsedTimeLabel = st.empty()
            attemptNumberLabel = st.empty() 
            passwordAttemptLabel = st.empty()
            passwordDetectedLabel = st.empty()
            
            labels = [elapsedTimeLabel, attemptNumberLabel, passwordAttemptLabel, passwordDetectedLabel]
            
            # Call main function - EXACT same as original
            main(labels, twoFACheckbox, None)

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
        passwordDetectedLabel.error("❌ No valid password in file")
        return
    
    # Show target info
    passwordDetectedLabel.info(f"🎯 Target loaded! Starting attack...")
    
    # Loop through passwords - EXACT same logic as original
    if len(password_list_array) > 0:
        attempt = 0
        progress_bar = st.progress(0)
        
        for word in password_list_array:
            attempt += 1
            print(f"{attempt}. Trying: \"{word}\"")
            
            # Update progress
            progress = attempt / len(password_list_array)
            progress_bar.progress(progress)
            
            attemptNumberLabel.write(f"🔢 **Attempt #{attempt}** of {len(password_list_array)}")
            passwordAttemptLabel.write(f"🔑 **Trying:** `{word}`")
            
            # Check if 2FA is enabled - EXACT same logic as original
            if twofa_checkbox and attempt % 50 == 1:  # Check every 50 attempts
                print("2FA enabled - requesting verification...")
                st.warning("🔒 2FA verification required...")
                
                if not perform_2fa():
                    print("2FA verification failed or cancelled. Stopping attack.")
                    passwordDetectedLabel.error("❌ Attack cancelled (2FA failed)")
                    return

            if word == target_word:
                print(f"\nSuccess, the password word was: \"{word}\"")
                passwordDetectedLabel.success(f"🎉 **Password found!** The password is: `{word}`")
                st.balloons()
                break
                
            # Small delay for demo effect
            time.sleep(0.01)
            
        else:
            print("\nFailed: The Common Password List doesn't contain the user's password.")
            passwordDetectedLabel.error("❌ Password was not found in the list")
    
    else:
        print("\nFailed: The common password list is empty.")
        passwordDetectedLabel.error("❌ Password list was empty")
    
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"\nFinished in {elapsed_time} seconds.\n")
    elapsedTimeLabel.success(f"⏱️ **Completed in {elapsed_time} seconds**")

if __name__ == "__main__":
    user_Interface()
