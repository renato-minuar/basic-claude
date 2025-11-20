-- Development Journal Schema
CREATE TABLE IF NOT EXISTS journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    session_id TEXT NOT NULL,
    user_prompt TEXT NOT NULL,
    summary TEXT NOT NULL,
    tools_used TEXT, -- JSON array of tool names
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_timestamp ON journal(timestamp);
CREATE INDEX IF NOT EXISTS idx_session ON journal(session_id);
