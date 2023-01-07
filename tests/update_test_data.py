import os
import shutil
# This file allows easy updating of the test_data

# Get folders of test data
folders = os.listdir("test_data/active_withdrawn")

# Delete test data
shutil.rmtree("test_data/active_withdrawn")

# Replace test data
for folder in folders:
    shutil.copytree(f"../data/active_withdrawn/{folder}", f"test_data/active_withdrawn/{folder}")
