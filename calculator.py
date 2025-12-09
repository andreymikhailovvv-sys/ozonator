def calculate_unit_economy(product):
    # Safely extract numeric fields with defaults to avoid KeyError/TypeError
    def _num(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return 0.0

    name = product.get("name") or "Без названия"
    price = _num(product.get("price"))
    commission_rate = _num(product.get("commission_rate"))
    logistics = _num(product.get("logistics"))
    storage = _num(product.get("storage"))
    buy_price = _num(product.get("buy_price"))

    commission_value = price * commission_rate
    gross_profit = price - commission_value - logistics - storage
    net_profit = gross_profit - buy_price

    margin_percent = (net_profit / price * 100) if price > 0 else 0
    roi = (net_profit / buy_price * 100) if buy_price > 0 else None

    lines = [
        f"Название: {name}",
        f"Цена продажи: {price:.2f} RUB",
        f"Закупочная цена: {buy_price:.2f} RUB",
        f"Комиссия Ozon ({commission_rate*100:.1f}%): {commission_value:.2f} RUB",
        f"Логистика: {logistics:.2f} RUB",
        f"Хранение: {storage:.2f} RUB",
        "",
        f"Чистая прибыль на товар: {net_profit:.2f} RUB",
        f"Маржинальность: {margin_percent:.2f}%",
    ]

    if roi is not None:
        lines.append(f"ROI: {roi:.2f}%")
    else:
        lines.append("ROI: нет данных")

    return "\n".join(lines)
