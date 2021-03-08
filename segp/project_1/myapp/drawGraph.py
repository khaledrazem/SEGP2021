from pytrends.request import TrendReq  # pip install pytrends
import plotly.graph_objects as go  # pip install plotly==4.14.3
from plotly.offline import plot


def plotGraph(query1, query2):
    the_graph = {
        'graph1': [],
        'graph2': [],
    }
    if query2 == None:
        kw_list = [query1]
        title1 = "Trend of " + query1
    else:
        query3 = query1 + " " + query2
        kw_list = [query1, query2]
        kw_list2 = [query3]
        title2 = "Combination Trend of " + query1 + " & " + query2
        title1 = "Trend of " + query1 + " & " + query2
        
    timeout = 0
    pytrends = TrendReq(hl='en-US', tz=360)
    daterange = "today 5-y"  # date range ( 5-y means 5 years )
    pytrends.build_payload(kw_list, cat=0, timeframe=daterange, geo='', gprop='')
    
    try:
        data1 = pytrends.interest_over_time()
    except:
        timeout = 1
        print("Google Trend down!")
    
    if timeout == 1:
        the_graph['graph1'] = emptyGraph(title1)
    else:
        if not data1.empty:
            data1 = data1.drop(labels=['isPartial'], axis='columns')

            trace = [go.Scatter(
                x=data1.index,
                y=data1[col], name=col) for col in data1.columns]
            
            the_graph['graph1'] = dataGraph(title1,trace)
        else:
            the_graph['graph1'] = emptyGraph(title1)

    # plot combination graph
    if query2 != None:
        timeout = 0
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list2, cat=0, timeframe=daterange, geo='', gprop='')
        try:
            data2 = pytrends.interest_over_time()
        except:
            print("Google Trend down!")
            timeout = 1
        
        if timeout == 1:
            the_graph['graph2'] = emptyGraph(title2)
        else:
            if not data2.empty:
                data2 = data2.drop(labels=['isPartial'], axis='columns')

                trace = [go.Scatter(
                    x=data2.index,
                    y=data2[col], line=dict(color='#00FF00', width=2), name=col) for col in data2.columns]

                the_graph['graph2'] = dataGraph(title2,trace)
            else:
                the_graph['graph2'] = emptyGraph(title2)

    return the_graph

def dataGraph(title,trace):
    fig = go.Figure(data=trace)
    fig.update_layout(
        title={
            'text': title,
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
    
    return plot(fig, output_type='div')

def emptyGraph(title):
    fig = go.Figure(data=[])
    fig.update_layout(
        title={
            'text': title,
        },
        autosize=False,
        width=1000,
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(gridcolor='black', gridwidth=0.5)
    
    return plot(fig, output_type='div')