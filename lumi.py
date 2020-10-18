import dash

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.io as pio
from dash.dependencies import Input, Output
from dashserve.server import SerializedDashServer
from dashserve.serializer import DashAppSerializer

import datetime
from pathlib import Path


def readfig():
  fig = pio.read_json('fig.json')
  return fig


def find_experiments():
  paths = list(Path('').glob('**/*.lumi'))
  options = [dict(label=p.name, value=p.name) for p in paths]

  dropdown = dcc.Dropdown(id='demo-dropdown', options=options)
  return dropdown, paths


def serve_layout():
  dropdown, exps = find_experiments()

  print("SERVING LAYOUT")
  layout = html.Div(children=[
    html.H1(children='Welcome to Lumi'),
    html.H1('The time is: ' + str(datetime.datetime.now())),
    html.H1('Experiments: ' + str(exps)),
    dropdown,
    html.Div(id='dd-output-container'),
  ])

  # exp_app = SerializedDashServer.from_file(exps[0]).serialized_app
  # serializer = DashAppSerializer()
  # exp_app = serializer.deserialize(exp_app)

  # layout = html.Div([layout, exp_app.layout])
  return layout


def init_callbacks(app):
  @app.callback(dash.dependencies.Output('dd-output-container', 'children'),
                [dash.dependencies.Input('demo-dropdown', 'value')])
  def update_output(value):
    if value is None:
      return html.Div('EMPTY')
    exp_app = SerializedDashServer.from_file(value).serialized_app
    serializer = DashAppSerializer()
    exp_app = serializer.deserialize(exp_app)
    print(dir(exp_app))
    print(exp_app.callback)
    print(exp_app.callback_map)
    print(exp_app.clientside_callback)
    return exp_app.layout


def main():
  # server = SerializedDashServer.from_file('app.dash')
  # server.run(host='localhost', port=8050)

  external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
  app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
  app.layout = serve_layout
  print("STARTING SERVER")
  init_callbacks(app)
  app.run_server(debug=True)


if __name__ == '__main__':
  main()

# Vision 1
# Starts lumi --path=outputdir
# Visit browser and see "empty" server
# Starts train.py, send all info
# Visit browser, see new experiment there with all data
# Starts new train.py, all that information also shows up
# Problem is that if we serialize the dash-app, that correspond to one experiment and we can only see one exp at a time. Maybe we can serialize only the callbacks but if the callbacks are dependent on external functions those also need to be serialized which wont work.

# Vision 2
# Log data and text-descriptions from train.py
# Interpret data, create callbacks etc and start server
# Check for changes in .lumi files. Add new data / callacks. Restart server if nessessary
# Allow user to start server with custom callbacks.

# Facts: Need to restart dash-server if new callbacks are logged
