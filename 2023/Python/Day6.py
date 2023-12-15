class Racing:
    def __init__(self, race_data):
        """
           Parsing race data for multiple and single races:
        - Time and distance from regular expressions.
        - Single race time and distance joining digits and converting to integers. 
        """
        times_str, distances_str = race_data
        self.times = list(map(int, re.findall(r'\d+', times_str)))
        self.distances = list(map(int, re.findall(r'\d+', distances_str)))
        self.single_race_time = int(''.join(re.findall(r'\d+', times_str)))
        self.single_race_distance = int(''.join(re.findall(r'\d+', distances_str)))

    def calculate_ways(self, time, record_distance):
        """
        Calculates the number of ways to beat the record for a given race.

        This method iterates to find all possible buttonhold times to get a distance greater than the record distance. 
        Distance holds a quadratic function between time, speed and remaining time.
        """
        ways_to_win = 0
        for hold_time in range(time):
            travel_time = time - hold_time
            distance = hold_time * travel_time
            if distance > record_distance:
                ways_to_win += 1
        return ways_to_win

    def calculate_multiple_races(self):
        """
        Returns how to win multiple races (q1)

        Calculating the number of winning strategies using calculate_ways, and multiply together to find total number
        of combinations to beat the records in all races.
        """
        multiple = 1
        for time, distance in zip(self.times, self.distances):
            ways = self.calculate_ways(time, distance)
            multiple *= ways
        return multiple

    def calculate_single_race(self):
        """
        Single long race (q2). Using the calculate_ways to calculate the many times during one whole one. 

        """
        return self.calculate_ways(self.single_race_time, self.single_race_distance)



#Solving the two puzzles
q1 = Racing.calculate_multiple_races()
q2 = Racing.calculate_single_race()

#Printing results 
print(q1, q2) 

