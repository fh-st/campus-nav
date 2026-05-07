# 校园导航查询系统 V1.0（初始静态版）
# 数据结构：列表 + 字典
# 核心算法：线性查找（顺序查找）

def main():

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

    print("===== 校园导航查询系统 V1.0 =====")
    while True:
        print("\n【菜单】")
        print("1.txt 查看所有地点")
        print("2 按名称查询地点")
        print("0 退出系统")
        choice = input("请输入操作序号：")

        if choice == "0":
            print("系统已退出。")
            break

        elif choice == "1.txt":
            print("\n===== 校园全部地点 =====")
            for p in campus_places:
                print(f"[{p['id']}] {p['name']} - {p['location']}")

        elif choice == "2":
            name = input("请输入要查询的地点名称：")
            found = False
            # 线性查找 O(n)
            for p in campus_places:
                if p["name"] == name:
                    print("\n查询结果：")
                    print(f"编号：{p['id']}")
                    print(f"名称：{p['name']}")
                    print(f"位置说明：{p['location']}")
                    found = True
                    break
            if not found:
                print("未找到该地点。")

        else:
            print("输入无效，请重新选择。")

if __name__ == "__main__":
    main()