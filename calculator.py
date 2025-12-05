def calculate_unit_economy(product):
    name = product["name"]
    price = product["price"]
    commission_rate = product["commission_rate"]
    logistics = product["logistics"]
    storage = product["storage"]
    buy_price = product["buy_price"]

    commission_value = price * commission_rate
    gross_profit = price - commission_value - logistics - storage
    net_profit = gross_profit - buy_price

    margin_percent = (net_profit / price * 100) if price > 0 else 0
    roi = (net_profit / buy_price * 100) if buy_price > 0 else None

    result = (
        f"Товар: {name}\n"
        f"Цена продажи: {price:.2f} ₽\n"
        f"Себестоимость: {buy_price:.2f} ₽\n"
        f"Комиссия Ozon ({commission_rate*100:.1f}%): {commission_value:.2f} ₽\n"
        f"Логистика: {logistics:.2f} ₽\n"
        f"Хранение: {storage:.2f} ₽\n\n"
        f"Чистая прибыль: {net_profit:.2f} ₽\n"
        f"Маржинальность: {margin_percent:.2f}%\n"
        f"ROI: {roi:.2f}%\n" if roi is not None else "ROI: —"
    )
    return result
