from pyglet import resource

DATA_PATH = resource.get_data_path("")
LOGS_PATH = DATA_PATH / "logs" # TODO let main module keep track of the apps name and configure the resource module; fix flake8