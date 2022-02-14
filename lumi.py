# import dash
import dash_responsive_grid_layout as drgl
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
from factories import CallbackFactory, FunctionFactory, ControlFactory, create_callback_function
import components


def make_view_card(content, title, fig_id, view_ids):

  modal_control = html.A(
    html.I(className='fas fa-expand fa-lg control-item'),
    href='#',
    id=dict(type='controller-modal', id=fig_id),
  )
  controls = html.Div(
    [
      modal_control,
      html.I(className='fas fa-arrows-alt fa-lg control-item draggable'),
    ],
    className='graph-controls',
  )

  return dbc.Card(
    [
      content,
      controls,
    ],
    body=True,
    className='view-card',
    id=f'{fig_id}-card',
    # id=f"{' '.join(view_ids)} {fig_id}",
  )


def navbar_view(win_ids):
  options = [dict(label=win_id, value=win_id) for win_id in win_ids]
  view_dropdown = html.Div(
    dcc.Dropdown(
      options=options,
      clearable=False,
      id='view-dropdown',
      value='everything',
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

  new_view_button = dbc.Button(
    "Edit Views",
    id="edit-views-button",
    className='nav-item',
  )
  navbar = html.Nav(
    [
      logo,
      new_view_button,
      view_dropdown,
    ],
    id='header-navbar',
  )

  return navbar


def sidebar_view(raw_controls):
  collapse = html.Li(
    html.A(
      html.I(className='fas fa-angle-double-right fa-5x'),
      href='#',
      className='nav-link',
      id='sidebar-toggle',
    ))

  controls = [collapse]
  for control in raw_controls:
    c = html.Li(control, className='nav-item')
    controls.append(c)

  controls_list = html.Ul(controls, className='sidebar-list')
  return html.Nav(controls_list, className='sidebar', id='sidebar')


def content_view(content, view_ids):
  n_cols = 12
  cols = {'lg': n_cols}
  breakpoints = {'lg': 3200}

  layouts = []
  width = 4
  n_graphs_x = n_cols / width
  for idx, ele in enumerate(content):
    ele_id = ele.id
    height = width * 2

    x = idx % n_graphs_x * width
    y = idx // n_graphs_x * height
    item = dict(i=ele_id, x=x, y=y, w=width, h=height)
    layouts.append(item)

  layout_data = {wid: layouts for wid in view_ids}
  store = dcc.Store(data=layout_data, id='layout-store')
  # store = dcc.Store(data=layout_data, id='layout-store', storage_type='local')

  layouts = {'lg': layouts}
  grid_layout = drgl.ResponsiveGridLayout(
    content,
    id='grid-layout',
    cols=cols,
    layouts=layouts,
    breakpoints=breakpoints,
    draggableHandle='.draggable',
    rowHeight=50,
    autoSize=True,
    margin=[0, 0, 0, 0],
    # width=500,
  )
  return html.Div([
    grid_layout,
    store,
  ], id='content-container'), layout_data


def serve_layout(app, index, controls):
  content = []
  all_view_ids = set()
  for name, item in index.items():
    fig = item['graph']

    # Add layout
    view_ids = item['view_ids']
    all_view_ids.update(view_ids)
    fig_id = f'{name}'
    print(fig_id)

    graph = dcc.Graph(id=fig_id, figure=fig)
    card = make_view_card(graph, name, fig_id, view_ids)
    content.append(card)

    if item['callback_list']:
      callb_args = CallbackFactory.get_item(name)
      callb = app.callback(callb_args)
      func = create_callback_function(index)
      callb(func)

  graph_modal = dbc.Modal(
    [
      dcc.Graph(id='expanded-graph'),
    ],
    id='expanded-graph-modal',
    size='xl',
  )

  content, layout = content_view(content, all_view_ids)
  modal_placeholder = components.create_edit_view(layout, 'everything')
  edit_views_modal = dbc.Modal(
    modal_placeholder,
    id='edit-views-modal',
    size='xl',
  )

  print('SERVING LAYOUT')
  layout = html.Div(children=[
    sidebar_view(controls),
    navbar_view(all_view_ids),
    content,
    graph_modal,
    edit_views_modal,
  ])

  return layout


def create_index(lumi_path):
  with open(lumi_path) as f:
    index = json.load(f)

  main = {}
  for jitem in index.values():
    ele_id = jitem['ele_id']
    fig = pio.read_json(jitem.pop('data_path'))
    fig.update_layout(plotly_styles.base_layout())
    fig.update_layout(
      title={
        'text': ele_id.title(),
        'x': 0.5,
        'yanchor': 'top',
        'font': {
          'size': 22,
        },
      })

    jitem['figure'] = fig
    # fig = 'fig'  # TODO

    callback_list = []
    for callback_id in jitem['callback_function_map']:
      func = FunctionFactory.get_item(callback_id)
      func_args = [fig, ControlFactory.get_id(callback_id)]
      callb_item = dict(function=func, function_args=func_args)
      callback_list.append(callb_item)

    item = dict(graph=fig,
                callback_list=callback_list,
                view_ids=jitem['view_ids'])
    main[ele_id] = item

  return main


def main():
  app = Dash(__name__,
             external_stylesheets=[dbc.themes.BOOTSTRAP],
             prevent_initial_callbacks=True)

  lumi_path = 'output/exp/meta.lumi.json'
  index = create_index(lumi_path)

  # Get the controllers that are used.
  controls = ControlFactory.get_controllers()

  app.layout = serve_layout(app, index, controls)
  init_callbacks(app, index)
  print('STARTING SERVER')
  app.run_server(debug=True)


if __name__ == '__main__':
  main()

# TODO: Specify layout within a view. Size of cards, position etc. Preferably via a GUI
