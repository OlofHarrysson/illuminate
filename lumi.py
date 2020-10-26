# import dash

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
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


def make_card(content, title):
  return dbc.Card(
    [
      html.H4(title, className='card-title'),
      html.Div(content),
    ],
    body=True,
  )


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
    card = make_card(dcc.Graph(id=fig_id), fig_id)
    content.append(card)

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
    navbar_view(),
    sidebar_view(),
    content_view(content),
    # html.H1('Experiments: ' + str(exps)),
    # dropdown,
  ])

  return layout


def navbar_view():
  return dbc.NavbarSimple(
    brand="Lumi",
    brand_href="#",
    color="primary",
    dark=True,
    id='navbar',
  )


def sidebar_view():
  collapse_button = html.Button(
    html.Span("Collapse"),
    id="sidebar-toggle",
  )
  slider_ele = html.Div(
    [html.H3('Smoother'),
     dcc.Slider(id='my-slider', min=0, max=1, step=0.01)])

  return html.Nav(
    [
      html.Ul(
        [
          html.Li(collapse_button, className='nav-item'),
          html.Li(slider_ele, className='nav-item'),
        ],
        className='navbar-nav',
      ),
    ],
    className='navbar',
    id="sidebar",
  )


def content_view(content):
  content_ele = html.Div(content)
  return html.Div([content_ele], id='content-container')


def line_smooth(smooth, fig):
  window = int(smooth * 49) + 1
  df = pd.Series(fig['data'][0]['y'])
  y = df.rolling(window, min_periods=1).mean()
  fig['data'][0]['y'] = y.to_numpy()
  return fig


def init_callbacks(app):
  @app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
  )
  def toggle_classname(n, classname):
    if not classname:
      return "collapsed"
    return ""


def main():
  app = Dash(__name__,
             external_stylesheets=[dbc.themes.BOOTSTRAP],
             prevent_initial_callbacks=True)
  # app.layout = serve_layout
  app.layout = serve_layout(app)
  init_callbacks(app)
  print('STARTING SERVER')
  app.run_server(debug=True)


if __name__ == '__main__':
  main()
