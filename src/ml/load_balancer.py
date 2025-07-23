import requests

class LoadBalancer:
    def __init__(self, controllers):
        self.controllers = controllers

    def get_controller_load(self, controller_url):
        try:
            response = requests.get(f"{controller_url}/get_load")
            return response.json().get('load', float('inf'))
        except requests.exceptions.ConnectionError:
            return float('inf')

    def balance(self, flow):
        # Adaptive load balancing based on controller load
        loads = [self.get_controller_load(c) for c in self.controllers]
        best_controller = self.controllers[loads.index(min(loads))]
        return best_controller
