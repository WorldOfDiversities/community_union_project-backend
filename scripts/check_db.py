#!/usr/bin/env python3
"""Simple DB connectivity checker for the project.

Usage:
  - Set `DATABASE_URL` in your environment (or pass it as the first arg).
  - Run: `python scripts/check_db.py` or `python scripts/check_db.py "postgresql://..."`

Exits with code 0 on success, non-zero on failure.
"""
import os
import sys
import time

def main():
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = os.environ.get("DATABASE_URL")

    if not url:
        print("No DATABASE_URL provided. Set env var or pass as argument.")
        return 2

    print("Testing database URL:", url.split("@")[-1])

    # Try psycopg (psycopg3) first, then psycopg2
    last_err = None
    try:
        import psycopg
        print("Using psycopg (psycopg3) to connect...")
        conn = psycopg.connect(url, connect_timeout=10)
        conn.close()
        print("Database connection OK (psycopg)")
        return 0
    except Exception as e:
        last_err = e

    try:
        import psycopg2
        print("Using psycopg2 to connect...")
        conn = psycopg2.connect(url, connect_timeout=10)
        conn.close()
        print("Database connection OK (psycopg2)")
        return 0
    except Exception as e:
        last_err = e

    print("Database connection failed:")
    print(repr(last_err))
    return 3

if __name__ == "__main__":
    sys.exit(main())
