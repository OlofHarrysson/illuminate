import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput
import dash_core_components as dcc
import dash_html_components as html


def line_smooth(smooth, fig):
  smooth = np.clip(1 - smooth, 1e-10, 1)
  df = pd.Series(fig['data'][0]['y']).ewm(alpha=smooth).mean()
  fig['data'][0]['y'] = df.to_numpy()
  return fig


def make_controller_card(content, title):
  return dbc.Card(
    [
      html.H4(title, className='card-title'),
      html.Div(content),
    ],
    body=True,
    className='dark',
  )


class FunctionFactory:
  func_map = {
    'lumi-smoothing': line_smooth,
  }

  @classmethod
  def get_item(cls, ele_id):
    return cls.func_map[ele_id]


class ControlFactory:
  smoother_id = 'lumi-smoothing-controller'
  smoother = dcc.Slider(id=smoother_id, min=0, max=1, step=0.01)
  smoother_ele = make_controller_card(smoother, 'Smoother')

  time_control_id = 'lumi-time-controller'
  time_control = dcc.Slider(id=time_control_id, min=0, max=1, step=0.01)
  time_control_ele = make_controller_card(time_control, 'Time')

  controls_map = {
    'lumi-smoothing': smoother_ele,
    'lumi-time-controller': time_control_id,
  }

  callb_map = {
    'lumi-smoothing': smoother_id,
    'lumi-time-controller': time_control_ele,
  }

  @classmethod
  def get_item(cls, callb_id):
    control = cls.controls_map[callb_id]
    control_id = cls.get_id(callb_id)
    return control_id, control

  @classmethod
  def get_id(cls, callb_id):
    return cls.callb_map[callb_id]


class CallbackFactory:
  @classmethod
  def get_item(cls, ele_id, callb_id):
    control_id = ControlFactory.get_id(callb_id)
    callback_args = [
      Output(f'{ele_id}-graph', 'figure'),
      Input(control_id, 'value'),
      State(f'{ele_id}-store', 'data'),
    ]

    return callback_args
