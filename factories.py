import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import MATCH, ALL
import dash
import math

import plotly.graph_objects as go


def line_smooth(fig, smooth):
  smooth = pow(smooth, 0.3)
  smooth = np.clip(1 - smooth, 1e-10, 1)
  for trace in fig.data:
    trace.y = tuple(pd.Series(trace.y).ewm(alpha=smooth, adjust=False).mean())


def time_cutoff(fig, values):
  min_val, max_val = values
  for trace in fig.data:
    start = int(min_val * len(trace.x))
    stop = int(max_val * len(trace.x))
    trace.x = trace.x[start:stop]
    trace.y = trace.y[start:stop]


def make_controller_card(control, title):
  container_id = dict(type='controller-container',
                      id=f"{control.id['id']}-container")

  return html.Div(
    dbc.Card(
      [
        html.H4(title, className='card-title'),
        html.Div(control),
      ],
      body=True,
      className='dark',
    ),
    id=container_id,
  )


class FunctionFactory:
  func_map = {
    'lumi-smoothing': line_smooth,
    'lumi-time-controller': time_cutoff,
  }

  @classmethod
  def get_item(cls, ele_id):
    return cls.func_map[ele_id]


class ControlFactory:
  # smoother_id = 'lumi-smoothing-controller'
  smoother_id = dict(type='controller', id='lumi-smoothing-controller')
  smoother = dcc.Slider(id=smoother_id, min=0, max=1, step=0.01, value=0)
  smoother_ele = make_controller_card(smoother, 'Smoother')

  # time_control_id = 'lumi-time-controller'
  time_control_id = dict(type='controller', id='lumi-time-controller')
  time_control = dcc.RangeSlider(id=time_control_id,
                                 min=0,
                                 max=1,
                                 step=0.01,
                                 value=[0, 1])
  time_control_ele = make_controller_card(time_control, 'Time')

  controls_map = {
    'lumi-smoothing': smoother_ele,
    'lumi-time-controller': time_control_ele,
  }

  callb_map = {
    'lumi-smoothing': smoother_id,
    'lumi-time-controller': time_control_id,
  }

  @classmethod
  def get_controllers(cls):
    return list(cls.controls_map.values())

  @classmethod
  def get_item(cls, callb_id):
    return cls.controls_map[callb_id]

  @classmethod
  def get_id(cls, callb_id):
    return cls.callb_map[callb_id]


class CallbackFactory:
  @classmethod
  def get_item(cls, ele_id):
    callback_args = [
      Output(ele_id, 'figure'),
      Input({
        'type': 'controller',
        'id': ALL,
      }, 'value'),
      State({
        'type': 'controller',
        'id': ALL,
      }, 'id'),
    ]

    return callback_args


def create_callback_function(index):
  def callback_function(values, ids):
    ctx = dash.callback_context
    out_id = ctx.outputs_list['id']
    controller_group = index[out_id]
    if not controller_group:
      return dash.no_update

    ids = {id_dict['id']: idx for idx, id_dict in enumerate(ids)}
    fig_copy = go.Figure(controller_group['graph'])

    for func_info in controller_group['callback_list']:
      func_args = []
      for func_arg in func_info['function_args']:
        if isinstance(func_arg, dict):
          controller_idx = ids[func_arg['id']]
          func_arg = values[controller_idx]
        elif func_arg is controller_group['graph']:
          func_arg = fig_copy
        func_args.append(func_arg)

      func_info['function'](*func_args)

    return fig_copy

  return callback_function


# main_info = {
#   'scatter1-graph': [
#     {
#       'function': line_smooth,
#       'func-args': [plotly_fig, 'controller.smoother'],
#     },
#     {
#       'function': time_control,
#       'func-args': [plotly_fig, 'controller.time'],
#     },
#   ],
#   'scatter2-graph': [{
#     'function': time_control,
#     'func-args': [plotly_fig, 'controller.time'],
#   }],
# }
