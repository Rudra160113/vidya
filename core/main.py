# File location: vidya/core/main.py

import os
import datetime
import logging
import time
import json

# --- File Imports (relative paths based on the directory structure) ---
from vidya.core.vidya_brain import VidyaBrain
from vidya.utils.permission_handler import PermissionHandler
from vidya.utils.auto_start import AutoStart
from vidya.services.supabase_handler import SupabaseHandler
from vidya.services.email_handler import EmailHandler
from vidya.services.web_crawler import WebCrawler

# --- API Keys & Credentials ---
# Please replace these with your actual keys.
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
HUGGINGFACE_API_KEY = "YOUR_HUGGINGFACE_API_KEY_HERE"
EMAIL_ADDRESS = "YOUR_EMAIL_ADDRESS@example.com"
EMAIL_PASSWORD = "YOUR_APP_SPECIFIC_PASSWORD_HERE"  # Use an app-specific password for security

def setup_logging():
    """Configures the main application logger."""
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    log_filename = datetime.datetime.now().strftime(f"{log_directory}/app_activity_%Y-%m-%d.txt")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        filename=log_filename,
        filemode='a'
    )

def main():
    """Main function to run the Vidya AI Assistant."""
    print("Welcome to Vidya AI Assistant.")

    # --- Validation ---
    if not all([GEMINI_API_KEY, HUGGINGFACE_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD]):
        print("Error: Missing credentials. Please update the script.")
        return

    setup_logging()
    logging.info("--- New Session Started ---")
    
    try:
        supabase_handler = SupabaseHandler('vidya/config/supabase_config.json')
    except Exception as e:
        print(f"Error initializing Supabase: {e}")
        return

    email_handler = EmailHandler(EMAIL_ADDRESS, EMAIL_PASSWORD)
    permission_handler = PermissionHandler()
    permission_handler.request_all_permissions()
    
    AutoStart.simulate_auto_start()

    vidya = VidyaBrain(GEMINI_API_KEY, HUGGINGFACE_API_KEY, supabase_handler, email_handler)
    web_crawler = WebCrawler(supabase_handler)
    last_crawl_time = 0

    print("Vidya is ready. Type your message below, or use special commands.")
    print("Type 'exit' to quit.")

    user_id = input("Enter a user ID to start your session: ")
    print(f"Session started for User ID: {user_id}")

    while True:
        # Check if it's time to run the crawler (every 3 days)
        if time.time() - last_crawl_time > 3 * 24 * 60 * 60:
            web_crawler.crawl()
            last_crawl_time = time.time()

        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            
            if "get my history" in user_input.lower():
                email = input("Please enter your email to receive a one-time password: ")
                otp_sent = vidya.send_otp_for_history(user_id, email)
                if otp_sent:
                    otp_entered = input("An OTP has been sent to your email. Please enter it here: ")
                    if vidya.verify_otp(user_id, otp_entered):
                        history = vidya.get_history(user_id)
                        print("Vidya: Here is your history:\n" + history)
                    else:
                        print("Vidya: The OTP is incorrect or has expired.")
                else:
                    print("Vidya: I could not send the OTP. Please try again.")
            else:
                response = vidya.process_input(user_input, user_id)
                print(f"Vidya: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
