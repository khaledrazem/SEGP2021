from pytrends.request import TrendReq  # pip install pytrends
import plotly.graph_objects as go  # pip install plotly==4.14.3
from plotly.offline import plot


def plotGraph(query1, query2):
    the_graph = {
        'graph1': [],
        'graph2': [],
    }

    """
    if query2 == None:
        kw_list = [query1]
    else:
        query3 = query1 + " and " + query2
        print(query3)
        kw_list = [query3]
    """

    if query2 == None:
        kw_list = [query1]
        title1 = "Trend of " + query1
    else:
        query3 = query1 + " " + query2
        kw_list = [query1, query2]
        kw_list2 = [query3]
        title2 = "Combination Trend of " + query1 + " and " + query2
        title1 = "Trend of " + query1 + " and " + query2

    # query3 = query1 + " " + query2
    # kw_list = [query1,query2,query3] #input keywords
    # kw_list = [query1] #input keywords

    pytrends = TrendReq(hl='en-US', tz=360)
    # keywords = pytrends.suggestions(keyword=query3)
    # print(keywords)
    daterange = "today 5-y"  # date range ( 5-y means 5 years )

    pytrends.build_payload(kw_list, cat=0, timeframe=daterange, geo='', gprop='')

    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'], axis='columns')

        trace = [go.Scatter(
            x=data.index,
            y=data[col], name=col) for col in data.columns]

        # plot graph
        fig = go.Figure(data=trace)
        fig.update_layout(
            title={
                'text': title1,
            },
            autosize=False,
            width=1000,
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
        )

        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(gridcolor='black', gridwidth=0.5)
        # fig.show()
        # plt_div = plot(fig,output_type='div')
        the_graph['graph1'] = plot(fig, output_type='div')
        # print(plt_div)

    if query2 != None:

        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list2, cat=0, timeframe=daterange, geo='', gprop='')
        data2 = pytrends.interest_over_time()

        if not data2.empty:
            data2 = data2.drop(labels=['isPartial'], axis='columns')

            trace = [go.Scatter(
                x=data2.index,
                y=data2[col], line=dict(color='#00FF00', width=2), name=col) for col in data2.columns]

            # plot graph
            fig2 = go.Figure(data=trace)
            fig2.update_layout(
                title={
                    'text': title2,
                },
                autosize=False,
                width=1000,
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
            )

            fig2.update_xaxes(showline=True, linewidth=2, linecolor='black')
            fig2.update_yaxes(showline=True, linewidth=2, linecolor='black')
            fig2.update_yaxes(gridcolor='black', gridwidth=0.5)

            the_graph['graph2'] = plot(fig2, output_type='div')
        else:
            fig2 = go.Figure(data=[])
            fig2.update_layout(
                title={
                    'text': title2,
                },
                autosize=False,
                width=1000,
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )

            fig2.update_xaxes(showline=True, linewidth=2, linecolor='black')
            fig2.update_yaxes(showline=True, linewidth=2, linecolor='black')
            fig2.update_yaxes(gridcolor='black', gridwidth=0.5)

            the_graph['graph2'] = plot(fig2, output_type='div')

    # return(plt_div)
    return the_graph