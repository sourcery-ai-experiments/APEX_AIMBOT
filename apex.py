from AimBot import AimBot
import multiprocessing
import yaml

class ApexAimBot(AimBot):
    def __init__(self, config_path):
        # Load configuration
        config = self.load_config(config_path)
        onnx_path = config['onnx_path']
        engine_path = config['trt_path']
        super().__init__(config_path, onnx_path, engine_path)

    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    def initialize_params(self):
        super().initialize_params()
        self.smooth = self.args.smooth * 1280 / self.args.resolution_x # default settings by game


if __name__ == '__main__':
    multiprocessing.freeze_support()
    apex = ApexAimBot(config_path='configs/apex.yaml')
    while True:
        apex.forward()
