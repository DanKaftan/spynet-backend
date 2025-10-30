-- Migration: Add manager_id to cases to support manager-owned unassigned cases

ALTER TABLE cases
ADD COLUMN IF NOT EXISTS manager_id UUID REFERENCES users(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_cases_manager_id ON cases(manager_id);

COMMENT ON COLUMN cases.manager_id IS 'Manager who created/owns the case; used to show unassigned cases to their detectives.';
