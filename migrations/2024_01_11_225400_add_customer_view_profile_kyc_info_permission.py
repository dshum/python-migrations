queries = [
    "update configurations set value = value::jsonb || ('[{\"key\": \"customer_view_profile_kyc_info\", \"type\": "
    "\"VisualRule\"}]')::jsonb WHERE \"group\" = 'Acl' and name LIKE '%department-%';",
]
