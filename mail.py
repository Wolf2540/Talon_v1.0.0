import os
import base64
import json
import pickle
import datetime
import re
from time import sleep

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_service():
    """Authenticate and return the Gmail API service."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def list_messages(service, user_id='me', query='', max_results=100):
    """List Messages of the user's mailbox matching the query."""
    try:
        response = service.users().messages().list(userId=user_id, q=query, maxResults=max_results).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        return messages
    except Exception as error:
        print(f'An error occurred: {error}')
        return []


def get_message(service, user_id, msg_id):
    """Get a Message with given ID."""
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        headers = message['payload']['headers']
        subject, sender, date = None, None, None
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Date':
                date = header['value']

        snippet = message.get('snippet', '')
        body = ""
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8')
                    break

        return {
            'subject': subject,
            'sender': sender,
            'date': date,
            'snippet': snippet,
            'body': body,
            'id': msg_id  # Include the message ID for easy reference
        }
    except Exception as error:
        print(f'An error occurred: {error}')
        return None


def trash_message(service, user_id, msg_id):
    """Move a Message to the Trash with given ID."""
    try:
        service.users().messages().trash(userId=user_id, id=msg_id).execute()
        print(f'Message with ID: {msg_id} has been moved to trash.')
    except Exception as error:
        print(f'An error occurred during trashing: {error}')


def sign_out():
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')
        print('Signed out successfully.')


def main():
    service = get_service()
    messages = list_messages(service)
    page = 0
    per_page = 20

    while True:
        clear_screen()
        start = page * per_page
        end = start + per_page
        current_messages = messages[start:end]

        print(f'Showing emails {start + 1} to {end} of {len(messages)}:')
        displayed_messages = []
        for i, msg in enumerate(current_messages, start=1):
            msg_content = get_message(service, 'me', msg['id'])
            displayed_messages.append(msg_content)  # Save the displayed messages
            print(f"{start + i}. From: {msg_content['sender']}")
            print(f"   Subject: {msg_content['subject']}")
            print(f"   Date: {msg_content['date']}")
            print(f"   Snippet: {msg_content['snippet']}")
            print('-' * 50)

        command = input('$-').strip().lower()

        if command == 'n':
            if end < len(messages):
                page += 1
            else:
                print('No more pages.')
        elif command == 'p':
            if page > 0:
                page -= 1
            else:
                print('You are on the first page.')
        elif command.isdigit() and 1 <= int(command) <= per_page:
            index = start + int(command) - 1
            if index < len(messages):
                msg_content = get_message(service, 'me', messages[index]['id'])
                clear_screen()
                print(f"From: {msg_content['sender']}")
                print(f"Subject: {msg_content['subject']}")
                print(f"Date: {msg_content['date']}")
                print(f"Body: {msg_content['body']}")
                input('Press Enter to return to the list.')
            else:
                print('Invalid email ID.')
        elif command.startswith('d '):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                email_index = int(parts[1]) - 1
                if 0 <= email_index < len(displayed_messages):
                    msg_id = displayed_messages[email_index]['id']
                    trash_message(service, 'me', msg_id)
                    messages = list_messages(service)  # Refresh the message list after trashing
                else:
                    print('Invalid email ID for trashing.')
            else:
                print('Invalid trash command. Use format: t [NUMBER]')
        elif command == 'so':
            sign_out()
            service = None
            while not service:
                try:
                    service = get_service()
                    messages = list_messages(service)
                except Exception as e:
                    print(f'An error occurred: {e}')
                    input('Press Enter to try signing in again...')
        elif command == 'si':
            service = get_service()
            messages = list_messages(service)
        elif command == 'q':
            break
        elif command in ['h', 'help']:
            print("\nHELP PAGE")
            print("\nn -- next page")
            print("p -- previous page")
            print("[ID] -- open email")
            print("d [ID] -- delete email")
            print("so -- sign-out")
            print("si -- sign-in")
            print("h -- help")
            print("q -- quit")
            input("\nPress Enter to continue...")
        else:
            print('\033[91mInvalid command\033[0m')
            sleep(.5)


if __name__ == '__main__':
    main()
