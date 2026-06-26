# ==========================================
# 校园导航查询系统 V5.0（图结构扩展版）
# 数据结构：List + Dictionary + BST + 无向图
# 算法：KMP、BM、BST、BFS（图最短路径）
# 承接V4全部功能，新增校园道路连通图模块
# ==========================================
campus_places = [
    {"id": 1, "name": "弘义楼", "location": "教学楼"},
    {"id": 2, "name": "致远楼", "location": "教学楼"},
    {"id": 3, "name": "明德楼", "location": "教学楼"},
    {"id": 4, "name": "明理楼", "location": "教学楼"},
    {"id": 5, "name": "明志楼", "location": "教学楼"},
    {"id": 6, "name": "明善楼", "location": "教学楼"},
    {"id": 7, "name": "图书馆", "location": "校内图书阅览中心"},
    {"id": 8, "name": "筑梦活动中心", "location": "校内活动场所"},
    {"id": 9, "name": "旭日餐厅", "location": "校内食堂"},
    {"id": 10, "name": "体育场", "location": "校内运动场地"},
    {"id": 11, "name": "看台", "location": "体育场附属设施"},
    {"id": 12, "name": "1A宿舍楼", "location": "学生宿舍"},
    {"id": 13, "name": "1B宿舍楼", "location": "学生宿舍"},
    {"id": 14, "name": "2A宿舍楼", "location": "学生宿舍"},
    {"id": 15, "name": "2B宿舍楼", "location": "学生宿舍"},
    {"id": 16, "name": "3A宿舍楼", "location": "学生宿舍"},
    {"id": 17, "name": "3B宿舍楼", "location": "学生宿舍"},
]

# ====================== 新增：无向图结构实现 ======================
class CampusGraph:
    def __init__(self):
        # 邻接表存储图：key=地点id，value=可直达的地点id列表
        self.adj = {}
        # 初始化所有地点为图顶点，初始无连通道路
        for place in campus_places:
            self.adj[place["id"]] = []

    # 添加双向道路（无向边）
    def add_road(self, id1, id2):
        if id1 not in self.adj or id2 not in self.adj:
            print("错误：地点编号不存在！")
            return
        if id2 not in self.adj[id1]:
            self.adj[id1].append(id2)
            self.adj[id2].append(id1)
            print(f"已修建道路：{id1} <--> {id2}")
        else:
            print("两点间已有道路，无需重复添加")

    # 删除双向道路
    def del_road(self, id1, id2):
        if id1 not in self.adj or id2 not in self.adj:
            print("错误：地点编号不存在！")
            return
        if id2 in self.adj[id1]:
            self.adj[id1].remove(id2)
            self.adj[id2].remove(id1)
            print(f"已拆除道路：{id1} <--> {id2}")
        else:
            print("两点间没有连通道路")

    # BFS广度优先搜索，查询两点最短路径
    def bfs_short_path(self, start_id, end_id):
        if start_id not in self.adj or end_id not in self.adj:
            return None
        if start_id == end_id:
            return [start_id]
        visited = {start_id}
        queue = [[start_id]]
        while queue:
            path = queue.pop(0)
            cur = path[-1]
            for neighbor in self.adj[cur]:
                if neighbor not in visited:
                    new_path = path.copy()
                    new_path.append(neighbor)
                    if neighbor == end_id:
                        return new_path
                    visited.add(neighbor)
                    queue.append(new_path)
        # 无法到达
        return None

    # 打印全部道路连通关系
    def show_all_roads(self):
        print("\n===== 校园道路连通图（邻接表）=====")
        for pid, link_list in self.adj.items():
            if link_list:
                print(f"地点{pid} 连通：{link_list}")
            else:
                print(f"地点{pid} 暂无连通道路")

# 全局图实例
graph = CampusGraph()

# ====================== 原有KMP算法（完整保留V4代码） ======================
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

# ====================== 原有BM算法（完整保留V4代码） ======================
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

# ====================== 原有BST二叉树（完整保留V4代码） ======================
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
def build_bst():
    root = None
    for p in campus_places:
        root = insert_bst(root, p)
    return root
def bst_search(root, target):
    if root is None:
        return None
    if target == root.place["id"]:
        return root.place
    elif target < root.place["id"]:
        return bst_search(root.left, target)
    else:
        return bst_search(root.right, target)
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

# ====================== 原有基础功能函数（完整保留V4） ======================
def show_all():
    print("\n=====全部地点=====")
    for p in campus_places:
        print(f"[{p['id']}] {p['name']} - {p['location']}")
