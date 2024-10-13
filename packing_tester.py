from visualize_gates import draw_gate_packing, visualize_gates
import random
import time
import matplotlib.pyplot as plt

class GatePacking:
    def __init__(self, gates, strategy):
        if strategy == 1:
            self.gates = sorted(gates, key=lambda g: g[1]+g[2]+g[1]*g[2], reverse=True)
        elif strategy == 2:
            self.gates = sorted(gates, key=lambda g: g[1]+g[2], reverse=True)
        else:
            self.gates = sorted(gates, key=lambda g: max(g[1],g[2]), reverse=True)
        self.placements = []
        self.occupied_positions = []
        self.candidate_points = [(0, 0)]  # Start with the origin as the first candidate
        self.bounding_box_width = gates[0][1]
        self.bounding_box_height = gates[0][2]

    def pack_gates(self):
        for gate in self.gates:
            name, width, height = gate
            position = self.find_position(width, height)
            if position is None:
                return False  # If no valid position found within the height, packing fails
            self.placements.append((name, position[0], position[1], width, height))
            self.occupied_positions.append((position[0], position[1], width, height))
            self.update_candidate_points(position[0], position[1], width, height)
            self.bounding_box_height = max(self.bounding_box_height, position[1]+height)
            self.bounding_box_width = max(self.bounding_box_width, position[0]+width)
        return True

    def find_position(self, width, height):
        valid_candidates = []
        valid_candidates2=[]
        for i in range(len(self.candidate_points)):
            x,y=self.candidate_points[i]
            if self.can_place_gate(x, y, width, height):
                if y + height <= self.bounding_box_height and x+width <=self.bounding_box_width: 
                    valid_candidates.append((i, x, y))
                else:
                    valid_candidates2.append((i,x,y))
        
        if len(valid_candidates)>0:
            # Choose the left-most and then the bottom-most valid candidate
            best_candidate = min(valid_candidates, key=lambda pos: (pos[1], pos[2]))
            self.candidate_points.pop(best_candidate[0])
            return (best_candidate[1], best_candidate[2])
        
        elif len(valid_candidates2)>0:
            best_candidate = min(valid_candidates2, key=lambda pos: max(pos[1]+width, self.bounding_box_width)*max(pos[2]+height, self.bounding_box_height))
            self.candidate_points.pop(best_candidate[0])
            return (best_candidate[1], best_candidate[2])

        return None

    def update_candidate_points(self, x, y, width, height):
        # Add top-left and bottom-right corners of the newly placed gate as candidate points
        top_left = (x, y + height)
        bottom_right = (x + width, y)
        self.candidate_points.append(top_left)
        self.candidate_points.append(bottom_right)

    def can_place_gate(self, x, y, width, height):
        for ox, oy, ow, oh in self.occupied_positions:
            if not (x + width <= ox or x >= ox + ow or y + height <= oy or y >= oy + oh):
                return False
        return True

    def write_output(self, output_file):
        bounding_width = self.bounding_box_width
        bounding_height = self.bounding_box_height
        with open(output_file, 'w') as f:
            f.write(f"bounding_box {bounding_width} {bounding_height}\n")
            for placement in self.placements:
                name, x, y, width, height = placement
                f.write(f"{name} {x} {y}\n")

    def calculate_packing_efficiency(self):
        bounding_width = self.bounding_box_width
        bounding_height = self.bounding_box_height
        bounding_area = bounding_width * bounding_height
        total_area = sum([w * h for _, _, w, h in self.occupied_positions])
        return total_area / bounding_area if bounding_area > 0 else 0

def read_input(input_file):
    gates = []
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.split()
            name = parts[0]
            width = int(parts[1])
            height = int(parts[2])
            gates.append((name, width, height))
    return gates
    

def solver(gates, strategy):
    packer = GatePacking(gates, strategy)
    success = packer.pack_gates()
    return packer if success else None



def main(input_file, output_file, visualizer=False):
    gates = read_input(input_file)
    
    packer = solver(gates, 1)
    # packer2 = solver(gates, 2)
    # packer3 = solver(gates, 3)
    # if packer2.calculate_packing_efficiency()>packer.calculate_packing_efficiency():
    #     packer = packer2
    # if packer3.calculate_packing_efficiency()>packer.calculate_packing_efficiency():
    #     packer = packer3
    # packer.write_output(output_file)
    
    if visualizer:
        visualize_gates(output_file, input_file, (300,300))
    
    return packer.calculate_packing_efficiency()

def testcase_generate(input_file, m, n):
    with open(input_file, 'w') as file:
        for i in range(1, n + 1):
            file.write(f"g{i} {random.randint(1, m)} {random.randint(1, m)}\n")

def tester(rand_input_file, input_file, output_file, m, n):
    testcase_generate(rand_input_file, m, n)
    input_file = rand_input_file
    return main(input_file, output_file, visualizer=False)

def plot_efficiency_vs_n():
    input_file = "input.txt"
    output_file = "output.txt"
    rand_input_file = "rand_input.txt"
    
    m = 100  # Maximum width/height of a gate
    t = 1  # Number of trials for each n to average out the results
    
    n_values = [i for i in range(100,1100, 100)]  # Different values of n (number of gates)
    efficiencies = []
    average_times = []

    for n in n_values:
        sum_efficiencies = 0
        total_time = 0
        
        for i in range(t):
            start = time.perf_counter()
            efficiency = tester(rand_input_file, input_file, output_file, m, n)
            end = time.perf_counter()
            
            sum_efficiencies += efficiency
            total_time += (end - start)
        
        average_efficiency = sum_efficiencies / t
        average_time = total_time / t
        
        efficiencies.append(average_efficiency * 100)  # Convert to percentage
        average_times.append(average_time)
    
    # Generate theoretical O(n^2) and O(n^3) curves
    n_squared = [n**2 for n in n_values]
    n_cubed = [n**3 for n in n_values]
    
    # Normalize the curves to match the scale of the average times
    max_time = max(average_times)
    max_n_squared = max(n_squared)
    max_n_cubed = max(n_cubed)
    
    normalized_n_squared = [(max_time / max_n_squared) * value for value in n_squared]
    normalized_n_cubed = [(max_time / max_n_cubed) * value for value in n_cubed]

    # Plotting
    plt.figure(figsize=(12, 6))
    
    # Plot packing efficiency
    # plt.subplot(1, 2, 1)
    # plt.plot(n_values, efficiencies, marker='o', color='b')
    # plt.xlabel('Number of Rectangles (n)')
    # plt.ylabel('Packing Efficiency (%)')
    # plt.title('Packing Efficiency vs. Number of Rectangles')
    # plt.grid(True)
    
    # Plot average time taken
    plt.plot(n_values, average_times, marker='o', color='r')
    plt.plot(n_values, normalized_n_squared, '--', color='g', label='O(n^2)')
    plt.plot(n_values, normalized_n_cubed, '--', color='b', label='O(n^3)')
    plt.xlabel('Number of Rectangles (n)')
    plt.ylabel('Average Time Taken (seconds)')
    plt.title('Average Time vs. Number of Rectangles')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    plt.savefig('aadi_lown.png')

if __name__ == "__main__":
    plot_efficiency_vs_n()