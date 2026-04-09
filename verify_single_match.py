import requests
import json
import sys

# Standard output to UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def verify_single_item_matching():
    try:
        # 1. Test "Tomato"
        print("Testing single ingredient: 'Tomato'...")
        res = requests.post("http://127.0.0.1:8000/recipes/match", json={"ingredients": ["Tomato"]})
        if res.status_code == 200:
            matches = res.json().get("matches", [])
            print(f"Result: Found {len(matches)} recipes for 'Tomato'.")
            for m in matches:
                 print(f" - {m['title']}")
        else:
            print(f"Error: {res.status_code}")

        # 2. Test "Pasta"
        print("\nTesting single ingredient: 'Pasta'...")
        res = requests.post("http://127.0.0.1:8000/recipes/match", json={"ingredients": ["Pasta"]})
        if res.status_code == 200:
            matches = res.json().get("matches", [])
            print(f"Result: Found {len(matches)} recipes for 'Pasta'.")
            for m in matches:
                 print(f" - {m['title']}")

        # 3. Test "Garlic"
        print("\nTesting single ingredient: 'Garlic'...")
        res = requests.post("http://127.0.0.1:8000/recipes/match", json={"ingredients": ["Garlic"]})
        if res.status_code == 200:
            matches = res.json().get("matches", [])
            print(f"Result: Found {len(matches)} recipes for 'Garlic'.")
            
        print("\nVerification Complete.")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    verify_single_item_matching()
