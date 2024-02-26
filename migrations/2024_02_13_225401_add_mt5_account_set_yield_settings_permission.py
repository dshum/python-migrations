queries = [
    '''
    UPDATE configurations
    SET value = value::jsonb ||
                ('[{"key": "MT5AccountSetYieldSettings", "type": "ContextRule"}]')::jsonb
    WHERE "group" = 'Acl' AND "name" LIKE '%department-%';
    ''',
]