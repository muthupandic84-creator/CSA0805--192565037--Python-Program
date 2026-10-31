"""Q5: Function parameters, return values, and variable scope."""

def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order

def calculate_bill(items, gst_rate=0.05):
    subtotal = sum(items)
    gst = subtotal * gst_rate
    total = subtotal + gst
    return total, gst

college_name = "SIMATS ENGINEERING"

def show_local_global():
    local_message = "This is local"
    print(local_message)
    print("Global value:", college_name)

def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

def main():
    print("Buggy shared default:")
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print("Correct independent defaults:")
    print(add_item("Tea"), add_item("Vada"))

    customer_orders = []
    customer_orders.append(add_item("Tea"))
    customer_orders.append(add_item("Vada"))
    customer_orders.append(add_item("Coffee"))
    print("Three customer orders:", customer_orders)

    total, gst = calculate_bill([40, 30, 20], gst_rate=0.05)
    print(f"Total including GST: Rs {total:.2f}; GST: Rs {gst:.2f}")

    show_local_global()
    counter = make_counter()
    print("Nonlocal counter:", counter(), counter(), counter())

    print("Buggy default list object:", add_item_buggy.__defaults__)

if __name__ == "__main__":
    main()
