# import dash

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.io as pio
# from dash.dependencies import Input, Output, State
from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput

import pandas as pd

import datetime
from pathlib import Path


def readfig(path):
  fig = pio.read_json(str(path))
  return fig


def find_experiments():
  paths = list(Path('').glob('**/meta.lumi.json'))
  options = [dict(label=p.name, value=p.name) for p in paths]

  dropdown = dcc.Dropdown(id='demo-dropdown', options=options)
  return dropdown, paths


def serve_layout(app):
  # dropdown, exps = find_experiments()
  index = pd.read_csv('output/exp/meta.lumi.csv')

  content = []
  for _, row in index.iterrows():
    fig = readfig(Path(row['data_path']))

    # Add layout and store
    name = row['ele_id']
    store_id = f'{name}-store'
    fig_id = f'{name}-fig'
    content.append(dcc.Store(id=store_id, data=fig))
    content.append(dcc.Graph(id=fig_id))

    # Add callback
    if row['callback_function'] == 'lumi.smoothing':
      callb = app.callback(
        Output(fig_id, 'figure'),
        Input('my-slider', 'value'),
        State(store_id, 'data'),
      )
      callb(line_smooth)

  print('SERVING LAYOUT')
  layout = html.Div(children=[
    html.H1(children='Welcome to Lumi'),
    html.H1('The time is: ' + str(datetime.datetime.now())),
    # html.H1('Experiments: ' + str(exps)),
    # dropdown,
    dcc.Slider(id='my-slider', min=0, max=1, step=0.01),
    html.Div(id='slider-output-container'),
    html.Div(content)
  ])

  return layout


def line_smooth(smooth, fig):
  window = int(smooth * 49) + 1

  y = fig['data'][0]['y']
  df = pd.Series(y)
  y = df.rolling(window, min_periods=1).mean()
  y = y.to_numpy()
  fig['data'][0]['y'] = y
  return fig


def main():
  external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
  app = Dash(__name__,
             external_stylesheets=external_stylesheets,
             prevent_initial_callbacks=True)
  # app.layout = serve_layout
  app.layout = serve_layout(app)
  print('STARTING SERVER')
  app.run_server(debug=True)


if __name__ == '__main__':
  main()

# Vision 1
# Starts lumi --path=outputdir
# Visit browser and see 'empty' server
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
