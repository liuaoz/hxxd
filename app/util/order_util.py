def generate_out_trade_no(order_no, old_out_trade_no=None):
    if not old_out_trade_no:
        return f"{order_no}_1"

    parts = old_out_trade_no.split("_")
    if len(parts) != 2 or not parts[1].isdigit():
        return f"{order_no}_1"

    order_no_suffix = int(parts[1])
    return f"{order_no}_{order_no_suffix + 1}"
