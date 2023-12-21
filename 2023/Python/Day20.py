from collections import deque
from math import lcm

def process_flip_flop(ff_name, flip_flop, pulse_type, pulses_queue):
    """Processes the pulse for a flip-flop module."""
    if pulse_type == 'LOW':
        new_pulse_type = 'HIGH' if flip_flop['is_active'] else 'LOW'
        flip_flop['is_active'] = not flip_flop['is_active']

        for output in flip_flop['outputs']:
            pulses_queue.append((new_pulse_type, ff_name, output))

def process_conjunction(conjunction_name, conjunction, source_name, pulse_type, pulses_queue):
    """Processes the pulse for a conjunction module."""
    conjunction['last_inputs'][source_name] = pulse_type
    new_pulse_type = 'LOW' if all(value == 'HIGH' for value in conjunction['last_inputs'].values()) else 'HIGH'

    for output in conjunction['outputs']:
        pulses_queue.append((new_pulse_type, conjunction_name, output))

def simulate_network(input_data, num_runs=1000):
    """Simulates the network for a given number of runs and calculates highs and lows."""
    broadcaster_outputs, flip_flops, conjunctions = prepare_modules(input_data)

    highs, lows = 0, 1000  # Count button pushes as "LOW"
    for _ in range(num_runs):
        pulses_queue = deque([('LOW', 'broadcaster', output) for output in broadcaster_outputs])
        while pulses_queue:
            pulse_type, source, target = pulses_queue.popleft()
            highs += (pulse_type == 'HIGH')
            lows += (pulse_type == 'LOW')

            if target in flip_flops:
                process_flip_flop(target, flip_flops[target], pulse_type, pulses_queue)
            elif target in conjunctions:
                process_conjunction(target, conjunctions[target], source, pulse_type, pulses_queue)

    print(f'Highs: {highs}, Lows: {lows}, Answer 1: {highs * lows}')

def prepare_modules(input_data):
    """Prepares the flip-flops and conjunction modules from the input data."""
    broadcaster_outputs, flip_flops, conjunctions = [], {}, {}

    for line in input_data.splitlines():
        node, outputs = line.split(' -> ')
        output_list = outputs.split(', ')

        if node == 'broadcaster':
            broadcaster_outputs = output_list
        elif node.startswith('%'):
            flip_flops[node[1:]] = {'is_active': False, 'outputs': output_list}
        elif node.startswith('&'):
            conjunctions[node[1:]] = {'last_inputs': {}, 'outputs': output_list}

    for ff_name, ff in flip_flops.items():
        for output in ff['outputs']:
            if output in conjunctions:
                conjunctions[output]['last_inputs'][ff_name] = 'LOW'

    return broadcaster_outputs, flip_flops, conjunctions

def find_cycle_length(input_data, target_module):
    """Finds the cycle length for a specific module."""
    broadcaster_outputs, flip_flops, conjunctions = prepare_modules(input_data)

    runs = 0
    while True:
        runs += 1
        pulses_queue = deque([('LOW', 'broadcaster', output) for output in broadcaster_outputs])
        while pulses_queue:
            pulse_type, source, target = pulses_queue.popleft()
            if source == target_module and pulse_type == 'HIGH':
                return runs

            if target in flip_flops:
                process_flip_flop(target, flip_flops[target], pulse_type, pulses_queue)
            elif target in conjunctions:
                process_conjunction(target, conjunctions[target], source, pulse_type, pulses_queue)

def calculate_lcm_of_cycles(input_data):
    """Calculates the least common multiple of the cycle lengths for specified modules."""
    cycle_lengths = [find_cycle_length(input_data, module) for module in ['ct', 'kp', 'ks', 'xc']]
    print(f'Answer 2: {lcm(*cycle_lengths)}')

# Main execution
input_data = open('20.txt').read().strip()

simulate_network(input_data)
calculate_lcm_of_cycles(input_data)
