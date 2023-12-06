from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resources_routes import route_resources

app = FastAPI(
    title='Resources Manager Service SNMP',
    description='Service for resource managment using snmp',
    openapi_tags=[{
        'name':'Resource',
        'description':'Resources routes',
    }]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(route_resources)