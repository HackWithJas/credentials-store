# 🔐 Secrets Manager

A secure password management system built with Python that encrypts and stores service passwords in a MySQL database using Fernet encryption.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Security](#-security)
- [Database Schema](#-database-schema)
- [Error Handling](#-error-handling)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

- **Secure Encryption**: Uses Fernet symmetric encryption from the `cryptography` library
- **MySQL Database Storage**: Stores encrypted passwords in a MySQL database
- **Environment Variables**: Secure configuration using `.env` files
- **Command Line Interface**: Simple CLI for storing and retrieving passwords
- **Automatic Table Creation**: Creates database table if it doesn't exist
- **Error Handling**: Comprehensive error handling for database operations

## 🔧 Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.7+**
- **MySQL Server** (running on localhost)
- **Required Python packages** (see Installation section)

## 🚀 Installation

1. **Clone the repository** (or download the files):

   ```bash
   git clone <repository-url>
   cd Secrets-Manager
   ```

2. **Install required Python packages**:

   ```bash
   pip install mysql-connector-python python-dotenv cryptography
   ```

3. **Set up MySQL Database**:
   - Install and start MySQL server
   - Create a database named `password`:
     ```sql
     CREATE DATABASE password;
     ```
   - Ensure MySQL is running on `localhost` with default port (3306)

## ⚙️ Configuration

### Environment Variables Setup

1. **Create/Update `password.env` file** in the project root:

   ```env
   SQLPass="your_mysql_root_password"
   MASTER_KEY="your_fernet_encryption_key"
   ```

2. **Generate a Master Key** (if you don't have one):
   ```python
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   print(key.decode())  # Use this as your MASTER_KEY
   ```

### Configuration Variables

| Variable     | Description                            | Example                     |
| ------------ | -------------------------------------- | --------------------------- |
| `SQLPass`    | MySQL root user password               | `"your_password"`           |
| `MASTER_KEY` | Fernet encryption key (base64 encoded) | `"key_from_generate_key()"` |

## 🎯 Usage

The Secrets Manager supports two main operations:

### Storing a Password

Store a new service password in the encrypted database:

```bash
python main.py store
```

**Interactive prompts:**

- Enter the Service Name: `gmail`
- Enter the Service password: `your_secure_password`

**Output:**

```
Password Stored Successfully!!
```

### Retrieving a Password

Retrieve and decrypt a stored password:

```bash
python main.py call
```

**Interactive prompts:**

- Enter the Service Name: `gmail`

**Output:**

```
ServiceName: gmail
Password: your_secure_password
```

### Command Syntax

```bash
python main.py <operation>
```

**Operations:**

- `store` - Store a new password
- `call` - Retrieve an existing password

## 🔒 Security

### Encryption Details

- **Algorithm**: Fernet (AES 128 in CBC mode with PKCS7 padding)
- **Key Management**: Master key stored in environment variables
- **Storage**: Encrypted passwords stored as LONGBLOB in MySQL

### Security Best Practices

1. **Secure Master Key**: Generate a strong master key and keep it secure
2. **Environment Variables**: Never commit `.env` files to version control
3. **Database Security**: Use strong MySQL passwords and proper user permissions
4. **Access Control**: Limit access to the application and database

### Key Generation

```python
from cryptography.fernet import Fernet

# Generate a new key
key = Fernet.generate_key()
print(f"Your master key: {key.decode()}")

# Save this key securely in your password.env file
```

## 🗄️ Database Schema

The application automatically creates the following table structure:

```sql
CREATE TABLE IF NOT EXISTS ServicePass (
    ServiceName varchar(100) PRIMARY KEY,
    Password LONGBLOB
);
```

### Table Structure

| Column        | Type         | Description                            |
| ------------- | ------------ | -------------------------------------- |
| `ServiceName` | VARCHAR(100) | Primary key, unique service identifier |
| `Password`    | LONGBLOB     | Encrypted password data                |

## ⚠️ Error Handling

The application handles various error scenarios:

### Common Errors and Solutions

| Error                    | Cause                             | Solution                                            |
| ------------------------ | --------------------------------- | --------------------------------------------------- |
| `Wrong Input!!`          | Invalid command argument          | Use `store` or `call` as arguments                  |
| `Service Not Found!!`    | Service doesn't exist in database | Check service name spelling                         |
| `MySQL Connection Error` | Database connection failed        | Verify MySQL is running and credentials are correct |
| `Encryption Error`       | Invalid master key                | Check MASTER_KEY in password.env                    |

### Database Errors

```python
except mysql.connector.Error as err:
    print("Error:", err)
```

Common database errors:

- Connection refused (MySQL not running)
- Access denied (wrong credentials)
- Database doesn't exist

## 🐛 Troubleshooting

### Application Won't Start

1. **Check Python version**: Ensure Python 3.7+ is installed
2. **Verify dependencies**: Run `pip install -r requirements.txt`
3. **Check MySQL**: Ensure MySQL server is running

### Database Connection Issues

1. **Verify MySQL Service**:

   ```bash
   # Windows
   net start mysql

   # Linux/Mac
   sudo systemctl start mysql
   ```

2. **Test Database Connection**:
   ```python
   import mysql.connector
   db = mysql.connector.connect(
       host="localhost",
       user="root",
       password="your_password"
   )
   print("Connection successful!")
   ```

### Environment Variable Issues

1. **Check file exists**: Ensure `password.env` exists in project root
2. **Verify format**: Ensure proper KEY="value" format
3. **Check file loading**: Verify `load_dotenv('password.env')` is called

### Encryption Issues

1. **Invalid Key Error**: Generate a new Fernet key
2. **Decryption Failed**: Ensure the same master key is used for encryption/decryption

## 📁 Project Structure

```
Secrets-Manager/
├── main.py           # Main application file
├── password.env      # Environment variables (DO NOT COMMIT)
├── README.md         # This documentation
└── requirements.txt  # Python dependencies (create if needed)
```

## 🔄 Example Workflow

1. **Setup**:

   ```bash
   # Install dependencies
   pip install mysql-connector-python python-dotenv cryptography

   # Configure environment
   # Edit password.env with your credentials
   ```

2. **Store a password**:

   ```bash
   python main.py store
   # Enter service: github
   # Enter password: mySecurePassword123
   ```

3. **Retrieve a password**:
   ```bash
   python main.py call
   # Enter service: github
   # Output: Password: mySecurePassword123
   ```

## 🛡️ Security Considerations

- **Never commit** `password.env` to version control
- Use **strong, unique passwords** for MySQL
- **Backup your master key** securely
- Consider using **database user with limited privileges** instead of root
- **Regularly rotate** your master key (requires re-encrypting all passwords)

## 📝 Requirements File

Create a `requirements.txt` file:

```txt
mysql-connector-python==8.0.33
python-dotenv==1.0.0
cryptography==41.0.7
```

Install with:

```bash
pip install -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review error messages carefully
3. Ensure all prerequisites are installed correctly
4. Verify your `password.env` configuration

---

**⚠️ Important**: This is a basic password manager for educational purposes. For production use, consider additional security measures like:

- Key derivation functions (PBKDF2, Argon2)
- Multi-factor authentication
- Secure key storage solutions
- Regular security audits