def search_by_name():
    key = input("输入地点名称：")
    found = False
    for p in campus_places:
        if kmp(p["name"], key):
            print(p)
            found = True
    if not found:
        print("未找到")
def fuzzy_search():
    key = input("输入关键字：")
    found = False
    for p in campus_places:
        text = p["name"] + p["location"]
        if bm(text, key):
            print(p)
            found = True
    if not found:
        print("未找到")
def search_by_category():
    key = input("输入类别：")
    count = 0
    for p in campus_places:
        if key in p["location"]:
            print(p)
            count += 1
    print("共找到", count, "个地点")
def add_place():
    id = int(input("编号:"))
    name = input("名称:")
    location = input("位置:")
    campus_places.append({"id": id, "name": name, "location": location})
    # 新增地点同步加入图顶点
    graph.adj[id] = []
    print("添加成功")
def delete_place():
    id = int(input("编号:"))
    for p in campus_places:
        if p["id"] == id:
            campus_places.remove(p)
            # 删除地点同时清除图中所有关联道路
            del graph.adj[id]
            for k in graph.adj:
                if id in graph.adj[k]:
                    graph.adj[k].remove(id)
            print("删除成功")
            return
    print("未找到")
def modify_place():
    id = int(input("编号:"))
    for p in campus_places:
        if p["id"] == id:
            p["name"] = input("新名称:")
            p["location"] = input("新位置:")
            print("修改成功")
            return
    print("未找到")
def statistics():
    print("地点总数:", len(campus_places))
def bst_query():
    root = build_bst()
    id = int(input("输入编号:"))
    result = bst_search(root, id)
    if result:
        print(result)
    else:
        print("未找到")
def bst_info():
    root = build_bst()
    print("树高:", tree_height(root))
    print("叶子节点数:", count_leaf(root))

# ====================== V5新增：图结构专属功能 ======================
def graph_add_road():
    a = int(input("输入起点地点ID："))
    b = int(input("输入终点地点ID："))
    graph.add_road(a, b)
def graph_del_road():
    a = int(input("输入起点地点ID："))
    b = int(input("输入终点地点ID："))
    graph.del_road(a, b)
def graph_find_path():
    start = int(input("输入出发地点ID："))
    end = int(input("输入目标地点ID："))
    path = graph.bfs_short_path(start, end)
    if path is None:
        print("两点之间无连通道路，无法到达！")
    else:
        print(f"最短通行路径(ID序列)：{path}")
        # 匹配地点名称展示完整路径
        name_path = []
        for pid in path:
            for p in campus_places:
                if p["id"] == pid:
                    name_path.append(p["name"])
                    break
        print(f"完整路径名称：{' → '.join(name_path)}")
def graph_show_road():
    graph.show_all_roads()

# ====================== V5更新菜单（保留全部V4功能，新增图选项） ======================
def menu():
    print("\n====== 校园导航查询系统 V5.0（图结构版）======")
    print("===== 原有基础功能 =====")
    print("1 查看全部地点")
    print("2 KMP名称查询")
    print("3 BM模糊查询")
    print("4 分类查询")
    print("5 添加地点")
    print("6 删除地点")
    print("7 修改地点")
    print("8 地点统计")
    print("9 BST编号查询")
    print("10 BST中序遍历")
    print("11 BST统计信息")
    print("===== 新增图-道路连通功能 =====")
    print("12 查看所有校园道路")
    print("13 新建两点通行道路")
    print("14 删除两点通行道路")
    print("15 查询两点最短通行路径(BFS)")
    print("0 退出系统")

# ====================== 主程序逻辑 ======================
def main():
    while True:
        menu()
        choice = input("请选择功能编号：")
        if choice == "1":
            show_all()
        elif choice == "2":
            search_by_name()
        elif choice == "3":
            fuzzy_search()
        elif choice == "4":
            search_by_category()
        elif choice == "5":
            add_place()
        elif choice == "6":
            delete_place()
        elif choice == "7":
            modify_place()
        elif choice == "8":
            statistics()
        elif choice == "9":
            bst_query()
        elif choice == "10":
            root = build_bst()
            inorder(root)
        elif choice == "11":
            bst_info()
        # V5新增图功能分支
        elif choice == "12":
            graph_show_road()
        elif choice == "13":
            graph_add_road()
        elif choice == "14":
            graph_del_road()
        elif choice == "15":
            graph_find_path()
        elif choice == "0":
            print("系统退出，感谢使用！")
            break
        else:
            print("输入无效，请输入菜单内数字！")

if __name__ == "__main__":
    main()