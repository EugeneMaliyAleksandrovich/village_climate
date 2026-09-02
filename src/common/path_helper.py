from pathlib import Path

class ProjectPaths:
    """Управление путями проекта"""
    def __init__(self):
        self._root = None
        self.setup()

    def setup(self):
        """Настройка всех путей проекта"""
        self._root = self._find_root()
        self.data_dir = Path(self._root / "data")
        self.logs_dir = Path(self._root / "logs")

    def _find_root(self) -> Path:
        """
        Найти корень проекта
        Маркеры: requirements.txt, .git, README.md
        """
        # Начинаем с директории этого файла
        current = Path(__file__).resolve().parent
        
        # Маркеры корня проекта
        markers = ['requirements.txt', 'setup.py', 'pyproject.toml', '.git']
        
        # Ищем вверх до 10 уровней
        for _ in range(10):
            for marker in markers:
                if (current / marker).exists():
                    return current
            current = current.parent
            
            # Если дошли до корня файловой системы
            if current == current.parent:
                break
                
        # Если не нашли, поднимаемся на 1 уровень от текущего файла
        return Path(__file__).resolve().parent.parent
