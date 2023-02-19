from fastapi import APIRouter, Body
from app.pkg.ssh_tools.ssh_tools import set_vpn_user

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

    set_vpn_user(ip, root_pass)

    return {
        'answer': 'OK'
    }