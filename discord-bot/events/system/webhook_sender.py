#!/usr/bin/env python3
"""
Standalone Discord Webhook Sender
A simple script to send messages to Discord via webhook.

Usage:
    python events/webhook_sender.py "Your message here"
    python events/webhook_sender.py "Custom message" "Custom Username"
"""

import sys
import os
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from system.webhook_lib import send_message_sync

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
WEBHOOK_URL = "https://discord.com/api/webhooks/1419241764669100052/xZRuFrQ1vrEFVdKPOWERrYZYpyEj_4c4jVPb_ZGfWwnn4sOF3I3WdiR5gRYF6kjYRq0g"
DEFAULT_MESSAGE = "hello world!"
DEFAULT_USERNAME = "Standalone Bot"

def main():
    """Main function to send webhook message"""
    
    # Parse command line arguments
    if len(sys.argv) >= 2:
        message = sys.argv[1]
    else:
        message = DEFAULT_MESSAGE
    
    if len(sys.argv) >= 3:
        username = sys.argv[2]
    else:
        username = DEFAULT_USERNAME
    
    print(f"📤 Sending message: {message}")
    print(f"👤 Username: {username}")
    
    # Send the message
    success = send_message_sync(WEBHOOK_URL, message, username)
    
    if success:
        print("✅ Message sent successfully!")
        sys.exit(0)
    else:
        print("❌ Failed to send message!")
        sys.exit(1)

if __name__ == "__main__":
    main()
