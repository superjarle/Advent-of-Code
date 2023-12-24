import numpy as np
from sympy import Symbol, solve_poly_system

class Christmas:
    def __init__(self, filename, test_area):
        self.filename = filename
        self.test_area = test_area
        self.hailstones = self.read_hailstone_data()

    def read_hailstone_data(self):
        with open(self.filename, 'r') as file:
            lines = [line.strip().split('@') for line in file.readlines()]
            hailstones = [tuple(map(int, pos.split(','))) + tuple(map(int, vector.split(','))) for pos, vector in lines]
        return hailstones

    @staticmethod
    def perp(a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b

    @staticmethod
    def seg_intersect(a1, a2, b1, b2):
        da = a2 - a1
        db = b2 - b1
        dp = a1 - b1
        dap = Christmas.perp(da)
        denom = np.dot(dap, db)
        num = np.dot(dap, dp)
        return (num / denom.astype(float)) * db + b1

    def calculate_intersections(self):
        counter = 0
        for i in range(len(self.hailstones) - 1):
            ax, ay, az, adx, ady, adz = self.hailstones[i]
            for j in range(i + 1, len(self.hailstones)):
                bx, by, bz, bdx, bdy, bdz = self.hailstones[j]
                pa = np.array([ax, ay])
                pb = np.array([ax + adx, ay + ady])
                pc = np.array([bx, by])
                pd = np.array([bx + bdx, by + bdy])

                res = Christmas.seg_intersect(pa, pb, pc, pd)
                if self.test_area[0] <= res[0] <= self.test_area[1] and self.test_area[0] <= res[1] <= self.test_area[1]:
                    counter += 1
        return counter

    def solve_poly_system(self):
        x, y, z = Symbol("x"), Symbol("y"), Symbol("z")
        dx, dy, dz = Symbol("dx"), Symbol("dy"), Symbol("dz")
        t1, t2, t3 = Symbol("t1"), Symbol("t2"), Symbol("t3")

        equations = []
        for i, hailstone in enumerate(self.hailstones[:3]):
            px, py, pz, vdx, vdy, vdz = hailstone
            t = [t1, t2, t3][i]
            equations.extend([x + dx * t - px - vdx * t, y + dy * t - py - vdy * t, z + dz * t - pz - vdz * t])

        res = solve_poly_system(equations, [x, y, z, dx, dy, dz, t1, t2, t3])
        return res

#solving 
christmas = Christmas("24.txt", (200000000000000, 400000000000000))
print("Number of intersections:", christmas.calculate_intersections())
solution = christmas.solve_poly_system()
if solution:
    #print("Solution for polynomial system:", solution[0])
    print("Sum of coordinates:", sum(solution[0][:3]))
else:
    print("No solution found for the polynomial system")