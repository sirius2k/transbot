-- TransBot Database Initialization Script
-- This script runs automatically when PostgreSQL container is first created

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS transbot;

-- Set default schema
SET search_path TO transbot, public;

-- Future tables will be created here by application migrations
-- Example placeholder:
-- CREATE TABLE IF NOT EXISTS translation_history (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     source_text TEXT NOT NULL,
--     target_text TEXT NOT NULL,
--     source_lang VARCHAR(10) NOT NULL,
--     target_lang VARCHAR(10) NOT NULL,
--     model VARCHAR(50) NOT NULL,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA transbot TO transbot_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA transbot TO transbot_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA transbot TO transbot_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA transbot GRANT ALL ON TABLES TO transbot_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA transbot GRANT ALL ON SEQUENCES TO transbot_user;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'TransBot database initialized successfully';
END $$;
