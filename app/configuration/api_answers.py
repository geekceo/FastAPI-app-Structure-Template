from enum import Enum
from dataclasses import dataclass

@dataclass
class servers_setup():

    auth_failed_ip: str = 'Неверный ip сервера'
    auth_failed_pass: str = 'Неверный пароль от сервера'