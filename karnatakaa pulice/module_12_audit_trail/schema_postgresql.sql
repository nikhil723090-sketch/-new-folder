CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(80) NOT NULL,
    role VARCHAR(40) NOT NULL,
    action VARCHAR(80) NOT NULL,
    question TEXT,
    ai_response TEXT,
    generated_sql TEXT,
    prediction TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs (user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_role ON audit_logs (role);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs (action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs (created_at);
