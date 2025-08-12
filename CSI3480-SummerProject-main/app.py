#!/usr/bin/env python3

"""
Project Name: Brute Force Demo Project  
Description: Simulates a brute force attack to guess a password
Author: Andrae Taylor, Christina Carvalho, Alexander Sekulski
Date: 7/24/2025
"""

import time
import random
import streamlit as st
import os

# Constants
COMMON_PASSWORD_LIST = "small-password-list/smallpasswordlist.txt"
TARGET_PASSWORD = "secret_user_info/secret_password.txt"

def read_passwords_from_file(filename: str) -> list[str]:
    """Read all the words in the text file and adds it to the array for testing."""
    try:
        # "rockyou.txt" uses latin-1 encoding so it has to be specified.
        with open(filename, "r", encoding="latin-1") as file:
            return [line.strip() for line in file]
    
    except FileNotFoundError:
        st.error(f"Error: File '{filename}' not found!")
        return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

def get_target(filename: str) -> str:
    """Get the target word from the secret file"""
    try:
        with open(filename, "r") as file:
            word = file.readline().strip()
            
            if word:  # If the word isn't null/empty
                return word
            else:
                st.error(f"Error: File '{filename}' is empty!")
                return ""
    
    except FileNotFoundError:
        st.error(f"Error: File '{filename}' not found!")
        return ""
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

def perform_2fa() -> bool:
    """Performs 2FA by generating a random 4-digit number and asking user to input it."""
    
    # Generate random 4-digit number and store in session state
    if 'twofa_number' not in st.session_state:
        st.session_state.twofa_number = random.randint(1000, 9999)
    
    random_number = st.session_state.twofa_number
    
    st.warning(f"🔐 **2FA Verification Required**")
    st.info(f"Please enter this number: **{random_number}**")
    
    user_input = st.text_input("Enter the 4-digit number:", max_chars=4, key="twofa_input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Verify", key="verify_2fa"):
            if user_input:
                try:
                    if int(user_input) == random_number:
                        st.success("✅ 2FA verification successful!")
                        # Clear session state
                        del st.session_state.twofa_number
                        if 'twofa_input' in st.session_state:
                            del st.session_state.twofa_input
                        return True
                    else:
                        st.error("❌ Incorrect number entered!")
                        return False
                except ValueError:
                    st.error("❌ Please enter a valid number!")
                    return False
            else:
                st.error("❌ Please enter the number!")
                return False
    
    with col2:
        if st.button("❌ Cancel", key="cancel_2fa"):
            # Clear session state
            if 'twofa_number' in st.session_state:
                del st.session_state.twofa_number
            return False
    
    return False

def run_brute_force_attack(enable_2fa: bool):
    """Main function to run the brute force attack simulation"""
    
    # Read files
    password_list_array = read_passwords_from_file(COMMON_PASSWORD_LIST)
    target_word = get_target(TARGET_PASSWORD)
    
    if not target_word:
        st.error("❌ Failed: No valid target password found.")
        return
    
    if len(password_list_array) == 0:
        st.error("❌ Failed: Password list is empty.")
        return
    
    # Show attack info
    st.success(f"🎯 Target password loaded successfully!")
    st.info(f"📋 Testing against {len(password_list_array)} common passwords...")
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    attempt_placeholder = st.empty()
    result_placeholder = st.empty()
    
    start_time = time.time()
    attempt = 0
    found = False
    
    # Loop through passwords - EXACT same logic as original
    for word in password_list_array:
        attempt += 1
        
        # Update progress
        progress = attempt / len(password_list_array)
        progress_bar.progress(progress)
        
        # Update status
        status_placeholder.write(f"🔍 **Trying password:** `{word}`")
        attempt_placeholder.write(f"📊 **Attempt #{attempt}** of {len(password_list_array)}")
        
        # Check if 2FA is enabled - EXACT same logic as original  
        if enable_2fa and attempt % 25 == 1:  # Check 2FA every 25 attempts
            st.warning("🔒 2FA verification required to continue...")
            
            if not perform_2fa():
                result_placeholder.error("❌ Attack cancelled (2FA verification failed)")
                return
            
            st.success("✅ 2FA passed, continuing attack...")
        
        # Check if password matches - EXACT same logic as original
        if word == target_word:
            found = True
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            
            # Success display
            result_placeholder.success(f"🎉 **SUCCESS!** Password found: `{word}`")
            st.balloons()
            
            # Show statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Result", "Found")
            with col2:
                st.metric("🔢 Attempts", attempt)
            with col3:
                st.metric("⏱️ Time", f"{elapsed_time}s")
            
            break
        
        # Small delay for visual effect
        time.sleep(0.05)
    
    # If not found - EXACT same logic as original
    if not found:
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        
        result_placeholder.error("❌ **FAILED:** Password not found in common password list")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("❌ Result", "Not Found")
        with col2:
            st.metric("⏱️ Time", f"{elapsed_time}s")

# Main Streamlit app
def main():
    # Page configuration
    st.set_page_config(
        page_title="Brute Force Demo",
        page_icon="🔓",
        layout="centered"
    )
    
    # Header
    st.title("🔓 Brute Force Attack Simulator")
    
    # Educational disclaimer
    st.warning("""
    ⚠️ **EDUCATIONAL PURPOSE ONLY**
    
    This application demonstrates password security concepts for learning purposes only. 
    Do not use this tool for unauthorized access attempts.
    """)
    
    # Team info
    with st.expander("👥 Project Team"):
        st.write("**Authors:** Andrae Taylor, Christina Carvalho, Alexander Sekulski")
        st.write("**Course:** CSI3480 Summer Project")
        st.write("**Date:** July 24, 2025")
    
    # File status check
    with st.expander("📁 System Status"):
        password_file_exists = os.path.exists(TARGET_PASSWORD)
        password_list_exists = os.path.exists(COMMON_PASSWORD_LIST)
        
        col1, col2 = st.columns(2)
        with col1:
            if password_file_exists:
                st.success("✅ Target password file found")
            else:
                st.error("❌ Target password file missing")
        
        with col2:
            if password_list_exists:
                st.success("✅ Password list file found")
                try:
                    with open(COMMON_PASSWORD_LIST, 'r', encoding='latin-1') as f:
                        count = sum(1 for _ in f)
                    st.info(f"📋 Contains {count} passwords")
                except:
                    st.warning("Could not count passwords")
            else:
                st.error("❌ Password list file missing")
    
    st.divider()
    
    # Attack configuration
    st.subheader("⚙️ Attack Configuration")
    
    enable_2fa = st.checkbox(
        "🔐 Enable 2FA Protection", 
        help="When enabled, you'll need to verify your identity during the attack simulation"
    )
    
    if enable_2fa:
        st.info("🔒 2FA verification will be required every 25 password attempts")
    
    st.divider()
    
    # Attack button
    if st.button("🎯 Start Brute Force Attack", type="primary", use_container_width=True):
        if not (os.path.exists(TARGET_PASSWORD) and os.path.exists(COMMON_PASSWORD_LIST)):
            st.error("❌ Cannot start attack: Required files are missing")
        else:
            run_brute_force_attack(enable_2fa)

if __name__ == "__main__":
    main()