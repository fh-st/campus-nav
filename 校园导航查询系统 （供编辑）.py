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

