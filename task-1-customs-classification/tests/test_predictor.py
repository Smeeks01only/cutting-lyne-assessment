import sys
from pathlib import Path

# Add project root to sys.path to allow importing from src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.predictor import classify_product

def test_stainless_steel_screw():
    result = classify_product("stainless steel automotive screw")
    
    assert result["input"] == "stainless steel automotive screw"
    assert result["status"] == "classified"
    # Ensure hs_code is present
    assert "hs_code" in result
    
    print("Test passed! Result:")
    print(result)

if __name__ == "__main__":
    test_stainless_steel_screw()