# 🔒 Secure Data Encryption System

## Project Description

The **Secure Data Encryption System** is a Streamlit-based web application that allows users to safely **store** and **retrieve** text data through encryption. It offers a simple, user-friendly interface while maintaining data confidentiality using strong encryption algorithms.

### Key Functionalities

- **User Authentication**
  - Users can **sign up** with a unique username and password.
  - Existing users can **log in** to access the secure features.
  - Passwords are hashed using SHA-256 for added security.

- **Data Encryption & Storage**
  - Logged-in users can input text data and a custom passkey.
  - The text is encrypted using the `cryptography` library and stored along with the hashed passkey.
  - The encryption key is unique per user and stored securely in session state.

- **Data Retrieval & Decryption**
  - Users can paste previously encrypted text and input the correct passkey.
  - If the encrypted data and passkey match, the original message is decrypted and displayed.


### Pages Included

- **Signup Page** – Create a new account.
- **Login Page** – Login with credentials.
- **Home Page** – Welcome screen after login.
- **Store Data** – Encrypt and save user input.
- **Retrieve Data** – Decrypt previously saved data.

---

**Made with by [Fazilat Jahan](https://www.linkedin.com/in/fazilat-jahan-web-developer/)**
