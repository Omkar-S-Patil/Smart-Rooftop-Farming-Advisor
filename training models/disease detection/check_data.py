import os

# This matches the path in train_model.py
DIR = 'dataset/PlantVillage'

if os.path.exists(DIR):
    print("✅ SUCCESS: Found the PlantVillage folder!")

    # Check inside
    subfolders = os.listdir(DIR)
    print(f"✅ Found {len(subfolders)} plant classes.")

    if len(subfolders) > 0:
        first_class = subfolders[0]
        print(f"   Example class: {first_class}")
        files = os.listdir(os.path.join(DIR, first_class))
        print(f"   Contains {len(files)} images.")
        print("\n🚀 You are ready to run train_model.py!")
    else:
        print("⚠️ Folder exists but is empty. Check extraction.")
else:
    print(f"❌ ERROR: Could not find folder at: {os.path.abspath(DIR)}")
    print("   Please check Step 2 again.")