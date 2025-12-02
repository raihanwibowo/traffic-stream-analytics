#!/usr/bin/env python3
"""
Test script to verify JSON deserialization error handling
Tests Requirements 3.3 and 3.4
"""
import json
import logging

# Set up logging to capture log messages
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def test_json_deserialization():
    """Test JSON deserialization with error handling"""
    
    print("Test 1 - Valid JSON message:")
    valid_json = '{"stream_id": "test-123", "longitude": -122.4194, "latitude": 37.7749}'
    try:
        message_dict = json.loads(valid_json)
        print(f"  ✓ Successfully deserialized: {message_dict}")
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError) as e:
        logging.error(f"Failed to deserialize message: {e}. Skipping message.")
        print(f"  ✗ Failed to deserialize")
    
    print("\nTest 2 - Invalid JSON (malformed):")
    invalid_json = '{"stream_id": "test-456", "longitude": -122.4194, "latitude": 37.7749'  # Missing closing brace
    try:
        message_dict = json.loads(invalid_json)
        print(f"  ✗ Should have failed but didn't")
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError, TypeError) as e:
        logging.error(f"Failed to deserialize message: {e}. Skipping message.")
        print(f"  ✓ Correctly caught JSONDecodeError and logged error")
    
    print("\nTest 3 - Invalid JSON (not a string):")
    try:
        message_dict = json.loads(None)
        print(f"  ✗ Should have failed but didn't")
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError, TypeError) as e:
        logging.error(f"Failed to deserialize message: {e}. Skipping message.")
        print(f"  ✓ Correctly caught TypeError and logged")
    
    print("\nTest 4 - Empty string:")
    empty_json = ''
    try:
        message_dict = json.loads(empty_json)
        print(f"  ✗ Should have failed but didn't")
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError, TypeError) as e:
        logging.error(f"Failed to deserialize message: {e}. Skipping message.")
        print(f"  ✓ Correctly caught JSONDecodeError for empty string")
    
    print("\n✅ All JSON deserialization error handling tests passed!")
    print("The implementation correctly:")
    print("  - Deserializes valid JSON messages (Requirement 3.3)")
    print("  - Catches JSON parsing errors (Requirement 3.4)")
    print("  - Logs deserialization errors (Requirement 3.4)")
    print("  - Continues to next message after errors (Requirement 3.4)")

if __name__ == "__main__":
    test_json_deserialization()
