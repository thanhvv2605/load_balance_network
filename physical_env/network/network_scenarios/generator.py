import numpy as np
import matplotlib.pyplot as plt
import yaml

class ScenariosGenerator():
    def __init__(self, num_points, num_scenarios):
        # Số lượng điểm ngẫu nhiên
        self.num_points = num_points
        self.space_size = 1000
        self.num_scenarios= num_scenarios
        self.points = None
        self.data  = {
            'node_phy_spe': {
                'capacity': 10800,
                'com_range': 80,
                'efs': 1.0e-08,
                'emp': 1.3e-12,
                'er': 0.0001,
                'et': 5.0e-05,
                'package_size': 400.0,
                'prob_gp': 1,
                'sen_range': 40,
                'threshold': 540
            },
            'seed': 0,
            'max_time': 604800,
            'Rc': 80,
            'Rs': 40,
            'base_station': [500, 500],
            'xllcorner': 106.413219,
            'yllcorner': 21.260683,
            'nodes': [],
            'targets': []
}


    def uniform_distribute(self):
        self.points = np.random.uniform(0, self.space_size, (self.num_points, 2))
        self.data['targets'] = self.points.tolist()

    def draw(self):
        # Vẽ biểu đồ
        plt.figure(figsize=(8, 8))
        plt.scatter(self.points[:, 0], self.points[:, 1], alpha=0.6, label='Random Points')
        plt.title('Randomly Distributed Points in 2D Space')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid(True)
        plt.legend()
        plt.show()

    def gen_scenarios(self):
        for i in range(0, self.num_scenarios):
            self.uniform_distribute()
            self.draw()
            # Xuất dữ liệu sang tệp YAML
            file_path = str(self.num_points) + "_" + 'normal_' + str(i) + '.yaml'
            with open(file_path, 'w') as file:
                yaml.dump(self.data, file, default_flow_style=False, allow_unicode=True)

            
