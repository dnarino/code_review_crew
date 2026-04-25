from hooks import read_file_hook
import os 

# 1. Setup the inputs
# Make sure the path is correct relative to where you run the script

test_inputs = {'file_path' : 'files/code_changes.txt'}
print(f"---Testing read_file_hook with:{test_inputs["file_path"]}---")

try:
    #2.run the hook
    result =read_file_hook(test_inputs)
    #3. Verify results
    if "file_content" in result:
        print("✅ SUCCESS: 'file_content' was added to inputs.")
        print("\n--- Content Preview (First 5 lines) ---")
        print("\n".join(result['file_content'].splitlines()[:5]))
    else:
        print("❌ FAILED: 'file_content' missing from result.")
except Exception as e:
    print(f"💥 ERROR during execution: {e}")