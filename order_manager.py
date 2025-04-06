import json

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"


def load_data(filename: str) -> list:
    """讀取 JSON 資料，若檔案不存在則回傳空列表"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_orders(filename: str, orders: list) -> None:
    """儲存訂單資料到 JSON 檔案"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)


def calculate_order_total(order: dict) -> int:
    """計算單筆訂單總金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])


def add_order(orders: list) -> str:
    """新增訂單到列表，檢查編號重複與資料合法性"""
    order_id = input("請輸入訂單編號：").strip().upper()

    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：").strip()
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if name == "":
            break

        while True:
            try:
                price = int(input("請輸入價格：").strip())
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        while True:
            try:
                quantity = int(input("請輸入數量：").strip())
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({
        "order_id": order_id,
        "customer": customer,
        "items": items
    })

    save_orders(INPUT_FILE, orders)
    return f"=> 訂單 {order_id} 已新增！"


def print_order_report(data: list, title="訂單報表", single=False) -> None:
    """列印訂單報表，格式統一"""
    if single:
        print(f"\n==================== 出餐訂單 ====================")
    else:
        print(f"\n==================== {title} ====================")

    for idx, order in enumerate(data, start=1):
        if not single:
            print(f"訂單 #{idx}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print("商品名稱\t單價\t數量\t小計")
        print("-" * 50)

        total = 0
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            print(f"{item['name']}\t{item['price']}\t{item['quantity']}\t{subtotal}")

        print("-" * 50)
        print(f"訂單總額: {total:,}")
        print("=" * 50)


def process_order(orders: list) -> tuple[str, dict | None]:
    """顯示可出餐訂單，選擇後轉移到 output_orders.json"""
    if not orders:
        return "=> 無待處理訂單", None

    print("\n======== 待處理訂單列表 ========")
    for idx, order in enumerate(orders, start=1):
        print(f"{idx}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    while True:
        selection = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
        if selection == "":
            return "=> 已取消出餐處理", None

        if not selection.isdigit():
            print("=> 錯誤：請輸入有效的數字")
            continue

        index = int(selection) - 1
        if 0 <= index < len(orders):
            order = orders.pop(index)
            completed = load_data(OUTPUT_FILE)
            completed.append(order)
            save_orders(INPUT_FILE, orders)
            save_orders(OUTPUT_FILE, completed)
            return f"=> 訂單 {order['order_id']} 已出餐完成", order
        else:
            print("=> 錯誤：請選擇有效的訂單編號")


def main() -> None:
    """主程式：選單控制與功能呼叫"""
    while True:
        print("\n***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()

        if choice == "":
            break
        elif choice == "1":
            orders = load_data(INPUT_FILE)
            result = add_order(orders)
            print(result)
        elif choice == "2":
            orders = load_data(INPUT_FILE)
            print_order_report(orders)
        elif choice == "3":
            orders = load_data(INPUT_FILE)
            result, selected_order = process_order(orders)
            print(result)
            if selected_order:
                print("\n出餐訂單詳細資料：")
                print_order_report([selected_order], single=True)
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")


if __name__ == "__main__":
    main()
