# Design Document

## Overview

The geocoding service extends the existing traffic monitoring system by adding reverse geocoding capabilities. It consumes traffic messages from Kafka, enriches them with human-readable addresses by calling a geocoding API, and stores the enriched data in PostgreSQL. The service follows the existing architecture patterns using the service layer pattern with static factory methods.

## Architecture

### Component Diagram

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Kafka     │─────▶│  Geocoding       │─────▶│  PostgreSQL     │
│   Topic     │      │  Consumer        │      │  traffic_data   │
└─────────────┘      └──────────────────┘      └─────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Geocoding API  │
                     │  (Nominatim)    │
                     └─────────────────┘
```

### Data Flow

1. Consumer reads traffic message from Kafka topic
2. Message is deserialized from JSON
3. Coordinates are validated
4. Reverse geocoding API is called with coordinates
5. Address is extracted from API response
6. Enriched data is inserted into PostgreSQL
7. Transaction is committed
8. Process repeats for next message

## Components and Interfaces

### GeocodingService

A new service class that handles reverse geocoding API calls.

```python
class GeocodingService:
    @staticmethod
    def reverse_geocode(latitude: float, longitude: float) -> Optional[str]:
        """
        Converts coordinates to address using Nominatim API.
        Returns address string or None if lookup fails.
        """
        pass
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> bool:
        """
        Validates coordinate ranges.
        Returns True if valid, False otherwise.
        """
        pass
```

### GeocodingParser

Extension to the Parser module that handles geocoding-specific message processing.

```python
class GeocodingParser:
    @staticmethod
    def consume_and_geocode(topic: str):
        """
        Consumes messages from Kafka, geocodes them, and stores in database.
        """
        pass
    
    @staticmethod
    def process_message(message: dict) -> dict:
        """
        Processes a single message: validates, geocodes, enriches.
        Returns enriched message dict.
        """
        pass
```

### QuerySql Extensions

Add method to insert enriched traffic data.

```python
def insert_traffic_data(self, data: dict) -> bool:
    """
    Inserts enriched traffic data into traffic_data table.
    Returns True on success, False on failure.
    """
    pass
