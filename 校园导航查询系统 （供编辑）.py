# ==========================================
# 校园导航查询系统 V5.0
# 数据结构：List + Dict + BST二叉搜索树
# 算法：KMP、BM、二叉搜索树BST
# 新增：持久化txt、距离计算、搜索历史、自动ID、分类统计、排序
# ==========================================
import os

# 持久化文件
DATA_FILE = "places.txt"
# 全局缓存
campus_places = []
search_history = []
bst_root = None

# 初始默认地点（带平面坐标x,y）
default_places = [
    {"id": 1, "name": "弘义楼", "location": "教学楼", "x": 12, "y": 25},
    {"id": 2, "name": "致远楼", "location": "教学楼", "x": 15, "y": 22},
    {"id": 3, "name": "明德楼", "location": "教学楼", "x": 18, "y": 20},
    {"id": 4, "name": "明理楼", "location": "教学楼", "x": 21, "y": 18},
    {"id": 5, "name": "明志楼", "location": "教学楼", "x": 24, "y": 16},
    {"id": 6, "name": "明善楼", "location": "教学楼", "x": 27, "y": 14},
    {"id": 7, "name": "图书馆", "location": "校内图书阅览中心", "x": 10, "y": 30},
    {"id": 8, "name": "筑梦活动中心", "location": "校内活动场所", "x": 30, "y": 28},
    {"id": 9, "name": "旭日餐厅", "location": "校内食堂", "x": 35, "y": 32},
    {"id": 10, "name": "体育场", "location": "校内运动场地", "x": 8, "y": 10},
    {"id": 11, "name": "看台", "location": "体育场附属设施", "x": 7, "y": 8},
    {"id": 12, "name": "1A宿舍楼", "location": "学生宿舍", "x": 40, "y": 12},
    {"id": 13, "name": "1B宿舍楼", "location": "学生宿舍", "x": 42, "y": 14},
    {"id": 14, "name": "2A宿舍楼", "location": "学生宿舍", "x": 44, "y": 16},
    {"id": 15, "name": "2B宿舍楼", "location": "学生宿舍", "x": 46, "y": 18},
    {"id": 16, "name": "3A宿舍楼", "location": "学生宿舍", "x": 48, "y": 20},
    {"id": 17, "name": "3B宿舍楼", "location": "学生宿舍", "x": 50, "y": 22},
]

# ===================== KMP =====================
def get_next(pattern):
    nxt = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j
    return nxt

def kmp(text, pattern):
    if pattern == "":
        return True
    nxt = get_next(pattern)
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = nxt[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            return True
    return False

# ===================== BM =====================
def build_bad(pattern):
    bad = {}
    for i in range(len(pattern)):
        bad[pattern[i]] = i
    return bad

def bm(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return True
    bad = build_bad(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return True
        s += max(1, j - bad.get(text[s + j], -1))
    return False

# ===================== BST二叉树 =====================
class TreeNode:
    def __init__(self, place):
        self.place = place
        self.left = None
        self.right = None

def insert_bst(root, place):
    if root is None:
        return TreeNode(place)
    if place["id"] < root.place["id"]:
        root.left = insert_bst(root.left, place)
    else:
        root.right = insert_bst(root.right, place)
    return root

def build_bst_global():
    global bst_root
    bst_root = None
    for p in campus_places:
        bst_root = insert_bst(bst_root, p)

def bst_search(target):
    def _search(node, t):
        if node is None:
            return None
        if t == node.place["id"]:
            return node.place
        elif t < node.place["id"]:
            return _search(node.left, t)
        else:
            return _search(node.right, t)
    return _search(bst_root, target)

def inorder(root):
    if root:
        inorder(root.left)
        print(f"[{root.place['id']}] {root.place['name']} - {root.place['location']}")
        inorder(root.right)

def tree_height(root):
    if root is None:
        return 0
    return max(tree_height(root.left), tree_height(root.right)) + 1

def count_leaf(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaf(root.left) + count_leaf(root.right)

# ===================== V5 持久化读写 =====================
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for p in campus_places:
            line = f"{p['id']}|{p['name']}|{p['location']}|{p['x']}|{p['y']}\n"
            f.write(line)

def load_data():
    global campus_places
    if not os.path.exists(DATA_FILE):
        campus_places = default_places.copy()
        save_data()
        return
    tmp = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                pid, pname, ploc, px, py = line.split("|")
                tmp.append({
                    "id": int(pid),
                    "name": pname,
                    "location": ploc,
                    "x": int(px),
                    "y": int(py)
                })
