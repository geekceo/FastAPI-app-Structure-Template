from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.pkg.ssh_tools.ssh_tools import set_vpn_user
from app.configuration.api_answers import servers_setup

router = APIRouter(
    prefix='/api/v1'
)

@router.get('/set_user')
def set_user():

    return {
        'hello': 'world'
    }

@router.get('/get_user_file')
def get_user_file(data=Body()):

    return {
        'hello': 'world'
    }

@router.get('/get_users_list')
def get_users_list():

    return {
        'hello': 'world'
    }

@router.get('/setup_server')
def setup_server(ip: str = Body(embed=True), root_pass: str = Body(embed=True)):

    if set_vpn_user(ip, root_pass) == servers_setup.auth_failed_ip:
        return JSONResponse(content={
            'answer': servers_setup.auth_failed_ip
        }, status_code=401)
    
    if set_vpn_user(ip, root_pass) == servers_setup.auth_failed_pass:
        return JSONResponse(content={
            'answer': servers_setup.auth_failed_pass
        }, status_code=401)


    return {
        'answer': 'Сервер настроен и добавлен в список ваших серверов'
    }