import tkinter as tk
from tkinter import filedialog
import heapq
import math

# Global state for animation
graph = {'N':0, 'adj':[], 'names':[], 'pos':[], 'node_items':[], 'edge_items':{}}
r = 15  # node radius
selected = []

def on_canvas_click(event):
    for i,(x,y) in enumerate(graph['pos']):
        if (event.x-x)**2 + (event.y-y)**2 <= r**2:
            if len(selected)==0:
                selected.append(i)
                canvas.itemconfig(graph['node_items'][i], fill='green')
            elif len(selected)==1:
                selected.append(i)
                canvas.itemconfig(graph['node_items'][i], fill='red')
                run_animation(selected[0], selected[1])
            break


def dijkstra_steps(s, t):
    N = graph['N']; adj = graph['adj']
    dist = [float('inf')]*N; prev = [-1]*N; visited = [False]*N
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if visited[u]: continue
        visited[u] = True
        yield ('visit', u)
        if u == t: break
        for v, w in adj[u]:
            yield ('consider', u, v)
            alt = d + w
            if alt < dist[v]:
                dist[v] = alt; prev[v] = u
                heapq.heappush(heap, (alt, v))
                yield ('relax', u, v)
    path = []
    j = t
    while j != -1:
        path.append(j); j = prev[j]
    path.reverse()
    yield ('done', path)


def run_animation(s, t):
    gen = dijkstra_steps(s, t)
    def step():
        try:
            ev = next(gen)
        except StopIteration:
            return
        typ = ev[0]
        if typ == 'visit':
            u = ev[1]; canvas.itemconfig(graph['node_items'][u], fill='yellow')
        elif typ == 'consider':
            u, v = ev[1], ev[2]
            edge = graph['edge_items'].get((u, v)) or graph['edge_items'].get((v, u))
            if edge: canvas.itemconfig(edge, fill='orange')
        elif typ == 'relax':
            u, v = ev[1], ev[2]
            edge = graph['edge_items'].get((u, v)) or graph['edge_items'].get((v, u))
            if edge: canvas.itemconfig(edge, fill='blue')
        elif typ == 'done':
            path = ev[1]
            for node in path:
                canvas.itemconfig(graph['node_items'][node], fill='green')
            for i in range(len(path)-1):
                a, b = path[i], path[i+1]
                edge = graph['edge_items'].get((a, b)) or graph['edge_items'].get((b, a))
                if edge: canvas.itemconfig(edge, fill='green')
            return
        delay = speed_var.get()
        root.after(delay, step)
    step()

def load_file():
    path = filedialog.askopenfilename(filetypes=[('Text Files','*.txt')])
    if not path: return
    with open(path) as f: data = f.read().split()
    it = iter(data)
    N = int(next(it)); M = int(next(it))
    names = [next(it) for _ in range(N)]
    idx = {n:i for i,n in enumerate(names)}
    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = next(it); v = next(it); w = int(next(it))
        iu, iv = idx[u], idx[v]
        adj[iu].append((iv, w)); adj[iv].append((iu, w))

    # Prompt for node selection and bind click handler
    text.delete('1.0', tk.END)
    text.insert(tk.END, 'Click on two nodes to choose source (green) and destination (red).')
    selected.clear()
    canvas.bind('<Button-1>', on_canvas_click)

    # Prepare and draw the static graph layout
    canvas.delete('all')
    width = int(canvas['width']); height = int(canvas['height'])
    center_x = width/2; center_y = height/2
    radius = min(width, height)/2 - 50
    pos = []
    for i in range(N):
        angle = 2*math.pi*i/N
        x = center_x + radius*math.cos(angle)
        y = center_y + radius*math.sin(angle)
        pos.append((x,y))

    # Store graph state for animation
    graph['N'] = N; graph['adj'] = adj; graph['names'] = names
    graph['pos'] = pos; graph['node_items'] = []; graph['edge_items'] = {}

    # Draw edges and record them
    drawn = set()
    for i in range(N):
        for v,w in adj[i]:
            if (v,i) in drawn: continue
            x1,y1 = pos[i]; x2,y2 = pos[v]
            e_id = canvas.create_line(x1,y1,x2,y2, fill='gray')
            mid_x,mid_y = (x1+x2)/2, (y1+y2)/2
            canvas.create_text(mid_x, mid_y, text=str(w))
            graph['edge_items'][(i,v)] = e_id
            drawn.add((i,v))

    # Draw nodes and record them
    for i,name in enumerate(names):
        x,y = pos[i]
        node_id = canvas.create_oval(x-r, y-r, x+r, y+r, fill='lightblue')
        canvas.create_text(x, y, text=name)
        graph['node_items'].append(node_id)

root = tk.Tk(); root.title('Dijkstra GUI')
btn = tk.Button(root, text='Load & Run', command=load_file); btn.pack()
text = tk.Text(root, width=60, height=20); text.pack()
canvas = tk.Canvas(root, width=600, height=600, bg='white')
canvas.pack()
# Animation speed control
speed_var = tk.IntVar(value=500)
speed_scale = tk.Scale(root, from_=100, to=2000, orient=tk.HORIZONTAL, label='Animation Speed (ms)', variable=speed_var)
speed_scale.pack()
root.mainloop() 