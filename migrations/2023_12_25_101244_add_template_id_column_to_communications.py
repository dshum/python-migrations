queries = [
    "ALTER TABLE communications ADD COLUMN template_id INTEGER NULL;",
    "CREATE INDEX IF NOT EXISTS communications_template_id_index ON communications (template_id);",
]