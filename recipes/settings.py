from pydantic import BaseSettings


#  Читает переменные окружения, валидирует и если их там нет, то устанавливает дефолтные значения, указанные тут.
class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str


#  Для считывания переменных окружения из файла. Нужна библиотека python-dotenv.
settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
