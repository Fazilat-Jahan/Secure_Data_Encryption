import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import base64


st.set_page_config(page_title="Secure Data Encryption System", page_icon="🔒", layout="wide")

# Function to set background image from a local file

def set_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.4; 
            
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function
set_bg_from_local("image.jpg")


# --- SESSION STATE ---
if "users" not in st.session_state:
    st.session_state.users = {}

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "page" not in st.session_state:
    st.session_state.page = "Signup"

# --- HELPERS ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_key():
    return Fernet.generate_key()

def encrypt(text, key):
    return Fernet(key).encrypt(text.encode()).decode()

def decrypt(text, key):
    return Fernet(key).decrypt(text.encode()).decode()

def set_page(name):
    st.session_state.page = name

def logout():
    st.session_state.current_user = None
    st.session_state.page = "Signup"
    st.rerun()




st.markdown(
    """
    <style>
    /* Force buttons to stay in a row */
    .stButton > button {
        display: inline-block;
        width: auto;
        margin: 5px;
    }
    .stColumns > div {
        display: inline-block;
        width: auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TOP BUTTONS  ---
if st.session_state.current_user:
    col1, col2, col3, col4 = st.columns(4)  
    with col1:
        if st.button("🏠 Home"):
            set_page("Home")
    with col2:
        if st.button("🔐 Store Data"):
            set_page("Store")
    with col3:
        if st.button("🔍 Retrieve Data"):
            set_page("Retrieve")
    with col4:
        if st.button("🚪 Logout"):
            logout()
            st.experimental_rerun()  # Re-run after logout




# --- SIGNUP PAGE ---
if st.session_state.page == "Signup":
    st.title("🔒 Secure Data Encryption System")
    st.subheader("🔐 Signup Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        if username in st.session_state.users:
            st.error("Username already exists!")
        elif username and password:
            st.session_state.users[username] = {
                "password": hash_password(password),
                "key": generate_key(),
                "data": []
            }
            st.success("Signup successful! Please login.")
            set_page("Login")
        else:
            st.warning("Please fill both fields.")

    st.button("Login", on_click=lambda: set_page("Login"))

# --- LOGIN PAGE ---
elif st.session_state.page == "Login":
    st.title("🔒 Secure Data Encryption System")
    st.subheader("🔑 Login Page")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = st.session_state.users.get(username)
        if user and user["password"] == hash_password(password):
            st.session_state.current_user = username
            st.success("Login successful!")
            set_page("Home")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.button("Don't have an account? Signup", on_click=lambda: set_page("Signup"))

# --- HOME PAGE ---
elif st.session_state.page == "Home":
    st.title("👋🏻 Welcome To Secure Data Encryption System")
    st.subheader(f"Hello, **{st.session_state.current_user}**! Use the buttons above to store or retrieve your data securely.")

# --- STORE DATA PAGE ---
elif st.session_state.page == "Store":
    st.title("🔐 Store Data Securely")
    text = st.text_area("Enter data to encrypt")
    passkey = st.text_input("Create a passkey", type="password")

    if st.button("Encrypt & Save"):
        if text and passkey:
            user = st.session_state.users[st.session_state.current_user]
            encrypted = encrypt(text, user["key"])
            user["data"].append({
                "encrypted": encrypted,
                "passkey": hash_password(passkey)
            })
            st.success("Data encrypted and stored!")
            st.code(encrypted)
        else:
            st.warning("Please fill both fields.")

# --- RETRIEVE DATA PAGE ---
elif st.session_state.page == "Retrieve":
    st.title("🔍 Retrieve Data")
    encrypted_input = st.text_area("Paste encrypted data")
    passkey = st.text_input("Enter passkey", type="password")

    if st.button("Decrypt"):
        user = st.session_state.users[st.session_state.current_user]
        found = False
        for item in user["data"]:
            if item["encrypted"] == encrypted_input and item["passkey"] == hash_password(passkey):
                decrypted = decrypt(encrypted_input, user["key"])
                st.success("Decrypted Data:")
                st.code(decrypted)
                found = True
                break

        if not found:
            st.error("Wrong passkey or data not found.")

footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 10px;
            left: 20px;
            font-size: 14px;
            color: gray;
        }
    </style>
    <div class="footer">
        Built by <a href="https://www.linkedin.com/in/fazilat-jahan-web-developer/"> <b>Fazilat Jahan</b> </a>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
