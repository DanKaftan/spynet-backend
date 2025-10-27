-- Add manager assignment to users table
-- This allows detectives to be assigned to specific managers

-- Add manager_id column to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS manager_id UUID REFERENCES users(id) ON DELETE SET NULL;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_users_manager_id ON users(manager_id);

-- Add comment for documentation
COMMENT ON COLUMN users.manager_id IS 'Assigned manager for detective users (self-reference to users.id)';

-- Optional: Add check constraint to ensure only managers can be assigned as managers
-- (This prevents circular references and ensures only managers can manage detectives)
-- Note: This is enforced in application logic since a manager can also have a manager

-- Sample query to assign a detective to a manager:
-- UPDATE users SET manager_id = 'manager-uuid-here' WHERE id = 'detective-uuid-here';

