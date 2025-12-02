# Implementation Plan

- [x] 1. Set up geocoding service infrastructure
  - Create `Packages/GeocodingService.py` with coordinate validation and API client
  - Add environment variable configuration for geocoding API
  - Install required dependencies: `requests` and `hypothesis`
  - _Requirements: 1.2, 1.3, 1.5, 5.2, 5.3, 5.4_

- [ ]* 1.1 Write property test for coordinate validation
  - **Property 2: Coordinate validation enforces valid ranges**
  - **Validates: Requirements 1.2, 1.3**

- [x] 2. Implement coordinate validation logic
  - Write `validate_coordinates()` method to check longitude [-180, 180] and latitude [-90, 90]
  - Return boolean indicating validity
  - _Requirements: 1.2, 1.3_

- [ ]* 2.1 Write property test for coordinate extraction
  - **Property 1: Coordinate extraction preserves values**
  - **Validates: Requirements 1.1**

- [x] 3. Implement reverse geocoding API client
  - Write `reverse_geocode()` method to call Nominatim API
  - Handle API response parsing to extract address string
  - Implement 5-second timeout for API requests
  - Include API key in requests when configured
  - _Requirements: 1.5, 2.3, 5.4_

- [ ]* 3.1 Write property test for API key inclusion
  - **Property 13: API key is included when configured**
  - **Validates: Requirements 5.4**

- [x] 4. Implement error handling for geocoding failures
  - Add try-except blocks for network errors, timeouts, and HTTP errors
  - Log errors with coordinate details
  - Return None when geocoding fails
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ]* 4.1 Write property test for API failure handling
  - **Property 5: API failures preserve data with null address**
  - **Validates: Requirements 2.2**

- [ ]* 4.2 Write property test for error logging
  - **Property 14: Errors are logged with context**
  - **Validates: Requirements 2.1, 2.4, 6.3**

- [x] 5. Create geocoding parser for Kafka message processing
  - Create `GeocodingParser` class in `Packages/Parser.py`
  - Implement `consume_and_geocode()` method to consume from Kafka topic
  - Read topic name from environment variable
  - _Requirements: 3.1, 3.2, 5.1_

- [x] 6. Implement message processing logic
  - Write `process_message()` method to handle individual messages
  - Extract coordinates from message
  - Validate coordinates and skip geocoding if invalid
  - Call geocoding service for valid coordinates
  - Enrich message with address field
  - _Requirements: 1.1, 1.4, 3.5_

- [ ]* 6.1 Write property test for invalid coordinate handling
  - **Property 3: Invalid coordinates skip geocoding**
  - **Validates: Requirements 1.4**

- [ ]* 6.2 Write property test for valid coordinate handling
  - **Property 4: Valid coordinates trigger geocoding**
  - **Validates: Requirements 1.5**

- [ ]* 6.3 Write property test for field extraction
  - **Property 9: All required fields are extracted**
  - **Validates: Requirements 3.5**

- [ ] 7. Implement JSON deserialization with error handling
  - Add try-except for JSON parsing errors
  - Log deserialization errors and continue to next message
  - _Requirements: 3.3, 3.4_

- [ ]* 7.1 Write property test for JSON round-trip
  - **Property 7: Message deserialization round-trip**
  - **Validates: Requirements 3.3**

- [ ]* 7.2 Write property test for deserialization error handling
  - **Property 8: Deserialization failures are non-fatal**
  - **Validates: Requirements 3.4**

- [ ] 8. Extend database query module for traffic data insertion
  - Add `insert_traffic_data()` method to `QuerySql` class in `Packages/Query.py`
  - Accept enriched message dictionary as parameter
  - Insert all original fields plus address into traffic_data table
  - _Requirements: 4.1, 4.2_

- [ ]* 8.1 Write property test for field preservation in database
  - **Property 10: Database insertion preserves all fields**
  - **Validates: Requirements 4.2**

- [ ] 9. Implement database transaction handling
  - Wrap insert in try-except block
  - Commit transaction on success
  - Rollback transaction on failure
  - Log errors with message details
  - Return boolean indicating success/failure
  - _Requirements: 4.3, 4.4, 4.5_

- [ ]* 9.1 Write property test for failed transaction handling
  - **Property 11: Failed transactions are not committed**
  - **Validates: Requirements 4.3, 4.4**

- [ ]* 9.2 Write property test for successful transaction handling
  - **Property 12: Successful transactions are committed**
  - **Validates: Requirements 4.5**

- [ ] 10. Implement resilient message processing loop
  - Ensure processing continues after geocoding failures
  - Ensure processing continues after database failures
  - Store data with null address when geocoding fails
  - _Requirements: 2.2, 2.5_

- [ ]* 10.1 Write property test for processing continuation
  - **Property 6: Processing continues after failures**
  - **Validates: Requirements 2.5**

- [ ] 11. Add comprehensive logging throughout the service
  - Log service startup with configuration details
  - Log Kafka connection status
  - Log PostgreSQL connection status
  - Log successful message processing with stream_id and address
  - Log all errors with sufficient context
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 11.1 Write property test for success logging
  - **Property 15: Successful processing is logged**
  - **Validates: Requirements 6.2**

- [ ] 12. Implement configuration validation at startup
  - Check for required environment variables (KAFKA_BOOTSTRAP_SERVERS, TRAFFIC_TOPIC, GEOCODING_API_URL)
  - Log error and exit with non-zero status if missing
  - Log startup configuration details
  - _Requirements: 5.1, 5.2, 5.3, 5.5, 6.1_

- [ ] 13. Create CLI entry point for geocoding consumer
  - Add geocoding consumer mode to `Worker.py` or create new entry point
  - Wire up GeocodingParser to run as consumer
  - _Requirements: 3.1, 3.2_

- [ ] 14. Update environment configuration
  - Add new environment variables to `.env` file
  - Document required and optional variables
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 15. Write integration tests for end-to-end flow
  - Test Kafka → Geocoding → Database pipeline
  - Test with mock Kafka and PostgreSQL
  - Test error scenarios with simulated failures

- [ ] 16. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
