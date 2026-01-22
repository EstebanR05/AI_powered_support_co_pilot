DROP TABLE IF EXISTS tickets CASCADE;
DROP TYPE IF EXISTS ticket_category CASCADE;
DROP TYPE IF EXISTS ticket_sentiment CASCADE;

-- Create ENUM types for categories and sentiments
CREATE TYPE ticket_category AS ENUM (
    'Técnico',
    'Facturación', 
    'Comercial',
    'Soporte'
);

CREATE TYPE ticket_sentiment AS ENUM (
    'Positivo',
    'Neutral',
    'Negativo'
);

-- Create the main tickets table
CREATE TABLE tickets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    description TEXT NOT NULL,
    category ticket_category,
    sentiment ticket_sentiment,
    processed BOOLEAN DEFAULT FALSE NOT NULL
);

-- Enable Row Level Security
ALTER TABLE tickets ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view all tickets" ON tickets
    FOR SELECT USING (true);

CREATE POLICY "Users can insert tickets" ON tickets
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update tickets" ON tickets
    FOR UPDATE USING (true);
