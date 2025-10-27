-- Supabase Database Schema for SpyNet Backend

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('detective', 'manager')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cases Table
CREATE TABLE IF NOT EXISTS cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    details TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'closed')),
    detective_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_cases_detective_id ON cases(detective_id);
CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cases_updated_at
    BEFORE UPDATE ON cases
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;

-- RLS Policies (backend handles all access, so allow service role)
CREATE POLICY "Allow service role full access to users" ON users
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow service role full access to cases" ON cases
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Comments for documentation
COMMENT ON TABLE users IS 'User profiles with detective or manager roles';
COMMENT ON TABLE cases IS 'Case records assignable to detectives';
COMMENT ON COLUMN users.role IS 'User role: detective or manager';
COMMENT ON COLUMN cases.status IS 'Case status: open, in_progress, or closed';
COMMENT ON COLUMN cases.detective_id IS 'Assigned detective (optional, can be null)';