```

## Data Models

### Kafka Message Format (Input)

```json
{
  "timestamp": "2025-11-20T10:30:00Z",
  "stream_id": "550e8400-e29b-41d4-a716-446655440000",
  "location": "Highway 101",
  "longitude": -122.4194,
  "latitude": 37.7749,
  "numbers_of_cars": 45,
  "label": "northbound",
  "type": "highway"
}
```

### Enriched Data Format (Output to DB)

All fields from input message plus:
- `address`: String containing human-readable address (e.g., "San Francisco, CA, USA")
- `created_at`: Timestamp of database insertion

### Geocoding API Response (Nominatim)

```json
{
  "display_name": "San Francisco, California, United States",
  "address": {
    "city": "San Francisco",
    "state": "California",
    "country": "United States"
  }
}
```

## Correctness
 Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

After reviewing all acceptance criteria, several properties are logically redundant or can be consolidated:

- Properties 1.2 and 1.3 (longitude/latitude validation) can be combined into a single coordinate validation property
- Properties 2.1, 2.4, and 6.3 (error logging) can be consolidated into a general error logging property
- Properties 4.3 and 4.4 (database failure handling) can be combined into a single transaction rollback property
- Properties 6.2 and 6.3 overlap with other logging requirements and can be consolidated

### Property 1: Coordinate extraction preserves values

*For any* traffic message containing longitude and latitude fields, extracting the coordinates should return values equal to the original message values.

**Validates: Requirements 1.1**

### Property 2: Coordinate validation enforces valid ranges

*For any* pair of coordinates, validation should return true if and only if longitude is in [-180, 180] and latitude is in [-90, 90].

**Validates: Requirements 1.2, 1.3**

### Property 3: Invalid coordinates skip geocoding

*For any* traffic message with invalid coordinates, the processing should not invoke the geocoding API and should log an error.

**Validates: Requirements 1.4**

### Property 4: Valid coordinates trigger geocoding

*For any* traffic message with valid coordinates, the processing should invoke the geocoding API with those exact coordinates.

**Validates: Requirements 1.5**

### Property 5: API failures preserve data with null address

*For any* traffic message where geocoding API fails, the data should be stored in the database with all original fields intact and address field set to null or empty.

**Validates: Requirements 2.2**

### Property 6: Processing continues after failures

*For any* sequence of traffic messages where some geocoding operations fail, all messages in the sequence should be processed (no early termination).

**Validates: Requirements 2.5**

### Property 7: Message deserialization round-trip

*For any* valid traffic message dictionary, serializing to JSON then deserializing should produce an equivalent dictionary.

**Validates: Requirements 3.3**

### Property 8: Deserialization failures are non-fatal

*For any* invalid JSON message, the consumer should log the error and continue processing without crashing.

**Validates: Requirements 3.4**

### Property 9: All required fields are extracted

*For any* deserialized message, the extraction should retrieve all eight required fields: timestamp, stream_id, location, longitude, latitude, numbers_of_cars, label, and type.

**Validates: Requirements 3.5**

### Property 10: Database insertion preserves all fields

*For any* enriched traffic data, the database record should contain all original message fields plus the address field.

**Validates: Requirements 4.2**

### Property 11: Failed transactions are not committed

*For any* database insertion that fails, no transaction commit should occur and an error should be logged.

**Validates: Requirements 4.3, 4.4**

### Property 12: Successful transactions are committed

*For any* database insertion that succeeds, the transaction should be committed immediately.

**Validates: Requirements 4.5**

### Property 13: API key is included when configured

*For any* geocoding API request when an API key is configured, the request should include the API key in the appropriate header or parameter.

**Validates: Requirements 5.4**

### Property 14: Errors are logged with context

*For any* error condition (API failure, validation failure, database failure), a log entry should be created containing sufficient context to identify the error source and affected data.

**Validates: Requirements 2.1, 2.4, 6.3**

### Property 15: Successful processing is logged

*For any* successfully processed message, a log entry should be created containing the stream_id and resolved address.

**Validates: Requirements 6.2**

## Error Handling

### Coordinate Validation Errors
- Invalid longitude/latitude values are logged with the message stream_id
- Processing continues with next message
- No geocoding API call is made

### Geocoding API Errors
- Network failures: Log error, store data with null address, continue
- Timeout (5 seconds): Log timeout, store data with null address, continue
- HTTP errors (4xx, 5xx): Log status code and response, store data with null address, continue
- Malformed response: Log parsing error, store data with null address, continue

### Kafka Consumer Errors
- Connection failures: Log error and retry with exponential backoff
- Deserialization errors: Log malformed message, skip message, continue
- Topic not found: Log error and exit with non-zero status

### Database Errors
- Connection failures: Log error and retry with exponential backoff
- Insert failures: Log error with message details, rollback transaction, continue
- Constraint violations: Log error, skip message, continue

### Configuration Errors
- Missing required environment variables: Log error and exit immediately with non-zero status
- Invalid configuration values: Log error and exit immediately with non-zero status

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and integration points:

- Coordinate validation with boundary values (exactly -180, 180, -90, 90)
- Message field extraction with complete and incomplete messages
- Database connection and query execution
- Configuration loading from environment variables
- Error logging format and content

### Property-Based Testing

We will use the `hypothesis` library for Python property-based testing. Each property test will run a minimum of 100 iterations with randomly generated inputs.

Property tests will verify:

- **Property 1**: Generate random messages with coordinate values, verify extraction returns same values
- **Property 2**: Generate random coordinate pairs (including invalid ranges), verify validation logic
- **Property 3**: Generate messages with invalid coordinates, verify no API calls made
- **Property 4**: Generate messages with valid coordinates, verify API is invoked
- **Property 5**: Simulate API failures with random messages, verify data stored with null address
- **Property 6**: Generate sequences of messages with random failures, verify all processed
- **Property 7**: Generate random valid message dictionaries, verify JSON round-trip
- **Property 8**: Generate invalid JSON strings, verify consumer continues
- **Property 9**: Generate random messages, verify all 8 required fields extracted
- **Property 10**: Generate random enriched data, verify all fields in database
- **Property 11**: Simulate database failures, verify no commits occur
- **Property 12**: Generate random successful insertions, verify commits occur
- **Property 13**: Generate random API requests with/without keys, verify key inclusion
- **Property 14**: Generate random error conditions, verify logging contains context
- **Property 15**: Generate random successful messages, verify logging contains stream_id and address

Each property-based test will be tagged with a comment in this format:
```python
# Feature: geocoding-service, Property X: <property description>
```

### Integration Testing

Integration tests will verify end-to-end flows:

- Kafka → Geocoding → Database pipeline with real Kafka and PostgreSQL instances
- API integration with actual Nominatim service (or mock server)
- Error recovery scenarios with simulated failures

## Implementation Notes

### Geocoding API Selection

We will use the Nominatim API (OpenStreetMap's geocoding service) because:
- Free and open-source
- No API key required for basic usage (though rate-limited)
- Supports reverse geocoding
- Returns structured address data
- Can be self-hosted if needed

API endpoint: `https://nominatim.openstreetmap.org/reverse`

Rate limiting: 1 request per second for free tier. Implementation should include rate limiting logic.

### Environment Variables

New environment variables required:
- `GEOCODING_API_URL`: Nominatim API endpoint (default: https://nominatim.openstreetmap.org/reverse)
- `GEOCODING_API_KEY`: Optional API key for premium services
- `GEOCODING_TIMEOUT`: API request timeout in seconds (default: 5)
- `TRAFFIC_TOPIC`: Kafka topic for traffic data (default: "traffic_data")

### Performance Considerations

- Geocoding API calls are synchronous and may be slow (100-500ms per request)
- Consider implementing caching for frequently seen coordinates
- Rate limiting may require throttling message processing
- Database connection pooling should be used for concurrent inserts

### Dependencies

New Python packages required:
- `requests`: For HTTP API calls to geocoding service
- `hypothesis`: For property-based testing
