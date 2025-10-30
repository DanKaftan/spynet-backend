-- Migration: Split roles and add many-to-many manager<->detective assignments

-- 1) Role tables
CREATE TABLE IF NOT EXISTS managers (
  id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS detectives (
  id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 2) Join table for many-to-many manager<->detective
CREATE TABLE IF NOT EXISTS detective_manager (
  manager_id UUID NOT NULL REFERENCES managers(id) ON DELETE CASCADE,
  detective_id UUID NOT NULL REFERENCES detectives(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (manager_id, detective_id)
);

CREATE INDEX IF NOT EXISTS idx_dm_manager_id ON detective_manager(manager_id);
CREATE INDEX IF NOT EXISTS idx_dm_detective_id ON detective_manager(detective_id);

COMMENT ON TABLE managers IS '1-1 profile for manager users (subset of users)';
COMMENT ON TABLE detectives IS '1-1 profile for detective users (subset of users)';
COMMENT ON TABLE detective_manager IS 'Many-to-many assignments between managers and detectives';

-- 3) Backfill from users.role
-- Create missing role profiles based on users.role values
INSERT INTO managers (id)
SELECT id FROM users WHERE role = 'manager'
ON CONFLICT (id) DO NOTHING;

INSERT INTO detectives (id)
SELECT id FROM users WHERE role = 'detective'
ON CONFLICT (id) DO NOTHING;

-- 4) Cases ownership: keep manager_id on cases (ensure column exists)
ALTER TABLE cases
ADD COLUMN IF NOT EXISTS manager_id UUID REFERENCES managers(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_cases_manager_id ON cases(manager_id);

-- If cases.manager_id previously pointed to users(id), ensure referential integrity manually as needed.

-- 5) Optional cleanup: drop users.manager_id if present (moved to join table)
-- ALTER TABLE users DROP COLUMN IF EXISTS manager_id;
