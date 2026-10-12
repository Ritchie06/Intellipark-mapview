import cv2
import numpy as np
import heapq
import requests
import qrcode
import time
import os
import base64

# --- CONFIGURATION ---
IMAGE_PATH = "grnddd2.png" 
IMGBB_API_KEY = "67693f596e7ccb92655784bc35156ab6" 

def load_background():
    img = cv2.imread(IMAGE_PATH)
    return img if img is not None else np.zeros((800, 600, 3), dtype=np.uint8)

def create_parking_grid(rows=20, cols=22):
    grid = np.ones((rows, cols), dtype=np.uint8)  
    grid[5, 2:20] = 0   
    grid[15, 2:20] = 0  
    grid[5:16, 5] = 0   
    for r in [6, 8, 10]: grid[r, 5:19] = 0 
    return grid

def generate_parking_slots():
    slots = []
    for r in [7, 9, 11]: 
        for c in range(7, 18, 2): slots.append((r, c))
    return slots

def astar(grid, start, goal):
    def heuristic(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    cost_so_far = {start: 0}
    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current); current = came_from[current]
            return path[::-1]
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] == 0:
                new_cost = cost_so_far[current] + 1
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    heapq.heappush(open_set, (new_cost + heuristic((nx, ny), goal), new_cost, (nx, ny)))
                    came_from[(nx, ny)] = current
    return None

def upload_to_cloud(image_path):
    print("Uploading shortest-path map to cloud...")
    try:
        with open(image_path, "rb") as file:
            payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.read())}
            res = requests.post("https://api.imgbb.com/1/upload", payload)
            if res.status_code == 200:
                return res.json()['data']['url']
    except Exception as e:
        print(f"Upload error: {e}")
    return None

def visualize_and_save(photo, grid, path, slots, selected, booked, filename):
    display_img = photo.copy()
    h, w, _ = display_img.shape
    sw, sh = w // grid.shape[1], h // grid.shape[0]
    if path:
        for i in range(len(path) - 1):
            pt1 = (path[i][1]*sw+sw//2, path[i][0]*sh+sh//2)
            pt2 = (path[i+1][1]*sw+sw//2, path[i+1][0]*sh+sh//2)
            cv2.line(display_img, pt1, pt2, (0, 255, 0), 10, cv2.LINE_AA)
    for idx, slot in enumerate(slots):
        r, c = slot
        if slot in booked:
            cv2.rectangle(display_img, (c*sw+5, r*sh+5), ((c+1)*sw-5, (r+1)*sh-5), (50, 50, 50), -1)
        else:
            color = (0, 165, 255) if slot == selected else (255, 255, 255)
            cv2.rectangle(display_img, (c*sw+5, r*sh+5), ((c+1)*sw-5, (r+1)*sh-5), color, 2)
    cv2.imwrite(filename, display_img)

# --- MAIN LOOP WITH SHORTEST PATH LOGIC ---
if __name__ == "__main__":
    bg = load_background()
    grid = create_parking_grid()
    START, SLOTS, BOOKED = (5, 2), generate_parking_slots(), []

    while True:
        available = [s for s in SLOTS if s not in BOOKED]
        if not available: 
            print("No slots available.")
            break

        # SHORTEST PATH SEARCH: Check every available slot
        best_path = None
        target_slot = None
        min_distance = float('inf')

        for slot in available:
            # The goal is the road cell directly above the slot
            path = astar(grid, START, (slot[0]-1, slot[1]))
            if path and len(path) < min_distance:
                min_distance = len(path)
                best_path = path
                target_slot = slot

        if target_slot:
            temp_map = "current_navigation.png"
            visualize_and_save(bg, grid, best_path, SLOTS, target_slot, BOOKED, temp_map)
            web_url = upload_to_cloud(temp_map)
            
            if web_url:
                qr = qrcode.make(web_url)
                qr.save("scan_me.png")
                cv2.imshow("SCAN FOR SHORTEST PATH", cv2.imread("scan_me.png"))
                print(f"Shortest path found! Slot: {target_slot} | URL: {web_url}")
                
                if cv2.waitKey(0) & 0xFF == ord('q'): break
                BOOKED.append(target_slot)
                cv2.destroyAllWindows()
            else:
                print("Cloud Upload Failed.")
                break
