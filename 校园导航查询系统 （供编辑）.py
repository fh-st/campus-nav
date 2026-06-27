# ==========================================
# 什邡校区校园导航 V6.3 完整修复版
# 修复Tkinter参数错误 | 登录框支持显示密码 | 管理员权限管控道路编辑
# 无弹窗操作日志 | JSON持久化 | Dijkstra/BFS双路线算法
# ==========================================
import json
import os
import heapq
import tkinter as tk
from tkinter import ttk, scrolledtext

# 管理员配置
ADMIN_PWD = "admin123"
IS_ADMIN = False

# 持久化文件路径
PLACE_FILE = "places.json"
GRAPH_FILE = "graph_road.json"

# 校区点位（严格匹配实拍地图）
init_campus_places = [
    # 教学楼组团
    {"id": 1, "name": "弘义楼西", "location": "教学楼", "x": 110, "y": 305},
    {"id": 2, "name": "弘义楼", "location": "教学楼", "x": 210, "y": 305},
    {"id": 3, "name": "弘义楼东", "location": "教学楼", "x": 310, "y": 305},
    {"id": 4, "name": "明德楼", "location": "教学楼", "x": 110, "y": 365},
    {"id": 5, "name": "致远楼", "location": "教学楼", "x": 210, "y": 365},
    {"id": 6, "name": "明志楼", "location": "教学楼", "x": 310, "y": 365},
    {"id": 7, "name": "明理楼", "location": "教学楼", "x": 110, "y": 425},
    {"id": 8, "name": "明善楼", "location": "教学楼", "x": 310, "y": 425},
    {"id": 9, "name": "图书馆", "location": "图书阅览中心", "x": 210, "y": 495},
    # 中部生活服务区域
    {"id": 10, "name": "筑梦活动中心", "location": "生活服务", "x": 435, "y": 305},
    {"id": 11, "name": "旭日餐厅", "location": "食堂", "x": 495, "y": 305},
    {"id": 12, "name": "文印室", "location": "生活服务", "x": 395, "y": 262},
    {"id": 13, "name": "旭日超市", "location": "生活服务", "x": 465, "y": 262},
    {"id": 14, "name": "奶茶店水果店", "location": "生活服务", "x": 528, "y": 262},
    {"id": 15, "name": "水站", "location": "生活服务", "x": 582, "y": 262},
    # 公寓宿舍楼区
    {"id": 16, "name": "1A公寓楼", "location": "学生公寓", "x": 622, "y": 305},
    {"id": 17, "name": "1B公寓楼", "location": "学生公寓", "x": 622, "y": 345},
    {"id": 18, "name": "2A公寓楼", "location": "学生公寓", "x": 682, "y": 345},
    {"id": 19, "name": "2B公寓楼", "location": "学生公寓", "x": 682, "y": 385},
    {"id": 20, "name": "3A公寓楼", "location": "学生公寓", "x": 762, "y": 345},
    {"id": 21, "name": "3B公寓楼", "location": "学生公寓", "x": 762, "y": 385},
    # 公寓配套商铺
    {"id": 22, "name": "理发店", "location": "生活服务", "x": 650, "y": 262},
    {"id": 23, "name": "菜鸟驿站(1A/1B公寓)", "location": "生活服务", "x": 692, "y": 262},
    {"id": 24, "name": "菜鸟驿站(3A/3B公寓)", "location": "生活服务", "x": 780, "y": 262},
    # 运动场地
    {"id": 25, "name": "体育场", "location": "运动场地", "x": 562, "y": 445},
    {"id": 26, "name": "看台", "location": "体育场附属", "x": 622, "y": 445},
    # 校门与配套设施
    {"id": 27, "name": "正大门", "location": "校门入口", "x": 362, "y": 222},
    {"id": 28, "name": "开闭站", "location": "电力配套", "x": 462, "y": 232},
    {"id": 29, "name": "水泵房", "location": "后勤设施", "x": 282, "y": 262},
    {"id": 30, "name": "北二门", "location": "校门入口", "x": 722, "y": 232},
    {"id": 31, "name": "迎新商业服务点", "location": "商业服务", "x": 652, "y": 372},
]
campus_places = []

