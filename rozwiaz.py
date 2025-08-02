from PIL import Image
import numpy as np
from collections import deque

# 1. Wczytaj obraz
input_path = "labirynt.png"  # nazwa pliku labiryntu
img = Image.open(input_path).convert("L")
arr = np.array(img)

# 2. Binarizacja (białe = True = ścieżka)
binary = arr > 128

# 3. Znajdź punkty wejścia i wyjścia (na krawędziach)
rows, cols = binary.shape
border_points = []

# górna krawędź
for x in range(cols):
    if binary[0, x]:
        border_points.append((0, x))
# dolna krawędź
for x in range(cols):
    if binary[rows - 1, x]:
        border_points.append((rows - 1, x))
# lewa krawędź
for y in range(rows):
    if binary[y, 0]:
        border_points.append((y, 0))
# prawa krawędź
for y in range(rows):
    if binary[y, cols - 1]:
        border_points.append((y, cols - 1))

if len(border_points) < 2:
    raise ValueError("Something went wrong.")

start = border_points[0]
end = border_points[-1]
print(f"Start: {start}, Koniec: {end}")

# 4. BFS - znajdowanie ścieżki
def bfs_path(maze, start, end):
    rows, cols = maze.shape
    visited = np.zeros_like(maze, dtype=bool)
    parent = {}
    q = deque([start])
    visited[start] = True

    while q:
        r, c = q.popleft()
        if (r, c) == end:
            break
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] and not visited[nr, nc]:
                visited[nr, nc] = True
                parent[(nr, nc)] = (r, c)
                q.append((nr, nc))

    # Odtworzenie ścieżki
    path = []
    node = end
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []  # brak ścieżki
    path.append(start)
    path.reverse()
    return path

path = bfs_path(binary, start, end)
if not path:
    raise RuntimeError("Nie udało się znaleźć ścieżki!")

# 5. Rysowanie ścieżki
solved = np.dstack([arr]*3)
for r, c in path:
    solved[r, c] = [255, 0, 0]  # czerwony

out_img = Image.fromarray(solved.astype(np.uint8))
out_img.save("labirynt_rozwiazany.png")
print("Zapisano wynik w labirynt_rozwiazany.png")