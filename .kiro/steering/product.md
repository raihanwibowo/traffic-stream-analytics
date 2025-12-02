---
inclusion: always
---

# Product Overview

This is a data streaming and processing service that handles real-time traffic data. The system integrates Kafka for message streaming, PostgreSQL for data persistence, and WebSocket for real-time client communication.

## Core Functionality

- Kafka producer/consumer for message streaming
- PostgreSQL database for storing traffic data, user information, and stock inventory
- WebSocket API for real-time client connections that forward messages to Kafka
- Traffic data processing with geolocation tracking (longitude/latitude)
- User management with role-based access
- Stock inventory tracking

## Primary Use Case

Real-time traffic monitoring system that ingests, processes, and stores vehicle count data with location information through streaming architecture.
