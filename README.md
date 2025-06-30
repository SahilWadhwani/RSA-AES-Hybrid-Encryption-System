# RSA & AES Hybrid Encryption System


##  Overview

This project implements a hybrid cryptosystem using **RSA** (asymmetric) and **AES-128** (symmetric) encryption in Python.

  - **RSA** is used for secure key exchange (encrypting/decrypting the AES key).
  - **AES-128** is used for fast and secure data encryption.

The system enables secure file encryption and decryption using best practices for hybrid cryptography.

-----

## Files

  - `genkeys.py`: Generates RSA key pairs (`alice.pub`, `alice.prv`).
  - `crypt.py`: Handles encryption and decryption using AES-128 and RSA.
      - Uses AES for actual data encryption.
      - Uses RSA for encrypting/decrypting the AES key.
  - `alice.pub`, `alice.prv`: Example RSA public and private key files (PEM format).
  - `secret.txt`, `encrypted.dat`, `decrypted.txt`: Example input, output, and test files.

-----

##  Features

  - **RSA key generation** using cryptographically secure large primes (Miller-Rabin test).
  - **Hybrid encryption**: Combines AES-128 (ECB mode) with RSA for key exchange.
  - **Command-line interface** for encryption/decryption.
  - **PEM format** for key storage (compatible with many tools).
  - Modular code, easy to extend or integrate.

-----

##  Usage

### 1\. RSA Key Generation

Generates public and private keys for RSA (saves as `alice.pub` and `alice.prv`).

```bash
python genkeys.py
```

### 2\. Encryption

Encrypts the input file using a random AES-128 key and RSA-encrypts the AES key.

```bash
python crypt.py -e alice.pub secret.txt encrypted.dat
```

  - `-e`: Encryption mode
  - `alice.pub`: Public RSA key file
  - `secret.txt`: Input file to encrypt
  - `encrypted.dat`: Output (contains encrypted AES key + encrypted data)

### 3\. Decryption

Decrypts the file. It uses the private key to recover the AES key, then decrypts the data with the AES key.

```bash
python crypt.py -d alice.prv encrypted.dat decrypted.txt
```

  - `-d`: Decryption mode
  - `alice.prv`: Private RSA key file
  - `encrypted.dat`: Encrypted file
  - `decrypted.txt`: Output (original data restored)

-----

##  Program Design

### `genkeys.py` - RSA Key Generation

This script generates two large, secure primes using the Miller-Rabin primality test. It then computes the modulus `N = p * q`, calculates Euler’s totient `ϕ(N) = (p-1)*(q-1)`, and sets the public exponent `e = 65537`. Finally, it computes the private exponent `d` as the modular inverse of `e mod ϕ(N)` and outputs the keys in PEM format as `alice.pub` (public) and `alice.prv` (private).

### `crypt.py` - AES and RSA Encryption/Decryption

#### Encryption Flow

1.  Generates a random AES-128 key.
2.  Encrypts input file content using AES-128 (ECB mode).
3.  Encrypts the AES key using the RSA public key.
4.  Outputs both: the RSA-encrypted AES key and AES-encrypted data.

#### Decryption Flow

1.  Uses the RSA private key to decrypt the encrypted AES key.
2.  Uses the decrypted AES key to decrypt the AES-encrypted data.
3.  Restores the original content.

###  Command-Line Arguments

  - `-e`: Encryption mode
  - `-d`: Decryption mode
  - `<key file>`: Path to the public or private RSA key
  - `<input file>`: Data to encrypt or decrypt
  - `<output file>`: Resulting file (encrypted or decrypted)

-----

##  Architecture Diagram

### Hybrid Encryption System

```
                [ genkeys.py ]
                     |
         +--------------------------+
         |   RSA Key Generation     |
         +--------------------------+
                     |
              [ alice.pub, alice.prv ]
                     |
+----------------------------------------------+
|             Encryption (crypt.py)            |
+----------------------------------------------+
| 1. Generate random AES-128 key               |
| 2. Encrypt data with AES key                 |
| 3. Encrypt AES key with RSA public key       |
| 4. Output: [RSA-encrypted AES key + data]    |
+----------------------------------------------+
                     |
+----------------------------------------------+
|             Decryption (crypt.py)            |
+----------------------------------------------+
| 1. Decrypt AES key with RSA private key      |
| 2. Decrypt data with AES key                 |
| 3. Output: original data                     |
+----------------------------------------------+
```

-----

## Conclusion

  - Secure RSA key generation with cryptographically sound primes.
  - Proper hybrid encryption/decryption: fast, secure, and reliable.
  - Follows real-world best practices for cryptographic systems.
  - Ideal for learning modern encryption workflow and cryptography fundamentals.

-----
