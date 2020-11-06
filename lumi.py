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


def make_view_card(content, title, fig_id, view_ids):
  header = html.Div(
    [
      html.H4(title, className='draggable'),
      html.I(className='fas fa-pizza-slice fa-2x'),
    ],
    className='card-header',
  )

  controls = html.Div(
    [
      html.I(className='fas fa-pizza-slice fa-lg control-item'),
      html.I(className='fas fa-arrows-alt fa-lg control-item draggable'),
      # html.Span(html.I(className='fas fa-pizza-slice fa-2x ontop')),
      # html.Span(html.I(className='fas fa-pizza-slice fa-2x ontop')),
    ],
    className='graph-controls',
  )

  resize = html.Span(
    html.I(className='fas fa-expand-arrows-alt draggable-resize'),
    className='react-resizable-handle',
  )

  content = html.Div(content, className='graph-wrapper')

  return dbc.Card(
    [
      content,
      controls,
      # header,
      # resize,
    ],
    body=True,
    className='view-card',
    id=f"{' '.join(view_ids)} {fig_id}",
    # id={
    #   'type': 'card-view',
    #   # 'graph-id': fig_id, # TODO: Callback doesnt fire with this
    #   'views': f"{' '.join(view_ids)} {fig_id}"
    # },
  )


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


def content_view(content):
  cols = {'lg': 12}
  breakpoints = {'lg': 2200}

  layouts = []
  width = 4
  for idx, ele in enumerate(content):
    item = dict(i=ele.id, x=idx * width, y=0, w=width, h=width * 2)
    layouts.append(item)
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
  return html.Div(grid_layout, id='content-container')
  # return html.Div(content, id='content-container')


def serve_layout(app, index, controls):
  content = []
  all_view_ids = set()
  for name, item in index.items():
    fig = item['graph']

    # Add layout
    view_ids = item['view_ids']
    all_view_ids.update(view_ids)
    fig_id = f'{name}'

    # style = {'height': '100%'}
    # graph = dcc.Graph(id=fig_id, figure=fig, style=style)
    graph = dcc.Graph(id=fig_id, figure=fig)
    card = make_view_card(graph, name, fig_id, view_ids)
    content.append(card)

    if item['callback_list']:
      callb_args = CallbackFactory.get_item(name)
      callb = app.callback(callb_args)
      func = create_callback_function(index)
      callb(func)

  print('SERVING LAYOUT')
  layout = html.Div(children=[
    sidebar_view(controls),
    navbar_view(all_view_ids),
    content_view(content),
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
    # fig.update_layout(title=dict(text=ele_id, xanchor='center'))
    fig.update_layout(title={
      'text': ele_id.title(),
      'x': 0.5,
      'xanchor': 'center',
    })

    jitem['figure'] = fig
    # fig.update_layout(autosize=True)
    # fig.update_layout(autosize=False, width=200, height=200)
    # fig.update_layout(autosize=True, width=500, height=500)
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
  init_callbacks(app)
  print('STARTING SERVER')
  app.run_server(debug=True)


if __name__ == '__main__':
  main()

# TODO: Specify layout within a view. Size of cards, position etc. Preferably via a GUI
