"""
Test script to verify Kaggle API credentials are working
"""

import os

def check_kaggle_setup():
    print("="*60)
    print("Kaggle API Setup Verification")
    print("="*60)
    
    # Check if kaggle.json exists
    kaggle_path = os.path.join(os.path.expanduser('~'), '.kaggle', 'kaggle.json')
    
    print(f"\nLooking for kaggle.json at:")
    print(f"  {kaggle_path}")
    
    if os.path.exists(kaggle_path):
        print("\n✓ kaggle.json found!")
        
        # Try to import and authenticate
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            print("✓ Kaggle API library installed")
            
            api = KaggleApi()
            api.authenticate()
            print("✓ Authentication successful!")
            
            # Test by listing a dataset
            print("\nTesting API by listing competitions...")
            competitions = api.competitions_list()
            print(f"✓ API working! Found {len(competitions)} competitions")
            
            print("\n" + "="*60)
            print("SUCCESS! Your Kaggle API is ready to use!")
            print("="*60)
            print("\nYou can now run: python prepare_kaggle_dataset.py")
            
            return True
            
        except ImportError:
            print("\n✗ Kaggle library not installed")
            print("\nInstall with: pip install kaggle")
            return False
            
        except Exception as e:
            print(f"\n✗ Authentication failed: {e}")
            print("\nPossible issues:")
            print("  1. kaggle.json has incorrect format")
            print("  2. API token has been revoked")
            print("  3. Check file permissions")
            return False
    else:
        print("\n✗ kaggle.json NOT found!")
        print("\nPlease follow these steps:")
        print("  1. Go to https://www.kaggle.com/")
        print("  2. Click your profile → Settings")
        print("  3. Scroll to 'API' section")
        print("  4. Click 'Create New API Token'")
        print("  5. Move downloaded kaggle.json to:")
        print(f"     {kaggle_path}")
        return False

if __name__ == '__main__':
    check_kaggle_setup()
