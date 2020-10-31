# import dash

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
# from dash.dependencies import Input, Output, State
from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput
from collections import defaultdict
import pandas as pd
import json
import copy
import datetime
from pathlib import Path
import numpy as np
from callbacks import init_callbacks
import plotly_styles
from factories import CallbackFactory, FunctionFactory, ControlFactory


def make_view_card(content, title, fig_id, win_ids):
  return dbc.Card(
    [
      html.H4(title, className='card-title'),
      html.Div(content),
    ],
    body=True,
    id={
      'type': 'card-view',
      # 'graph-id': fig_id, # TODO: Callback doesnt fire with this
      'views': f"{' '.join(win_ids)} {fig_id}"
    },
    className='',
  )


# TODO: Click on view, find all cards,
# Goal, set either active/not active on the cards.
# Need to get information of what views a card is connected to


def navbar_view(win_ids):
  options = [dict(label=win_id, value=win_id) for win_id in win_ids]
  view_dropdown = html.Div(
    dcc.Dropdown(
      options=options,
      placeholder="Select a view",
      clearable=False,
      id='view-dropdown',
    ),
    className='nav-item',
  )

  logo = html.Div(
    [
      html.I(className='fas fa-pizza-slice fa-3x'),
      html.Span('Lumi', className='nav-span'),
    ],
    className='nav-item',
  )
  navbar = html.Nav(
    [
      logo,
      view_dropdown,
    ],
    id='header-navbar',
  )

  return navbar


def sidebar_view(controls):
  # TODO: Allow controls outside of sidebar?
  collapse = html.A(
    html.I(className='fas fa-angle-double-right fa-5x'),
    href='#',
    className='nav-link',
    id='sidebar-toggle',
  )

  controls = [html.Li(c, className='nav-item') for c in controls.values()]
  controls.insert(0, collapse)

  controls_list = html.Ul(controls, className='sidebar-list')
  return html.Nav(controls_list, className='sidebar', id='sidebar')


def content_view(content):
  content_ele = html.Div(content)
  return html.Div(content_ele, id='content-container')


def serve_layout(app, index):
  content = []
  controls = {}
  window_ids = set()
  for _, item in index.items():
    fig = item['figure']

    # Add layout
    name = item['ele_id']
    win_ids = item['window_id']
    window_ids.update(win_ids)
    fig_id = f'{name}-graph'
    card = make_view_card(dcc.Graph(id=fig_id, figure=fig), name, fig_id,
                          win_ids)
    content.append(card)

    if 'callback_function' in item:
      store_id = f'{name}-store'
      content.append(dcc.Store(id=store_id, data=fig))
      callb_args = item['callback_args']
      func = item['callback_function']
      callb = app.callback(callb_args)
      callb(func)

      control_id, control = item['control']
      controls[control_id] = control

  print('SERVING LAYOUT')
  layout = html.Div(children=[
    sidebar_view(controls),
    navbar_view(window_ids),
    content_view(content),
    html.Div(id='todo')
  ])

  return layout


def create_index(lumi_path):
  with open(lumi_path) as f:
    index = json.load(f)

  for jitem in index.values():
    fig = pio.read_json(jitem.pop('data_path'))
    fig.update_layout(plotly_styles.base_layout())
    fig.update_layout(autosize=False, width=1200, height=200)
    jitem['figure'] = fig
    ele_id = jitem['ele_id']
    win_ids = jitem['window_id']

    if 'callback_function_map' in jitem:
      callback_id = jitem['callback_function_map']
      callb_args = CallbackFactory.get_item(ele_id, callback_id)
      control_id, control = ControlFactory.get_item(callback_id)
      cb_func = FunctionFactory.get_item(callback_id)
      jitem['callback_args'] = callb_args
      jitem['control'] = (control_id, control)
      jitem['callback_function'] = cb_func

  return index


def user_add_index(index):
  def double(smooth, fig):
    fig['data'][0]['y'] = np.array(fig['data'][0]['y']) * smooth
    return fig

  scatter2 = copy.deepcopy(index['scatter2'])
  ele_id = 'scatter5'
  scatter2['ele_id'] = ele_id
  win_id = scatter2['window_id'][0]
  scatter2['window_id'] = [win_id]

  scatter2['callback_function'] = double
  callback_args = scatter2['callback_args'][win_id]
  callback_args[0] = Output(f'{ele_id}-{win_id}-graph', 'figure')
  callback_args[-1] = State(f'{ele_id}-{win_id}-store', 'data')
  scatter2['callback_args'] = {win_id: callback_args}
  index[ele_id] = scatter2

  return index


def main():
  app = Dash(__name__,
             external_stylesheets=[dbc.themes.BOOTSTRAP],
             prevent_initial_callbacks=True)

  lumi_path = 'output/exp/meta.lumi.json'
  index = create_index(lumi_path)
  # index = user_add_index(index)

  app.layout = serve_layout(app, index)
  init_callbacks(app)
  print('STARTING SERVER')
  app.run_server(debug=True)


if __name__ == '__main__':
  main()

# TODO: Allow to add elements to layout e.g. controllers
# TODO: How to solve multiple controllers for one element?
