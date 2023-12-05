import os
from datetime import datetime
from pathlib import Path

from infrastructure.config.configuration import Config
from infrastructure.logging.infrastructure_logger import ProgramLogger


class ProjectDefinition:

    @classmethod
    def get_project_root(cls) -> Path:
        return Path(__file__).parent.parent.parent

    @classmethod
    def get_logger_config(cls):
        external_work_dir = cls.get_project_root()
        cnf = Config("config.ini", external_work_dir)
        log = cnf.configuration.__getitem__('Log')
        log_name = f"{log.get('file').split('.log')[0]}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.log"
        logger = ProgramLogger(log.get('logger-name'),
                               os.path.join(external_work_dir, "logs", log_name),
                               '%(asctime)s %(levelname)s %(name)s %(message)s',
                               log.get('level'))
        return logger, cnf
