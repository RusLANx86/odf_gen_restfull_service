from odf.opendocument import OpenDocument
from odf import chart, style, text

# import a support class from the examples directory
from odf_gen.modules.datatable import DataTable


class create_chart(object):

    def __init__(self, chart_data):
        self.ChartProperties = chart_data["meta"]["style"]
        # self.charttype = 'chart:circle'
        self.charttype = "chart:"+self.ChartProperties["type"]
        self.subtype = self.ChartProperties["subtype"]  # 'percentage', 'stacked' or 'normal'
        self.threedimensional = "true"
        self.x_axis = "X"
        self.y_axis = "Y"
        self.values = (1,2,3)
        self.title = None
        self.subtitle = None
        self.chart = None

        self.title = "Схема"
        self.subtitle = "Вооружённые силы Российской Федерации"
        self.x_axis = u"Рода войск"
        self.y_axis = u"Тысяч человек"
        self.values = chart_data["data"]
        self.datasourcehaslabels = "both"

    def __call__(self, doc: OpenDocument):
        chartstyle  = style.Style(name="chartstyle", family="chart")
        chartstyle.addElement( style.GraphicProperties(stroke="none", fillcolor="#ffffff"))

        doc.automaticstyles.addElement(chartstyle)

        mychart = chart.Chart( width="570pt", height="500pt", stylename=chartstyle, attributes={'class':self.charttype})
        doc.chart.addElement(mychart)

        # Title
        if self.title:
            titlestyle = style.Style(name="titlestyle", family="chart")
            titlestyle.addElement( style.GraphicProperties(stroke="none", fill="none"))
            titlestyle.addElement( style.TextProperties(fontfamily="'Nimbus Sans L'",
                    fontfamilygeneric="swiss", fontpitch="variable", fontsize="13pt"))
            doc.automaticstyles.addElement(titlestyle)

            mytitle = chart.Title(x="300pt", y="25pt", stylename=titlestyle)
            mytitle.addElement( text.P(text=self.title))
            mychart.addElement(mytitle)

        # Subtitle
        if self.subtitle:
            subtitlestyle = style.Style(name="subtitlestyle", family="chart")
            subtitlestyle.addElement( style.GraphicProperties(stroke="none", fill="none"))
            subtitlestyle.addElement( style.TextProperties(fontfamily="'Nimbus Sans L'",
                    fontfamilygeneric="swiss", fontpitch="variable", fontsize="10pt"))
            doc.automaticstyles.addElement(subtitlestyle)

            subtitle = chart.Subtitle(x="100pt", y="50pt", stylename=subtitlestyle)
            subtitle.addElement( text.P(text= self.subtitle))
            mychart.addElement(subtitle)

        # Legend
        legendstyle = style.Style(name="legendstyle", family="chart")
        legendstyle.addElement( style.GraphicProperties(fill="none"))
        legendstyle.addElement( style.TextProperties(fontfamily="'Nimbus Sans L'",
                fontfamilygeneric="swiss", fontpitch="variable", fontsize="6pt"))
        doc.automaticstyles.addElement(legendstyle)

        mylegend = chart.Legend(legendposition="bottom", legendalign="center", stylename=legendstyle)
        mychart.addElement(mylegend)

        # Plot area
        plotstyle = style.Style(name="plotstyle", family="chart")
        if self.subtype == "stacked": percentage="false"; stacked="true"
        elif self.subtype == "percentage": percentage="true"; stacked="false"
        else: percentage="false"; stacked="false"
        plotstyle.addElement( style.ChartProperties(seriessource="columns",
                percentage=percentage, stacked=stacked,
                threedimensional=self.ChartProperties["3D_view"]))
        doc.automaticstyles.addElement(plotstyle)

        plotarea = chart.PlotArea(datasourcehaslabels=self.datasourcehaslabels, stylename=plotstyle)
        mychart.addElement(plotarea)

        # Style for the X,Y axes
        axisstyle = style.Style(name="axisstyle", family="chart")
        axisstyle.addElement( style.ChartProperties(displaylabel="true"))
        doc.automaticstyles.addElement(axisstyle)

        # Title for the X axis
        xaxis = chart.Axis(dimension="x", name="primary-x", stylename=axisstyle)
        plotarea.addElement(xaxis)
        xt = chart.Title()
        xaxis.addElement(xt)
        xt.addElement(text.P(text=self.x_axis))

        # Title for the Y axis
        yaxis = chart.Axis(dimension="y", name="primary-y", stylename=axisstyle)
        plotarea.addElement(yaxis)
        yt = chart.Title()
        yaxis.addElement(yt)
        yt.addElement(text.P(text=self.y_axis))

        # Data area
        datatable = DataTable( self.values )

        n = datatable.numcols
        for i in range(n-1):
            letter = chr(i + 66)
            color = self.get_color_col_style(doc, i)
            s = chart.Series(
                                valuescellrangeaddress="local-table."+letter+"2:."+letter+(n+3).__str__(),
                                labelcelladdress="local-table."+letter+"1",
                                stylename=color
                             )
            s.addElement(chart.DataPoint(repeated=3+n))
            plotarea.addElement(s)

        datatable.datasourcehaslabels = self.datasourcehaslabels
        mychart.addElement(datatable())

    def get_color_col_style(self, doc: OpenDocument, num_of_color: int):
        import random
        r = lambda: random.randint(0, 255)
        color = ('#%02X%02X%02X' % (r(), r(), r()))
        col_style = style.Style(name=color, family="chart")
        col_style.addElement(style.ChartProperties(linkdatastyletosource="true"))
        col_style.addElement(style.GraphicProperties(stroke="none", fillcolor=color))
        doc.automaticstyles.addElement(col_style)
        return color
