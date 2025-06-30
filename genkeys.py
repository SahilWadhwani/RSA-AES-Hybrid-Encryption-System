#!/usr/bin/env python3
"""
genkeys.py — generate RSA public and private keys for a given user.

Usage:
    ./genkeys.py <username>
Produces:
    <username>.pub  — RSA public key (n and e)
    <username>.prv  — RSA private key (n and d)
"""

import sys
import os
import random

def is_prime(n, k=40):
    """Miller–Rabin primality test."""
    if n < 2:
        return False
    # small primes to speed up
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        if n % p == 0:
            return n == p
    # write n-1 as d * 2^s
    s = 0
    d = n - 1
    while d & 1 == 0:
        d >>= 1
        s += 1

    rng = random.SystemRandom()
    for _ in range(k):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a prime number of the given bit length."""
    rng = random.SystemRandom()
    while True:
        # ensure top bit set and make it odd
        candidate = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(candidate):
            return candidate

def egcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Modular inverse of a modulo m."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def generate_rsa_keypair(bits=1024):
    """Generate an RSA keypair with modulus of given bit size."""
    half_bits = bits // 2
    e = 65537

    while True:
        p = generate_prime(half_bits)
        q = generate_prime(half_bits)
        if p == q:
            continue
        n = p * q
        phi = (p - 1) * (q - 1)
        # ensure e is coprime to phi
        if egcd(e, phi)[0] == 1:
            break

    d = modinv(e, phi)
    return n, e, d

def write_keyfile(filename, components):
    """Write key components (dict) to a file as text."""
    with open(filename, 'w') as f:
        for name, value in components.items():
            f.write(f"{name}={value}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: ./genkeys.py <username>")
        sys.exit(1)

    user = sys.argv[1]
    n, e, d = generate_rsa_keypair(bits=1024)

    pubfile = f"{user}.pub"
    prvfile = f"{user}.prv"

    write_keyfile(pubfile, {'n': n, 'e': e})
    write_keyfile(prvfile, {'n': n, 'd': d})

    print(f"Generated RSA keypair:")
    print(f"  Public key:  {pubfile}")
    print(f"  Private key: {prvfile}")

if __name__ == "__main__":
    main()
