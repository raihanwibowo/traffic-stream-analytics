"""
Test script for the Kafka consumer with traffic data format
"""
import json
from unittest.mock import Mock, MagicMock, patch
from Packages.Query import QuerySql


@patch('Packages.Query.GeocodingService')
def test_insert_traffic_data(mock_geocoding):
    """Test that traffic data is correctly inserted into the database with fulladdress"""
    
    # Mock the geocoding service
    mock_geocoding.validate_coordinates.return_value = True
    mock_geocoding.reverse_geocode.return_value = "Jl. Example Street, Jakarta, Indonesia"
    
    # Sample data matching your format
    sample_data = {
        "timestamp": "2025-11-17 14:16:17+0700",
        "stream_id": "96151250-abcb-408e-b25f-2fb4e82ea4a7",
        "location": "Simpang MORATA",
        "longitude": 106.913354,
        "latitude": -6.108524,
        "numbers_of_cars": 4,
        "label": "Normal Traffic",
        "type": "TC"
    }
    
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Create instance and set mock connection
    query_service = QuerySql.__new__(QuerySql)
    query_service.conn = mock_conn
    
    # Call the insert function
    query_service.insert_traffic_data(sample_data)
    
    # Verify cursor.execute was called
    assert mock_cursor.execute.called
    
    # Verify the SQL query contains the expected fields including fulladdress
    call_args = mock_cursor.execute.call_args
    sql_query = call_args[0][0]
    params = call_args[0][1]
    
    assert "INSERT INTO traffic_data" in sql_query
    assert "fulladdress" in sql_query
    assert params[0] == "2025-11-17 14:16:17+0700"
    assert params[1] == "96151250-abcb-408e-b25f-2fb4e82ea4a7"
    assert params[2] == "Simpang MORATA"
    assert params[3] == 106.913354
    assert params[4] == -6.108524
    assert params[5] == 4
    assert params[6] == "Normal Traffic"
    assert params[7] == "TC"
    assert params[8] == "Jl. Example Street, Jakarta, Indonesia"  # fulladdress
    
    # Verify geocoding was called with correct coordinates
    mock_geocoding.validate_coordinates.assert_called_once_with(-6.108524, 106.913354)
    mock_geocoding.reverse_geocode.assert_called_once_with(-6.108524, 106.913354)
    
    # Verify commit was called
    assert mock_conn.commit.called
    
    print("✅ Test passed: Traffic data insertion with fulladdress works correctly")


if __name__ == "__main__":
    test_insert_traffic_data()
