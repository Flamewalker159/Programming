def _current_document():
    import uno

    ctx = uno.getComponentContext()
    service_manager = ctx.getServiceManager()
    desktop = service_manager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", ctx
    )
    doc = desktop.getCurrentComponent()
    if doc is None:
        raise RuntimeError("Нет открытого документа LibreOffice.")
    return doc


def _sheet_by_name(doc, name):
    sheets = doc.getSheets()
    if not sheets.hasByName(name):
        raise RuntimeError("В документе нет листа «{}».".format(name))
    return sheets.getByName(name)


def _as_number(value):
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _range_to_rows(cell_range):
    values = None

    try:
        values = cell_range.getValueArray()
    except Exception:
        values = None

    if values is None:
        try:
            values = cell_range.getDataArray()
        except Exception:
            values = None

    if values is None and isinstance(cell_range, (list, tuple)):
        values = cell_range

    if values is None:
        return [[cell_range]]

    if not isinstance(values, (list, tuple)):
        return [[values]]

    rows = []
    for row in values:
        if isinstance(row, (list, tuple)):
            rows.append(list(row))
        else:
            rows.append([row])
    return rows


def _flat_numbers(cell_range):
    for row in _range_to_rows(cell_range):
        for value in row:
            yield _as_number(value)

def OnClick(*args):
    try:
        doc = _current_document()
        sheet = _sheet_by_name(doc, "Лист1")

        first_data_row = 2
        store_count = 4

        # Получаем план из K4
        plan = _as_number(sheet.getCellRangeByName("K1").getValue())

        if plan <= 0:
            raise ValueError("В ячейке K1 не указан план продаж.")

        totals = []

        # Считаем выручку за три месяца
        for row in range(first_data_row, first_data_row + store_count):
            sales = sum(
                _as_number(
                    sheet.getCellRangeByName("{}{}".format(col, row)).getValue()
                )
                for col in ("B", "C", "D")
            )

            # Записываем выручку в E
            sheet.getCellRangeByName("E{}".format(row)).setValue(sales)
            totals.append(sales)

        # Сортируем выручку по убыванию методом выбора
        ranked_totals = totals[:]

        for i in range(len(ranked_totals) - 1):
            max_index = i

            for j in range(i + 1, len(ranked_totals)):
                if ranked_totals[j] > ranked_totals[max_index]:
                    max_index = j

            if max_index != i:
                ranked_totals[i], ranked_totals[max_index] = (
                    ranked_totals[max_index],
                    ranked_totals[i]
                )

        # Рассчитываем проценты и премию
        for index, row in enumerate(
            range(first_data_row, first_data_row + store_count)
        ):
            total = totals[index]

            plan_percent = 2 if total >= plan else 0

            if total == ranked_totals[0]:
                place_percent = 4
            elif total == ranked_totals[1]:
                place_percent = 2
            elif total == ranked_totals[2]:
                place_percent = 1
            else:
                place_percent = 0

            total_percent = plan_percent + place_percent
            premium = total * total_percent / 100.0

            sheet.getCellRangeByName("F{}".format(row)).setValue(plan_percent)
            sheet.getCellRangeByName("G{}".format(row)).setValue(place_percent)
            sheet.getCellRangeByName("H{}".format(row)).setValue(total_percent)
            sheet.getCellRangeByName("I{}".format(row)).setValue(premium)

    except Exception:
        import traceback
        traceback.print_exc()


def OnClick2(*args):
    try:
        doc = _current_document()
        sheet = _sheet_by_name(doc, "Лист2")
        for row in range(1, 5):
            sales = sum(
                _as_number(sheet.getCellByPosition(col, row).getValue())
                for col in (1, 2, 3)
            )
            sheet.getCellByPosition(4, row).setValue(sales)
            sheet.getCellByPosition(5, row).setValue(Premia(sales))
    except Exception:
        import traceback
        traceback.print_exc()

def Premia(sales):
    value = _as_number(sales)
    if value < 20000:
        return 0.0
    if value <= 40000:
        return value * 0.03
    if value <= 80000:
        return value * 0.045
    return value * 0.065

def SUMQW1(cell_range):
    """Return the sum of squares of all numeric values in a Calc range."""
    return sum(value * value for value in _flat_numbers(cell_range))


def FORMULA1(sheet_name, a_range, c_range):
    try:
        doc = _current_document()
        sheet = _sheet_by_name(doc, str(sheet_name))
        vector = sheet.getCellRangeByName(str(a_range))
        matrix = sheet.getCellRangeByName(str(c_range))
        return FORMULA1_RANGES(vector, matrix)
    except Exception:
        import traceback
        traceback.print_exc()
        return 0.0


def FORMULA1_RANGES(a_range, c_range):
    a_values = list(_flat_numbers(a_range))
    c_values = list(_flat_numbers(c_range))
    sum_a = sum(a_values)
    sum_c = sum(c_values)
    sum_a_squares = sum(value * value for value in a_values)
    denominator = (1.0 + sum_a) * (1.0 + sum_a_squares)
    if denominator == 0:
        return 0.0
    return (2.0 * sum_a + sum_c) / denominator

def SUMMIDDLE(cell_range):
    matrix = _range_to_rows(cell_range)
    if not matrix:
        return 0.0

    row_count = len(matrix)
    col_count = max((len(row) for row in matrix), default=0)
    if col_count == 0:
        return 0.0

    if row_count % 2 == 0:
        middle_rows = {row_count // 2 - 1, row_count // 2}
    else:
        middle_rows = {row_count // 2}

    if col_count % 2 == 0:
        middle_cols = {col_count // 2 - 1, col_count // 2}
    else:
        middle_cols = {col_count // 2}

    result = 0.0
    for row_index, row in enumerate(matrix):
        for col_index in range(col_count):
            if row_index in middle_rows or col_index in middle_cols:
                value = row[col_index] if col_index < len(row) else 0
                result += _as_number(value)

    return result

def WriteCurrentTime(*args):
    from datetime import datetime
    try:
        doc = _current_document()
        sheet = doc.getCurrentController().getActiveSheet()
        cell = sheet.getCellRangeByName("A1")
        cell.setString(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    except Exception:
        import traceback
        traceback.print_exc()


# The tuple is required by LibreOffice to expose the Python entry points.
g_exportedScripts = (
    OnClick,
    OnClick2,
    Premia,
    SUMQW1,
    FORMULA1,
    FORMULA1_RANGES,
    SUMMIDDLE,
    WriteCurrentTime,
)
