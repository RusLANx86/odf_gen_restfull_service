from odf.opendocument import OpenDocument, OpenDocumentChart
from odf.style import Style, TableCellProperties, TableRowProperties, TableProperties, TableColumnProperties, \
    ListLevelProperties
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.text import P, List, ListItem, ListLevelStyleNumber, ListStyle
from odf_gen.modules.marmalades import create_chart


class Table_Cell_Style_Attr:
    def __init__(self, border_style):
        self.all_border_cell_style = {
            "verticalalign": "middle",
            "border": border_style
        }
        self.left_top_cs_attr = {"verticalalign": "middle", "bordertop": border_style, "borderleft": border_style}
        self.top_cs_attr = {"verticalalign": "middle", "bordertop": border_style}
        self.right_top_cs_attr = {"verticalalign": "middle", "bordertop": border_style, "borderright": border_style}
        self.left_cs_attr = {"verticalalign": "middle", "borderleft": border_style}
        self.right_cs_attr = {"verticalalign": "middle", "borderright": border_style}
        self.left_bottom_cs_attr = {"verticalalign": "middle", "borderleft": border_style, "borderbottom": border_style}
        self.bottom_cs_attr = {"verticalalign": "middle", "borderbottom": border_style}
        self.right_bottom_cs_attr = {"verticalalign": "middle", "borderright": border_style, "borderbottom": border_style}


def update_odf_element(element, data: dict) -> OpenDocument:
    data_type = data["type"]
    if data_type == "Table":
        return create_odf_table(odf_element=element, data=data)
    elif data_type == "List":
        if element.tagName == "text:user-field-get":
            list_el = create_odf_list(data_list=data["data"])
            odf_list_el = list_el["element"]
            replace_odf_element(new_element=odf_list_el, old_element=element.parentNode)
    elif data_type == "String":
        return create_str_el(odf_element=element, text=data["data"])
    elif data_type == "Chart":
        return create_odf_chart(chart_data=data)


def create_odf_chart(chart_data) -> dict:
    doc = OpenDocumentChart()
    mychart = create_chart(chart_data)
    mychart(doc)
    res = {
        "element": doc,
        "style": None
    }
    return res


def replace_odf_element(new_element, old_element):
    parent = old_element.parentNode
    parent.insertBefore(newChild=new_element, refChild=old_element)
    parent.removeChild(oldChild=old_element)


def return_table_size(data: list) -> dict:
    cols = 0
    rows = 0
    for row in data:
        rows += 1
        c = 0
        for cell in row:
            if cell.__contains__("colspan"):
                c += cell["colspan"]
            else:
                c += 1
            if c > cols:
                cols = c
    return {"cols": cols, "rows": rows}


def create_str_el(odf_element, text) -> None:
    if odf_element.tagName == "text:user-field-decl":
        odf_element.setAttribute('stringvalue', text)


def create_odf_table(data, odf_element) -> dict:
    styles = []

    thin_border = "0.05pt solid #000000"
    bolt_border = "0.5pt solid #000000"

    cs_attr = Table_Cell_Style_Attr(border_style=thin_border)

    all_cells_style = Style(name="all_border_cell_style", family="table-cell")
    all_cells_content_style = TableCellProperties(attributes=cs_attr.all_border_cell_style)
    all_cells_style.addElement(all_cells_content_style)
    styles.append(all_cells_style)

    row_style = Style(name="row_style", family="table-row")
    row_style.addElement(TableRowProperties(keeptogether="always"))

    table_style = Style(name="table_style", family="table")
    table_style.addElement(TableProperties(bordermodel="collapsing"))
    styles.append(table_style)

    cell_style_name = all_cells_style
    content_cell_style_name = all_cells_content_style

    if data.__contains__("table_title"):
        title = data["table_title"]
    data = data["data"]
    params = return_table_size(data=data)
    cols = params["cols"]
    rows = params["rows"]

    if odf_element.tagName == "text:user-field-get":
        data = title + data
        t = Table(stylename=table_style)
        t.addElement(TableColumn(numbercolumnsrepeated=cols))
        pn1 = odf_element.parentNode
        pn1.removeChild(odf_element)
        pn2 = pn1.parentNode
        pn2.insertBefore(t, pn1)
        pn2.removeChild(pn1)
        odf_element = t

    elif odf_element.tagName == "table:table":
        last_title_table_row = odf_element.childNodes[-1]
        row_style = last_title_table_row.getAttribute("stylename")
        last_title_table_cells_styles = []
        for cell in last_title_table_row.childNodes:
            cell_style_name = cell.getAttribute("stylename")
            content_cell_style_name = cell.childNodes[0].getAttribute("stylename")
            last_title_table_cells_styles.append([cell_style_name, content_cell_style_name, cell.childNodes[0]])
        del odf_element.childNodes[-1]

    else:
        return None

    styles.append(row_style)

    for row in range(len(data)):
        tr = TableRow(stylename=row_style)
        cur_cols_count = len(data[row])
        for col in range(cur_cols_count):
            name = None
            try:
                cell_style_name, content_cell_style_name, _ = last_title_table_cells_styles[(cols-cur_cols_count)+col]
            except:
                pass
            tc = TableCell(stylename=cell_style_name, valuetype="string")
            el = data[row][col]
            if type(el)==dict:
                if el.__contains__("label"):
                    name = el["label"]
                if el.__contains__("odf_elems"):
                    data_list_odf_elems = el["odf_elems"]
                    for data_odf_elem in data_list_odf_elems:
                        odf_elem_type = data_odf_elem["type"]
                        if odf_elem_type == "String":
                            odf_elem = P(stylename=content_cell_style_name, text=data_odf_elem["data"])
                        elif odf_elem_type == "List":
                            odf_elem = (create_odf_list(
                                data_list=data_odf_elem["data"],
                                stylename=content_cell_style_name
                            ))["element"]
                        tc.addElement(odf_elem)

                if el.__contains__("colspan"):
                    tc.setAttribute("numbercolumnsspanned", el["colspan"])
                if el.__contains__("rowspan"):
                    tc.setAttribute("numberrowsspanned", el["rowspan"])

            else:
                name = el

            # text = name.split('new_element')
            # for odf_text in text:
            #     p = P(text=odf_text)
            #     tc.addElement(p)

            p = P(stylename=content_cell_style_name, text=name)
            tc.addElement(p)
            tr.addElement(tc)
        odf_element.addElement(tr)


    res = {
        "element": odf_element,
        "styles": styles,
    }
    return res


def create_odf_list(data_list: list, stylename=None):
    textList = List(stylename='style_analisys')
    for el in data_list:
        p = P(stylename=stylename) if stylename else P()
        sub_list = None
        if el.__contains__("text"):
            p.addText(el["text"])
            el.__delitem__("text")
        if el.__contains__("cdata"):
            p.addCDATA(el["cdata"])
            el.__delitem__("cdata")
        if el.__contains__("data"):
            sub_list = create_odf_list(el["data"])["element"]
            el.__delitem__("data")
        for attr in el:
            p.setAttribute(attr, el.get(attr))
        item = ListItem()
        item.addElement(p)
        if sub_list: item.addElement(sub_list)
        textList.addElement(item)

    res = {
        "element": textList,
        "styles": None
    }
    return res
