import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = __name__):
    """
    Configura e retorna um logger com formatação padronizada e rotação de arquivos.
    
    Args:
        name: Nome do módulo que está usando o logger
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicação de handlers para não registrar logs múltiplos
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Formato padrão: [timestamp] [nível] [módulo] mensagem
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # --- Handler para console (saída padrão) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # --- Handler para arquivo com rotação ---
    # Criar diretório de logs se não existir
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'app.log')
    
    # Usar o handler padrão do Python com rotação de arquivo.
    # Ele rotaciona o log quando atinge 10MB e mantém 5 arquivos de backup.
    file_handler = RotatingFileHandler(
        log_file,
        mode='a',
        maxBytes=10*1024*1024, # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

