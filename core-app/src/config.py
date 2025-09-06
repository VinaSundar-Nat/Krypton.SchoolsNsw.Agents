import os

env = os.environ.get('ENV', 'local')

env_configs = {
    'local': {
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USERNAME': 'local_user',
        'NEO4J_PASSWORD': 'local_password',
        'NEO4J_TRANSPORT': 'stdio',
        'NEO4J_DB': 'local_db',
        'API_ENDPOINT': 'localhost',
        'MCP_TRANSPORT': 'streamable-http'
    },
    'development': {
        'NEO4J_URI': 'bolt://dev-db.example.com:7687',
        'NEO4J_USERNAME': 'dev_user',
        'NEO4J_PASSWORD': 'dev_password',
        'NEO4J_TRANSPORT': 'http',
        'NEO4J_DB': 'dev_db',
        'API_ENDPOINT': 'http://localhost:8000',
        'MCP_TRANSPORT': 'streamable-http'
    },
    'production': {
        'NEO4J_URI': 'bolt://prod-db.example.com:7687',
        'NEO4J_USERNAME': 'prod_user',
        'NEO4J_PASSWORD': 'prod_password',
        'NEO4J_TRANSPORT': 'http',
        'NEO4J_DB': 'prod_db',
        'API_ENDPOINT': 'https://api.example.com',
        'MCP_TRANSPORT': 'https'
    }
}

config = env_configs.get(env, {})
