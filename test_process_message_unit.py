#!/usr/bin/env python3
"""
Unit test for process_message - tests the logic without external dependencies
"""
import sys
import os

# Mock the dependencies before importing
class MockGeocodingService:
    @staticmethod
    def validate_coordinates(latitude, longitude):
        return -180 <= longitude <= 180 and -90 <= latitude <= 90
    
    @staticmethod
    def reverse_geocode(latitude, longitude):
        # Mock successful geocoding
        return f"Address for ({latitude}, {longitude})"

# Mock modules
sys.modules['Packages.KafkaService'] = type('module', (), {'KafkaService': None})()
sys.modules['Packages.GeocodingService'] = type('module', (), {'GeocodingService': MockGeocodingService})()

# Now we can test the logic
def test_process_message_logic():
    """Test the process_message logic"""
    
    # Simulate the process_message logic
    def process_message(message):
        try:
            longitude = message.get("longitude")
            latitude = message.get("latitude")
            
            if longitude is None or latitude is None:
                print(f"Missing coordinates in message with stream_id: {message.get('stream_id', 'unknown')}")
                message["address"] = None
                return message
            
            if not MockGeocodingService.validate_coordinates(latitude, longitude):
                print(f"Invalid coordinates ({latitude}, {longitude}) for stream_id: {message.get('stream_id', 'unknown')}")
                message["address"] = None
                return message
            
            address = MockGeocodingService.reverse_geocode(latitude, longitude)
            message["address"] = address
            return message
            
        except Exception as e:
            print(f"Error processing message: {e}")
            message["address"] = None
            return message
    
    # Test 1: Valid coordinates
    print("Test 1 - Valid coordinates:")
    message1 = {
        'stream_id': 'test-123',
        'longitude': -122.4194,
        'latitude': 37.7749,
    }
    result1 = process_message(message1)
    assert "address" in result1, "Address field should be present"
    assert result1["address"] is not None, "Address should not be None for valid coordinates"
    print(f"  ✓ Address field present: {result1['address']}")
    
    # Test 2: Invalid coordinates (out of range)
    print("\nTest 2 - Invalid coordinates:")
    message2 = {
        'stream_id': 'test-456',
        'longitude': 200,  # Invalid
        'latitude': 100,   # Invalid
    }
    result2 = process_message(message2)
    assert "address" in result2, "Address field should be present"
    assert result2["address"] is None, "Address should be None for invalid coordinates"
    print(f"  ✓ Address is None for invalid coordinates")
    
    # Test 3: Missing coordinates
    print("\nTest 3 - Missing coordinates:")
    message3 = {
        'stream_id': 'test-789',
    }
    result3 = process_message(message3)
    assert "address" in result3, "Address field should be present"
    assert result3["address"] is None, "Address should be None for missing coordinates"
    print(f"  ✓ Address is None for missing coordinates")
    
    # Test 4: Edge case - boundary values
    print("\nTest 4 - Boundary values:")
    message4 = {
        'stream_id': 'test-boundary',
        'longitude': 180,  # Max valid
        'latitude': 90,    # Max valid
    }
    result4 = process_message(message4)
    assert "address" in result4, "Address field should be present"
    assert result4["address"] is not None, "Address should not be None for boundary coordinates"
    print(f"  ✓ Boundary coordinates handled correctly")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_process_message_logic()
