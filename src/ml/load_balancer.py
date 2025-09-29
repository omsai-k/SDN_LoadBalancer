
import os
import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class LoadBalancer:
    def __init__(self, controllers):
        self.controllers = controllers
        logger.info(f"LoadBalancer initialized with controllers: {controllers}")

    def get_controller_load(self, controller_url):
        try:
            headers = {"Authorization": f"Bearer {os.getenv('SECRET_KEY','')}"}
            response = requests.get(f"{controller_url}/get_load", headers=headers)
            load = response.json().get('load', float('inf'))
            logger.info(f"Controller {controller_url} load: {load}")
            return load
        except requests.exceptions.ConnectionError:
            logger.error(f"Could not connect to controller: {controller_url}")
            return float('inf')
        except Exception as e:
            logger.exception(f"Error getting controller load: {e}")
            return float('inf')

    def balance(self, flow):
        # Adaptive load balancing based on controller load
        try:
            loads = [self.get_controller_load(c) for c in self.controllers]
            best_controller = self.controllers[loads.index(min(loads))]
            logger.info(f"Flow {flow} assigned to controller {best_controller}")
            return best_controller
        except Exception as e:
            logger.exception(f"Error in load balancing: {e}")
            return None
