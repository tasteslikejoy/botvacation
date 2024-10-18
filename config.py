from pydantic import SecretStr # Это тип данных Pydantic, который используется для работы с секретными строками, такими как токены API, пароли и т.д.
# Строка будет обрабатываться безопасно и не будет выводиться в строковом представлении
from pydantic_settings import BaseSettings, SettingsConfigDict # это классы из модуля pydantic_settings, которые помогают загружать настройки приложения из конфигурационных файлов, таких как .env


# Здесь определяется класс Settings, который наследует от BaseSetting
class Settings(BaseSettings):
    # У класса есть одно свойство api_token, которое является экземпляром типа SecretStr
    api_token: SecretStr
    # Это атрибут, который позволяет настроить поведение базы структур данных
    # Здесь он устанавливается как SettingsConfigDict, в котором определено, что конфигурация должна быть загружена из файла .env с кодировкой utf-8.
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

# Здесь создается экземпляр класса Settings
config = Settings()


