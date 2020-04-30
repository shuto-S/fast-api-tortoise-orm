from starlette.requests import Request

def get_db_connection(request: Request):
    return request.state.connection
