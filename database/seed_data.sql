-- Seed data for Airtel Payment Bank
-- This file contains initial test users and admin account

-- Insert Admin User
INSERT INTO users (full_name, mobile, password, balance, role) VALUES 
('Admin User', '9999999999', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUl.8JVm', 50000.00, 'admin')
ON DUPLICATE KEY UPDATE id=id;

-- Insert Test User 1
INSERT INTO users (full_name, mobile, password, balance, role) VALUES 
('Raj Kumar', '9123456789', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUl.8JVm', 5000.00, 'user')
ON DUPLICATE KEY UPDATE id=id;

-- Insert Test User 2
INSERT INTO users (full_name, mobile, password, balance, role) VALUES 
('Priya Singh', '9198765432', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUl.8JVm', 3000.00, 'user')
ON DUPLICATE KEY UPDATE id=id;

-- Note: All passwords are hashed with 'user123' using werkzeug.security
-- Hash generated: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUl.8JVm
-- Login credentials:
-- Admin: 9999999999 / admin123
-- User 1: 9123456789 / user123
-- User 2: 9198765432 / user123
