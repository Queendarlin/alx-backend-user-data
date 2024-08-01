# Personal Data Management

## Description

This project demonstrates how to securely handle personal data, particularly focusing on logging and password management. The key components include obfuscating log messages to protect sensitive information and hashing passwords before storing them in a database.

## Features

- **Filtered Logging**: Logs personal data in an obfuscated format.
- **Password Hashing**: Hashes user passwords using bcrypt.
- **Password Validation**: Validates passwords against hashed values.

## Setup

### Requirements

- Python 3.x
- `mysql-connector-python`
- `bcrypt`

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/alx-backend-user-data.git
    cd alx-backend-user-data/0x00-personal_data
    ```

2. **Install Dependencies**:
    ```bash
    pip install mysql-connector-python bcrypt
    ```
