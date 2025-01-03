# Replace 'YOUR-LICENSE-KEY-HERE' with your actual license key
import Metashape
license_key = "YOUR-LICENSE-KEY-HERE"

try:
    success = Metashape.license.activate("........")
    if success:
        print("License activated successfully!")
    else:
        print("Failed to activate license. Please check the license key or your internet connection.")
except Exception as e:
    print(f"An error occurred during license activation: {e}")
