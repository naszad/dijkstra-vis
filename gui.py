import tkinter as tk
from tkinter import filedialog
import heapq
import math

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
        adj[iu].append((iv,w)); adj[iv].append((iu,w))
    src = next(it); s = idx[src]
    dist = [float('inf')]*N; prev = [-1]*N; dist[s] = 0
    heap = [(0,s)]
    while heap:
        d,u = heapq.heappop(heap)
        if d>dist[u]: continue
        for v,w in adj[u]:
            alt = d+w
            if alt<dist[v]: dist[v]=alt; prev[v]=u; heapq.heappush(heap,(alt,v))
    out = ''
    for i,n in enumerate(names):
        out += f'Path to {n} (cost {dist[i]}): '
        path = []
        j = i
        while j!=-1: path.append(names[j]); j = prev[j]
        out += ' '.join(reversed(path)) + '\n'
    text.delete('1.0', tk.END); text.insert(tk.END, out)
    canvas.delete("all")
    width = int(canvas['width']); height = int(canvas['height'])
    center_x = width/2; center_y = height/2
    radius = min(width, height)/2 - 50
    pos = []
    for i in range(N):
        angle = 2*math.pi*i/N
        x = center_x + radius*math.cos(angle)
        y = center_y + radius*math.sin(angle)
        pos.append((x,y))
    drawn = set()
    for i in range(N):
        for v,w in adj[i]:
            if (v,i) in drawn: continue
            x1,y1 = pos[i]; x2,y2 = pos[v]
            canvas.create_line(x1,y1,x2,y2)
            mid_x,mid_y = (x1+x2)/2, (y1+y2)/2
            canvas.create_text(mid_x, mid_y, text=str(w))
            drawn.add((i,v))
    for i,name in enumerate(names):
        x,y = pos[i]
        r = 15
        canvas.create_oval(x-r, y-r, x+r, y+r, fill='lightblue')
        canvas.create_text(x, y, text=name)

root = tk.Tk(); root.title('Dijkstra GUI')
btn = tk.Button(root, text='Load & Run', command=load_file); btn.pack()
text = tk.Text(root, width=60, height=20); text.pack()
canvas = tk.Canvas(root, width=600, height=600, bg='white')
canvas.pack()
root.mainloop() 