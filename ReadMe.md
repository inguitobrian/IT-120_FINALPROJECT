# IT 120 – Final Project - Django REST Framework Application

## Section

**Course:** IT 120 – Integrative Programming Technologies II  
**Section:** BN1
**Term:** Final – 2024–2025, 1st Semester  
**Instructor:** Dexter A. Romaguera

## Team Members

- **Brian Inguito** (Group Leader)
- **Danielle Irish May Martinez**
- **Marbenson Buyan**

## Project Instruction

- Develop Two (2) Django REST Framework (DRF) applications that communicate with each other securely by
  sending and receiving encrypted or hashed messages
- Building secure APIs using middleware for encryption/decryption, as well as integrating essential features.

## Features to Implement

- Login and Registration: Each application must support user authentication.
- Sending and Receiving Messages: Create secure APIs for message transmission. Messages sent between
  the two applications must be encrypted or hashed before being transmitted, and the receiving end or
  application must have a mechanism to decrypt the message before it can be displayed.
- Security Features: Implement middleware to manage encryption, hashing, or request validation.
- Dashboard: Provide an intuitive interface to display and manage all users and messages.

## System Overview

**Project Title:** Santa's Delivery Message
**Description:** A Web-chat application where users can send letters/messages to Santa and Santa can read and manage the users as well as sending messages to them. This application are interconnected enabling seamless and encrypted communication. The application is built with Django REST Framework.

## Application Features

3. **End-to-End Secure Communication:** Messages exchanged between the systems are encrypted during transmission and seamlessly decrypted on receipt using custom middleware, ensuring confidentiality and data integrity.
4. **User Authentication:** A secure login and registration system powered by token-based session management guarantees user privacy and access control.
5. **Interoperable Two-Way Communication:** Interoperable systems enable cross-platform messaging.
6. **User-Friendly Interface:** A responsive, visually appealing design crafted with CSS And Javascript offers users an effortless and engaging experience.

## Technical Stack and Tools

**For Backend:**

- Django 5.0+
- Django Channels
- PostgreSQL

**For Frontend:**

- HTML, CSS, JavaScript

**Development Tools:**

- Git/GitHub
- VS Code
- IntelliJ IEA 2024.2.2 (Alternative for VS Code)

## Installation and Setup

## Clone the Repository

1. Install Python.
2. Install Django
3. Clone the repository:
   ```bash
   https://github.com/inguitobrian/IT-120_FINALPROJECT
   ```
4. Navigate to the project directory:
   ```bash
   cd IT-120_FINALPROJECT
   ```
5. Navigate to `admin_app/settings.py` and `user_ap/settings.py` for database configuration. Change the name of the Database.

6. Generate a FERNET Key for Encryption:

   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

   ```

7. Run migrations:
   ```bash
   python manage.py migrate
   ```
8. Start admin_app and user_app systems:
   ```bash
   python manage.py runserver 8000
   python manage.py runserver 8001 - Depends on the user what port number should use
   ```

## Middleware

### Encrypt and Decrypt Messages

- Secures outgoing message payloads using Fernet encryption.
- Ensures all transmitted data is safe and tamper-proof.
- Decodes incoming encrypted messages.
- Verifies the integrity of the message and ensures only authorized access.

## Santa's Delivery Message System Development Roadmap

1. Watch Video Tutorial about Djano

- Watch tutorials and review documentation to understand Django and its tools.

2. Set up Django project and apps in VS Code.
3. Configure database and sessions.
4. Develop our Frontend Using HTML,CSS,Javascript based on our chosen Web application concept.
5. Define models for users and messages.
6. Store messages securely in PostgreSQL.
7. Implement and integrate encryption middleware.
8. Develop an admin dashboard for user management.
9. Implement APIs for message history with decryption.
10. Perform extensive testing to ensure the application is secure and functional.

![Screenshot 2024-12-26 121020](https://github.com/user-attachments/assets/24de18a7-8447-4a9c-9010-9c8a06f70931)
![Screenshot 2024-12-26 121003](https://github.com/user-attachments/assets/4029a21f-c99b-42f1-a318-649fe7afc046)

