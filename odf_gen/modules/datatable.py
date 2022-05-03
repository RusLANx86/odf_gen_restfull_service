from odf import  table, text

def valuetype(val):
    valuetype="string"
    if isinstance(val,str): valuetype="string"
    if isinstance(val,int): valuetype="float"
    if isinstance(val,float): valuetype="float"
    if isinstance(val,bool): valuetype="boolean"
    return valuetype


class DataTable(object):

    def __init__(self, values=()):
        self.values = values
        self.datasourcehaslabels = "none"

    def _set_values(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            self.__dict__['values'] = value
            firstrow = value[0]
            # print('firstrow:', len(firstrow))
            if isinstance(firstrow, list) or isinstance(firstrow, tuple):
                self.numcols = len(firstrow)
            else:
                self.numcols = 1
        else:
            raise ValueError('Value must be list or tuple.')

    def __setattr__(self, name, value):
        if name == 'values':
            self._set_values(value)
        else:
            self.__dict__[name] = value

    def __call__(self):
        datatable = table.Table(name="local-table")
        if self.datasourcehaslabels in ('row','both'):
            t = table.TableHeaderColumns()
            t.addElement(table.TableColumn())
            datatable.addElement(t)

        t = table.TableColumns()
        if self.datasourcehaslabels in ('row','both'):
            t.addElement(table.TableColumn(numbercolumnsrepeated=str(self.numcols-1)))
        else:
            t.addElement(table.TableColumn(numbercolumnsrepeated=str(self.numcols)))
        datatable.addElement(t)

        if self.datasourcehaslabels in ('column','both'):
            t = table.TableHeaderRows()
            datatable.addElement(t)
            tr = table.TableRow()
            t.addElement(tr)
            content = self.values[0]
            for val in content:
                tc = table.TableCell(valuetype=valuetype(val))
                tr.addElement(tc)
                tc.addElement(text.P(text=str(val)))

        t = table.TableRows()
        datatable.addElement(t)
        rownum = 0
        for content in self.values:
            if rownum == 0 and self.datasourcehaslabels in ('column','both'):
                rownum += 1
                continue
            tr = table.TableRow()
            t.addElement(tr)
            for val in content:
                tc = table.TableCell(valuetype=valuetype(val), value=val)
                tr.addElement(tc)
                tc.addElement(text.P(text=str(val)))
            rownum += 1
        return datatable