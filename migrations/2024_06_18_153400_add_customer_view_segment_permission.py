queries = [
    '''
    UPDATE configurations
        SET value =
            value::jsonb ||
            ('[{\"key\": \"customer_view_segment\", \"type\": \"VisualRule\"}]')::jsonb
        WHERE \"group\" = 'Acl' AND \"name\" LIKE '%department-%';
    ''',
]