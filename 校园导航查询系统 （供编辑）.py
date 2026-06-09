# ==========================================
# 校园导航查询系统 V4.0（二叉树优化版）
# 数据结构：
# List + Dictionary + BST
#
# 算法：
# KMP
# BM
# BST
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

# ==========================================
# KMP算法
# ==========================================

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


# ==========================================
# BM算法
# ==========================================

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


# ==========================================
# BST
# ==========================================

class TreeNode:

    def __init__(self, place):

        self.place = place
        self.left = None
        self.right = None


def insert_bst(root, place):

    if root is None:
        return TreeNode(place)

    if place["id"] < root.place["id"]:

        root.left = insert_bst(
            root.left,
            place
        )

    else:

        root.right = insert_bst(
            root.right,
            place
        )

    return root


def build_bst():

    root = None

    for p in campus_places:

        root = insert_bst(
            root,
            p
        )

    return root


def bst_search(root, target):

    if root is None:
        return None

    if target == root.place["id"]:
        return root.place

    elif target < root.place["id"]:

        return bst_search(
            root.left,
            target
        )

    else:

        return bst_search(
            root.right,
            target
        )


def inorder(root):

    if root:

        inorder(root.left)

        print(
            f"[{root.place['id']}] "
            f"{root.place['name']} - "
            f"{root.place['location']}"
        )

        inorder(root.right)


def tree_height(root):

    if root is None:
        return 0

    return max(
        tree_height(root.left),
        tree_height(root.right)
    ) + 1


def count_leaf(root):

    if root is None:
        return 0

    if root.left is None and root.right is None:
        return 1

    return (
        count_leaf(root.left)
        + count_leaf(root.right)
    )


# ==========================================
# 功能函数
# ==========================================

def show_all():

    print("\n=====全部地点=====")

    for p in campus_places:

        print(
            f"[{p['id']}] "
            f"{p['name']} - "
            f"{p['location']}"
        )


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

    campus_places.append(
        {
            "id": id,
            "name": name,
            "location": location
        }
    )

    print("添加成功")


def delete_place():

    id = int(input("编号:"))

    for p in campus_places:

        if p["id"] == id:

            campus_places.remove(p)

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

    print(
        "树高:",
        tree_height(root)
    )

    print(
        "叶子节点数:",
        count_leaf(root)
    )


# ==========================================
# 菜单
# ==========================================

def menu():

    print("\n====== V4.0 ======")

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

    print("0 退出")


# ==========================================
# 主函数
# ==========================================

def main():

    while True:

        menu()

        choice = input("请选择：")

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

        elif choice == "0":

            print("系统退出")

            break

        else:

            print("输入错误")


if __name__ == "__main__":
    main()

