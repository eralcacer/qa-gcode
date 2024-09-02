import math

def calculate_center(start_point, end_point, clockwise=True):
    center_x = (start_point[0] + end_point[0]) / 2.0
    center_y = (start_point[1] + end_point[1]) / 2.0

    if clockwise:
        radius = -math.sqrt((start_point[0] - center_x)**2 + (start_point[1] - center_y)**2)
    else:
        radius = math.sqrt((start_point[0] - center_x)**2 + (start_point[1] - center_y)**2)

    return center_x, center_y, radius


def generate_arc_points(start_point, end_point, center_point=None, clockwise=True, radius=None, angle_increment=5):
    if radius is None:
        if center_point is None:
            center_x, center_y, radius = calculate_center(start_point, end_point, clockwise)
        else:
            center_x, center_y = center_point
            radius = math.sqrt((start_point[0] - center_x) ** 2 + (start_point[1] - center_y) ** 2)
    else:
        if center_point is None:
            center_x, center_y, _ = calculate_center(start_point, end_point, clockwise)
        else:
            center_x, center_y = center_point

    start_angle = math.atan2(start_point[1] - center_y, start_point[0] - center_x)
    end_angle = math.atan2(end_point[1] - center_y, end_point[0] - center_x)
    # Handle the case where the arc forms a full circle
    if abs(end_angle - start_angle) in {0, 2 * math.pi}:
        end_angle += 2 * math.pi
    # Calculate angle increment in radians
    angle_increment_rad = math.radians(angle_increment)

    # Generate arc points
    points = []
    num_points = int(abs(end_angle - start_angle) / angle_increment_rad)
    for _ in range(num_points):
        x = center_x + radius * math.cos(start_angle)
        y = center_y + radius * math.sin(start_angle)
        points.append([x, y])
        start_angle += angle_increment_rad
    if radius < 0:
        points = points[::-1]
    return points
