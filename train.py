import dash

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

import plotly.io as pio

from dashserve import JupyterDash


def main():
  external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
  app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
  # df = pd.DataFrame({
  #   "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
  #   "Amount": [4, 1, 2, 2, 4, 5],
  #   "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
  # })

  # fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

  # pio.write_json(fig, 'fig.json')

  # layout = html.Div(children=[
  #   html.H1(children='Hello OLOF'),
  #   html.Div(id='example-graph-wrapper'),
  #   dcc.Interval(
  #     id='interval-component',
  #     interval=1 * 1000,  # in milliseconds
  #     n_intervals=0)
  # ])

  # @app.callback(Output('example-graph-wrapper', 'children'),
  #               [Input('interval-component', 'n_intervals')])
  # def update_metrics(n):
  #   print(n)
  #   fig = readfig()
  #   return dcc.Graph(id='example-graph', figure=fig)

  layout = html.Div([html.H1("exp2")])
  app.layout = layout

  # app.save('app.dash')
  # app.save('exp1.lumi')
  app.save('exp2.lumi')


class LumiLogger:
  def __init__(self):
    pass


if __name__ == '__main__':
  main()
