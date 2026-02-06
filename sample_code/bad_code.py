import os
import sys
import json

DATA_FILE = "data/users.json"


def load_users():
    f = open(DATA_FILE, "r")          # ❌ file not closed
    data = json.load(f)
    return data


def get_user_by_id(users, user_id):
    for u in users:
        if u["id"] == user_id:
            return u
    return None


def calculate_average_age(users):
    total = 0
    for u in users:
        total += u["age"]
    return total / len(users)         # ❌ possible division by zero


def print_user(user):
    print("User: " + user["name"])    # ❌ type risk
    print("Age: " + user["age"])


def save_user(user):
    if not os.path.exists("data"):
        os.mkdir("data")

    f = open(DATA_FILE, "a")           # ❌ no context manager
    f.write(str(user))                 # ❌ invalid JSON write
    f.close()


def main():
    users = load_users()

    user_id = input("Enter user id: ")
    user = get_user_by_id(users, int(user_id))  # ❌ no validation

    if user:
        print_user(user)
    else:
        print("User not found")

    avg = calculate_average_age(users)
    print("Average age is " + avg)     # ❌ type error


main()                                  # ❌ missing __main__ guard
