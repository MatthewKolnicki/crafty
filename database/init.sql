-- Database initialization script for Crafty CRM
-- This script creates the basic schema and tables

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE companies (
    Company_id SERIAL PRIMARY KEY,
    Company_name VARCHAR(255) NOT NULL,
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contacts (
    Contact_id SERIAL PRIMARY KEY,
    Contact_name VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Company_id INTEGER REFERENCES companies(Company_id),
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE client_engagements (
    Engagement_id SERIAL PRIMARY KEY,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Type VARCHAR(32),
    Contact_id INTEGER REFERENCES contacts(Contact_id),
    Company_id INTEGER REFERENCES companies(Company_id)
);

CREATE TABLE support_tickets (
    Ticket_id SERIAL PRIMARY KEY,
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Closed_at TIMESTAMP,
    Status VARCHAR(32) DEFAULT 'Open',
    Subject VARCHAR(500),
    Company_id INTEGER REFERENCES companies(Company_id),
    Contact_id INTEGER REFERENCES contacts(Contact_id),
    Properties JSONB
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_contacts_company_id ON contacts(Company_id);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(Email);
CREATE INDEX IF NOT EXISTS idx_engagements_contact_id ON client_engagements(Contact_id);
CREATE INDEX IF NOT EXISTS idx_engagements_company_id ON client_engagements(Company_id);
CREATE INDEX IF NOT EXISTS idx_tickets_company_id ON support_tickets(Company_id);
CREATE INDEX IF NOT EXISTS idx_tickets_contact_id ON support_tickets(Contact_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON support_tickets(Status);
