#!/usr/bin/env python3
"""
Email Notifier - Automated Email Notification System

This script monitors specific events or conditions and sends automated email
notifications. Perfect for keeping track of important updates without manual
checking.

Usage:
    python email_notifier.py [options]
    
Example:
    python email_notifier.py --check-interval 300

Features:
    - Monitor system events, file changes, or custom conditions
    - Send formatted HTML or plain text emails
    - Configurable check intervals
    - Support for multiple recipients
    - Secure SMTP authentication

Author: automation-scripts
License: MIT
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import sys

class EmailNotifier:
    """A flexible email notification system for automated alerts."""
    
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        """
        Initialize the email notifier.
        
        Args:
            smtp_server (str): SMTP server address (e.g., 'smtp.gmail.com')
            smtp_port (int): SMTP port (usually 587 for TLS)
            sender_email (str): Sender's email address
            sender_password (str): Sender's email password or app-specific password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_email(self, recipient_email, subject, body, html=False):
        """
        Send an email notification.
        
        Args:
            recipient_email (str or list): Recipient email address(es)
            subject (str): Email subject line
            body (str): Email body content
            html (bool): Whether the body is HTML formatted
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['Subject'] = subject
            
            # Handle multiple recipients
            if isinstance(recipient_email, list):
                message['To'] = ', '.join(recipient_email)
                recipients = recipient_email
            else:
                message['To'] = recipient_email
                recipients = [recipient_email]
            
            # Attach body
            if html:
                message.attach(MIMEText(body, 'html'))
            else:
                message.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable TLS encryption
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipients, message.as_string())
            
            print(f"Email sent successfully to {recipients}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed. Check your email and password.")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP Error: {e}")
            return False
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_notification(self, recipients, title, message, details=None):
        """
        Send a formatted notification email.
        
        Args:
            recipients (str or list): Email recipient(s)
            title (str): Notification title
            message (str): Main notification message
            details (dict): Optional additional details to include
        
        Returns:
            bool: Success status
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create HTML body
        html_body = f"""
        <html>
        <head></head>
        <body>
            <h2 style="color: #2c3e50;">{title}</h2>
            <p><strong>Time:</strong> {timestamp}</p>
            <p>{message}</p>
        """
        
        if details:
            html_body += "<h3>Details:</h3><ul>"
            for key, value in details.items():
                html_body += f"<li><strong>{key}:</strong> {value}</li>"
            html_body += "</ul>"
        
        html_body += """
        </body>
        </html>
        """
        
        subject = f"Notification: {title}"
        return self.send_email(recipients, subject, html_body, html=True)

def monitor_condition(notifier, recipients, check_function, interval=60):
    """
    Monitor a condition and send notifications when it's met.
    
    Args:
        notifier (EmailNotifier): Email notifier instance
        recipients (str or list): Notification recipients
        check_function (callable): Function that returns True when notification should be sent
        interval (int): Check interval in seconds
    """
    print(f"Starting monitoring... (Checking every {interval} seconds)")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            if check_function():
                notifier.send_notification(
                    recipients,
                    "Condition Met",
                    "The monitored condition has been triggered."
                )
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

def example_condition():
    """
    Example condition function.
    Replace this with your own custom condition.
    """
    # Example: Check if a file exists
    # return os.path.exists('/path/to/file.txt')
    
    # For demonstration, always return False
    return False

def main():
    """
    Main function demonstrating email notifier usage.
    Configure with your SMTP settings before running.
    """
    print("Email Notifier - Configuration Required")
    print("="*50)
    print("\nThis script requires SMTP configuration.")
    print("Please edit the script and provide:")
    print("  - SMTP server address")
    print("  - SMTP port")
    print("  - Sender email address")
    print("  - Sender email password (or app-specific password)")
    print("\nExample configuration for Gmail:")
    print("  SMTP_SERVER = 'smtp.gmail.com'")
    print("  SMTP_PORT = 587")
    print("  SENDER_EMAIL = 'your_email@gmail.com'")
    print("  SENDER_PASSWORD = 'your_app_password'")
    print("\n" + "="*50)
    print("\nTo use this script:")
    print("1. Configure your SMTP settings")
    print("2. Define your monitoring condition")
    print("3. Run the script")
    
    # Example usage (uncomment and configure):
    # SMTP_SERVER = 'smtp.gmail.com'
    # SMTP_PORT = 587
    # SENDER_EMAIL = 'your_email@gmail.com'
    # SENDER_PASSWORD = 'your_password'
    # RECIPIENT_EMAIL = 'recipient@example.com'
    # 
    # notifier = EmailNotifier(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)
    # 
    # # Send a test notification
    # notifier.send_notification(
    #     RECIPIENT_EMAIL,
    #     "Test Notification",
    #     "This is a test notification from the Email Notifier script.",
    #     details={'Status': 'Active', 'Priority': 'High'}
    # )
    # 
    # # Start monitoring (with custom condition)
    # monitor_condition(notifier, RECIPIENT_EMAIL, example_condition, interval=300)

if __name__ == "__main__":
    main()
