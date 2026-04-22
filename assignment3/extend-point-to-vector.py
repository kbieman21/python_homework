import math

# Task 5: Extending a Class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # equality check
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    # String representation for Point
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    
    # Euclidean distance: sqrt((x2-x1)^2 + (y2-y1)^2)
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Vector(Point):
    # overriding string representation for Vector
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    # override the + operator
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented


# Demonstrate results
if __name__ == "__main__":
    p1 = Point(3, 4)
    p2 = Point(0, 0)
    print(f"Point 1: {p1}")
    print(f"Distance from p1 to origin: {p1.distance(p2)}")
    print(f"Are points equal? {p1 == Point(3, 4)}")

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    v3 = v1 + v2
    print(f"\nVector 1: {v1}")
    print(f"Vector 2: {v2}")
    print(f"Vector Addition (v1 + v2): {v3}")
    print(f"Is v3 a Vector? {isinstance(v3, Vector)}")  