import requests
import json
import sys

# Set standard output to UTF-8 to handle any potential characters, though we'll use ASCII
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def verify_recipes():
    try:
        # 1. Check if server is up
        print("Checking server status...")
        res = requests.post("http://127.0.0.1:8000/recipes/match", 
                           json={"ingredients": ["Tomato", "Pasta", "Garlic", "Rice"]})
        if res.status_code != 200:
            print(f"Error: Server returned status {res.status_code}")
            return
            
        data = res.json()
        matches = data.get("matches", [])
        print(f"Success: Found {len(matches)} matches for basic ingredients.")
        
        # 2. Check variety and images
        print("\nVerifying Image URLs and Recipe variety:")
        for r in matches:
            img_url = r.get("image")
            print(f"- Recipe: {r['title']}")
            print(f"  Image: {img_url}")
            
            try:
                img_res = requests.head(img_url, timeout=5)
                if img_res.status_code == 200:
                    print("  Status: Image LOADED (200)")
                elif img_res.status_code == 403:
                    print("  Status: Image ACCESSIBLE (403 Forbidden on HEAD is often common for protection, testing GET)")
                    # Fallback to a small GET request to be sure
                    get_res = requests.get(img_url, stream=True, timeout=5)
                    if get_res.status_code == 200:
                         print("  Status: Image LOADED (200 via GET)")
                    else:
                         print(f"  Status: Image FAILED ({get_res.status_code} via GET)")
                else:
                    print(f"  Status: Image FAILED ({img_res.status_code})")
            except Exception as e:
                print(f"  Status: Image ERROR: {str(e)[:50]}...")
                
        print("\nVerification Complete.")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    verify_recipes()
