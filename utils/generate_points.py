import numpy as np

def generate_reference_points(M: int, p: int) -> np.ndarray:
    def generate_recursive(
        points: list[list[float]],
        num_objs: int,
        left: int,
        total: int,
        depth: int,
        current_point: list[float]
    ) -> None:
        if depth == num_objs - 1:
            current_point.append(left / total)
            points.append(current_point.copy())
            current_point.pop()
        else:
            for i in range(left + 1):
                current_point.append(i / total)
                generate_recursive(points, num_objs, left - i, total, depth + 1, current_point)
                current_point.pop()

    points: list[list[float]] = []
    generate_recursive(points, M, p, p, 0, [])
    return np.array(points, dtype=float)