# ---------------------- 持久化读写工具 ----------------------
def save_places():
    with open(PLACE_FILE, "w", encoding="utf-8") as f:
        json.dump(campus_places, f, ensure_ascii=False, indent=2)

def load_places():
    global campus_places
    try:
        if os.path.exists(PLACE_FILE):
            with open(PLACE_FILE, "r", encoding="utf-8") as f:
                campus_places = json.load(f)
        else:
            campus_places = init_campus_places.copy()
            save_places()
    except Exception:
        campus_places = init_campus_places.copy()
        save_places()

def save_graph(adj_data):
    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(adj_data, f, ensure_ascii=False, indent=2)

def load_graph():
    try:
        if os.path.exists(GRAPH_FILE):
            with open(GRAPH_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                adj = {}
                for k, v in raw.items():
                    adj[int(k)] = [(int(x[0]), x[1]) for x in v]
                return adj
    except Exception:
        pass
    adj = {p["id"]: [] for p in campus_places}
    return adj

def reset_all_data():
    global campus_places
    campus_places = init_campus_places.copy()
    save_places()
    new_adj = {p["id"]: [] for p in campus_places}
    save_graph(new_adj)

# ---------------------- 带权无向图（防KeyError崩溃） ----------------------
class CampusGraph:
    def __init__(self):
        self.adj = load_graph()

    def save(self):
        save_graph(self.adj)

    def add_road(self, id1, id2, distance):
        if id1 not in self.adj or id2 not in self.adj:
            return False
        for v, d in self.adj[id1]:
            if v == id2:
                return False
        self.adj[id1].append((id2, distance))
        self.adj[id2].append((id1, distance))
        self.save()
        return True

    def del_road(self, id1, id2):
        flag = False
        lst1 = self.adj.get(id1, [])
        lst2 = self.adj.get(id2, [])
        for item in lst1:
            if item[0] == id2:
                lst1.remove(item)
                flag = True
                break
        for item in lst2:
            if item[0] == id1:
                lst2.remove(item)
                break
        if flag:
            self.adj[id1] = lst1
            self.adj[id2] = lst2
            self.save()
        return flag

    def bfs_short_node_path(self, start_id, end_id):
        if start_id == end_id:
            return [start_id], 0
        if start_id not in self.adj or end_id not in self.adj:
            return None, -1
        visited = set([start_id])
        queue = [[start_id]]
        while queue:
            path = queue.pop(0)
            cur = path[-1]
            for neighbor, _ in self.adj.get(cur, []):
                if neighbor not in visited:
                    new_path = path.copy()
                    new_path.append(neighbor)
                    if neighbor == end_id:
                        return new_path, len(new_path)-1
                    visited.add(neighbor)
                    queue.append(new_path)
        return None, -1

    def dijkstra_min_dist_path(self, start_id, end_id):
        if start_id not in self.adj or end_id not in self.adj:
            return None, -1
        dist = {pid: float("inf") for pid in self.adj}
        prev = {pid: None for pid in self.adj}
        dist[start_id] = 0
        heap = []
        heapq.heappush(heap, (0, start_id))
        visited = set()
        while heap:
            cur_dist, cur = heapq.heappop(heap)
            if cur in visited:
                continue
            if cur == end_id:
                break
            visited.add(cur)
            for nxt, w in self.adj.get(cur, []):
                if dist[nxt] > cur_dist + w:
                    dist[nxt] = cur_dist + w
                    prev[nxt] = cur
                    heapq.heappush(heap, (dist[nxt], nxt))
        if dist[end_id] == float("inf"):
            return None, -1
        path = []
        cur = end_id
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path, dist[end_id]

graph = CampusGraph()

# ---------------------- KMP / BM 字符串模糊检索 ----------------------
def get_next(pattern):
    nxt = [0]*len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j-1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j
    return nxt

def kmp(text, pattern):
    if not pattern:
        return True
    nxt = get_next(pattern)
    j = 0
    for c in text:
        while j > 0 and c != pattern[j]:
            j = nxt[j-1]
        if c == pattern[j]:
            j += 1
        if j == len(pattern):
            return True
    return False

def build_bad(pattern):
    bad = {}
    for idx, c in enumerate(pattern):
        bad[c] = idx
    return bad

def bm(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return True
    bad = build_bad(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s+j]:
            j -= 1
        if j < 0:
            return True
        s += max(1, j - bad.get(text[s+j], -1))
    return False

# ---------------------- BST二叉搜索树模块 ----------------------
class TreeNode:
    def __init__(self, place):
        self.place = place
        self.left = self.right = None

def insert_bst(root, place):
    if not root:
        return TreeNode(place)
    if place["id"] < root.place["id"]:
        root.left = insert_bst(root.left, place)
    else:
        root.right = insert_bst(root.right, place)
    return root

def build_bst():
    root = None
    for p in campus_places:
        root = insert_bst(root, p)
    return root

def bst_search(root, target):
    if not root:
        return None
    if target == root.place["id"]:
        return root.place
    elif target < root.place["id"]:
        return bst_search(root.left, target)
    else:
        return bst_search(root.right, target)

# ---------------------- 通用工具函数 ----------------------
def get_id_by_name(name_key):
    res = []
    for p in campus_places:
        if kmp(p["name"], name_key):
            res.append(p)
    if len(res) == 0:
        return None
    elif len(res) == 1:
        return res[0]["id"]
    else:
        return res

def get_pos_by_id(pid):
    for p in campus_places:
        if p["id"] == pid:
            return (p["x"], p["y"], p["name"])
    return None

def get_name_by_id(pid):
    for p in campus_places:
        if p["id"] == pid:
            return p["name"]
    return "未知地点"

# ---------------------- GUI主界面类 ----------------------
class NavGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("什邡校区校园导航系统 V6.3 权限完整版")
        self.root.geometry("1150x720")
        self.path_highlight = []
        self.init_ui()
        self.refresh_map()

    def init_ui(self):
        # 左侧地图画布
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        self.canvas = tk.Canvas(self.left_frame, bg="#e8f3e8")
        self.canvas.pack(fill="both", expand=True)
        # 右侧控制面板
        self.right_frame = tk.Frame(self.root, width=320)
        self.right_frame.pack(side="right", fill="y", padx=6, pady=6)

        # 管理员登录按钮
        ttk.Button(self.right_frame, text="管理员登录", command=self.admin_login).pack(fill="x", pady=2)

        # 路线导航区域（所有用户可用）
        ttk.Label(self.right_frame, text="路线导航查询", font=("黑体", 14, "bold")).pack(pady=4)
        tk.Label(self.right_frame, text="起点地点名称：").pack(anchor="w")
        self.start_entry = ttk.Entry(self.right_frame, font=("微软雅黑", 10))
        self.start_entry.pack(fill="x", pady=2)
        tk.Label(self.right_frame, text="终点地点名称：").pack(anchor="w")
        self.end_entry = ttk.Entry(self.right_frame, font=("微软雅黑", 10))
        self.end_entry.pack(fill="x", pady=2)

        btn_frame = tk.Frame(self.right_frame)
        btn_frame.pack(pady=6, fill="x")
        ttk.Button(btn_frame, text="最少中转路线", command=self.calc_bfs).grid(row=0, column=0, padx=3)
        ttk.Button(btn_frame, text="最短距离路线", command=self.calc_dijk).grid(row=0, column=1, padx=3)
        ttk.Button(self.right_frame, text="清除路线高亮", command=self.clear_highlight).pack(fill="x", pady=3)

        # 操作日志文本框
        ttk.Label(self.right_frame, text="操作日志 & 分段导航指引：").pack(anchor="w", pady=2)
        self.text_box = scrolledtext.ScrolledText(self.right_frame, height=14, font=("微软雅黑", 9))
        self.text_box.pack(fill="both", expand=True)

        # 管理员道路管理区域
        ttk.Separator(self.right_frame).pack(fill="x", pady=10)
        ttk.Label(self.right_frame, text="【管理员专用】道路路网管理", font=("黑体", 12, "bold")).pack()
        road_f = tk.Frame(self.right_frame)
        road_f.pack(fill="x", pady=3)
        tk.Label(road_f, text="起点ID:").grid(row=0, column=0)
        self.rid1 = ttk.Entry(road_f, width=6)
        self.rid1.grid(row=0, column=1)
        tk.Label(road_f, text="终点ID:").grid(row=0, column=2)
        self.rid2 = ttk.Entry(road_f, width=6)
        self.rid2.grid(row=0, column=3)

        tk.Label(self.right_frame, text="道路步行距离(米)：").pack(anchor="w")
        self.dis_entry = ttk.Entry(self.right_frame)
        self.dis_entry.pack(fill="x", pady=2)

        btn_r = tk.Frame(self.right_frame)
        btn_r.pack(fill="x", pady=4)
        self.btn_add = ttk.Button(btn_r, text="新建连通道路", command=self.add_road_gui)
        self.btn_add.grid(row=0, column=0, padx=3)
        self.btn_del = ttk.Button(btn_r, text="删除现有道路", command=self.del_road_gui)
        self.btn_del.grid(row=0, column=1, padx=3)

        # 重置地图按钮
        ttk.Separator(self.right_frame).pack(fill="x", pady=10)
        self.btn_reset = ttk.Button(self.right_frame, text="一键重置校区原始地图数据", command=self.reset_data)
        self.btn_reset.pack(fill="x", pady=4)

    # 日志统一输出函数
    def log_print(self, msg):
        self.text_box.insert(tk.END, msg + "\n")
        self.text_box.see(tk.END)

    # 管理员登录弹窗（修复参数错误+显示密码勾选框）
    def admin_login(self):
        global IS_ADMIN
        login_win = tk.Toplevel(self.root)
        login_win.title("管理员登录")
        login_win.geometry("280x180")
        login_win.transient(self.root)
        login_win.grab_set()

        ttk.Label(login_win, text="请输入管理员密码", font=("黑体",11)).pack(pady=12)
        pwd_var = tk.StringVar()
        pwd_entry = ttk.Entry(login_win, textvariable=pwd_var, show="*")
        # 修复：标准pack参数 padx 替代错误的pad
        pwd_entry.pack(pady=4, fill="x", padx=30)

        # 显示密码勾选框
        show_pwd = tk.BooleanVar()
        def toggle_pwd():
            if show_pwd.get():
                pwd_entry.config(show="")
            else:
                pwd_entry.config(show="*")
        ttk.Checkbutton(login_win, text="显示密码", variable=show_pwd, command=toggle_pwd).pack()

        def check_login():
            global IS_ADMIN
            if pwd_var.get() == ADMIN_PWD:
                IS_ADMIN = True
                self.log_print("✅ 管理员登录成功，已解锁道路编辑权限")
                login_win.destroy()
            else:
                self.log_print("❌ 密码错误，未获得管理员权限，无法编辑道路")

        ttk.Button(login_win, text="确认登录", command=check_login).pack(pady=10)
        self.root.wait_window(login_win)

    def refresh_map(self):
        self.canvas.delete("all")
        self.path_highlight.clear()
        # 绘制所有道路
        for u, link_list in graph.adj.items():
            pos_u = get_pos_by_id(u)
            if not pos_u:
                continue
            x1, y1, _ = pos_u
            for v, d in link_list:
                pos_v = get_pos_by_id(v)
                if not pos_v:
                    continue
                x2, y2, _ = pos_v
                self.canvas.create_line(x1, y1, x2, y2, fill="#777777", dash=(5, 3), tags="road")
        # 绘制点位与名称
        for p in campus_places:
            x, y, name = p["x"], p["y"], p["name"]
            self.canvas.create_oval(x-11, y-11, x+11, y+11, fill="#3b82f6", tags="point")
            self.canvas.create_text(x, y+20, text=name, font=("微软雅黑", 8))

    def clear_highlight(self):
        self.refresh_map()
        self.log_print("已清除路线高亮")

    def draw_path(self, path):
        self.clear_highlight()
        for i in range(len(path)-1):
            a = path[i]
            b = path[i+1]
            x1, y1, _ = get_pos_by_id(a)
            x2, y2, _ = get_pos_by_id(b)
            line = self.canvas.create_line(x1, y1, x2, y2, fill="#ef4444", width=4)
            self.path_highlight.append(line)
        self.canvas.update()

    # 最少中转路线计算
    def calc_bfs(self):
        self.text_box.delete(1.0, tk.END)
        sname = self.start_entry.get().strip()
        ename = self.end_entry.get().strip()
        sid = get_id_by_name(sname)
        eid = get_id_by_name(ename)
        if not sid or not eid:
            self.log_print("【错误】未找到该起点/终点建筑，请重新输入名称")
            return
        path, step = graph.bfs_short_node_path(sid, eid)
        if not path:
            self.log_print("【提示】两点暂无连通道路，无法规划路线")
            return
        self.draw_path(path)
        self.log_print(f"【最少中转路线】途经路段数：{step}")
        self.log_print("完整路线：" + " → ".join([get_name_by_id(i) for i in path]))
        self.log_print("====分段步行指引====")
        for i in range(len(path)-1):
            a = get_name_by_id(path[i])
            b = get_name_by_id(path[i+1])
            self.log_print(f"{i+1}. {a} → {b}")

    # 最短距离路线计算
    def calc_dijk(self):
        self.text_box.delete(1.0, tk.END)
        sname = self.start_entry.get().strip()
        ename = self.end_entry.get().strip()
        sid = get_id_by_name(sname)
        eid = get_id_by_name(ename)
        if not sid or not eid:
            self.log_print("【错误】未找到该起点/终点建筑，请重新输入名称")
            return
        path, dist = graph.dijkstra_min_dist_path(sid, eid)
        if not path:
            self.log_print("【提示】两点暂无连通道路，无法规划路线")
            return
        self.draw_path(path)
        self.log_print(f"【最短步行距离路线】总路程：{dist} 米")
        self.log_print("完整路线：" + " → ".join([get_name_by_id(i) for i in path]))
        self.log_print("====分段步行指引====")
        for i in range(len(path)-1):
            a = get_name_by_id(path[i])
            b = get_name_by_id(path[i+1])
            self.log_print(f"{i+1}. {a} → {b}")

    # 新建道路（权限校验）
    def add_road_gui(self):
        if not IS_ADMIN:
            self.log_print("⚠️ 权限不足：仅管理员可编辑道路，请先登录")
            return
        try:
            a = int(self.rid1.get())
            b = int(self.rid2.get())
            d = int(self.dis_entry.get())
        except ValueError:
            self.log_print("❌ 输入错误：ID与距离必须填写纯数字")
            return
        res = graph.add_road(a, b, d)
        if res:
            msg = f"✅ 新建道路成功：{get_name_by_id(a)} ↔ {get_name_by_id(b)}，距离{d}米"
            self.log_print(msg)
            self.refresh_map()
        else:
            self.log_print("⚠️ 点位不存在或该道路已搭建")

    # 删除道路（权限校验）
    def del_road_gui(self):
        if not IS_ADMIN:
            self.log_print("⚠️ 权限不足：仅管理员可编辑道路，请先登录")
            return
        try:
            a = int(self.rid1.get())
            b = int(self.rid2.get())
        except ValueError:
            self.log_print("❌ 输入错误：ID必须填写纯数字")
            return
        res = graph.del_road(a, b)
        if res:
            self.log_print("✅ 道路删除成功")
            self.refresh_map()
        else:
            self.log_print("⚠️ 未查询到两点间的道路")

    # 重置地图（权限校验）
    def reset_data(self):
        if not IS_ADMIN:
            self.log_print("⚠️ 权限不足：仅管理员可重置地图，请先登录")
            return
        from tkinter import messagebox
        if messagebox.askyesno("确认重置", "重置将清空所有自建道路与新增点位，恢复原始什邡校区地图，确定继续？"):
            reset_all_data()
            self.refresh_map()
            self.text_box.delete(1.0, tk.END)
            self.log_print("✅ 地图数据已重置为初始状态")

# 程序入口启动
if __name__ == "__main__":
    load_places()
    main_root = tk.Tk()
    app = NavGUI(main_root)
    main_root.mainloop()
