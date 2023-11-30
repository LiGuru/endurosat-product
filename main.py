from infrastructure.commons.project_definitions import ProjectDefinition
from infrastructure.commons.transform_data import DictToObj

if __name__ == "__main__":
    sys_logger, cfg = ProjectDefinition.get_logger_config()
    port_conf = DictToObj(dict(cfg.configuration.items('Port.Config')))
