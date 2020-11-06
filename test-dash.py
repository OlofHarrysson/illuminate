import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput
from dash.dependencies import MATCH, ALL
import dash


def serve_layout(app):
  div1_id = dict(type='controller', id='div1', index='hej1')
  div2_id = dict(type='controller', id='div2', index='hej2')
  div3_id = dict(type='controller', id='div3')
  layout = html.Div([
    html.H1('HEJ'),
    html.Div('DIV1', id='div1'),
    html.Div('DIV2', id='div2'),
    html.Div('DIV3', id='div3'),
    dcc.Slider(id=div1_id, min=0, max=1, step=0.01),
    dcc.Slider(id=div2_id, min=0, max=1, step=0.01),
    dcc.Slider(id=div3_id, min=0, max=1, step=0.01),
  ])
  return layout


def init_callbacks(app):
  @app.callback(
    Output('div1', 'children'),
    Input({
      'type': 'controller',
      'id': ALL,
      'index': ALL,
    }, 'value'),
  )
  def line_smooth(values):
    ctx = dash.callback_context
    print(ctx.outputs_list)
    # print(dir(ctx))
    # print(output_id)
    print(values)
    return values


def main():
  app = Dash(__name__, prevent_initial_callbacks=True)
  app.layout = serve_layout(app)
  init_callbacks(app)
  print('STARTING SERVER')
  app.run_server(debug=True)


if __name__ == '__main__':
  main()

# CURRENT SOLUTION ™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™™
# One callback per output graph.
# Bring in all controllers
# Find output-id via dash.callback_context. Find triggered control via dash.callback_context
# Use output-id to find connected controllers. Select all values from controller-inputs.
# Return no_update if triggered control isn't connected to graph
# Lookup functions for graph-id, put in controller-values and data into functions

main_info = {
  'scatter1-graph': [{
    'function': line_smooth,
    'func-args': [plotly_fig, 'controller.smoother'],
  }],
  'scatter1-graph': [{
    'function': time_control,
    'func-args': [plotly_fig, 'controller.time'],
  }],
}
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# One callback per output graph.
# From all controllers select the ones connected to the graph.
# Can also bring in all controls and select inside callback function?
# Bring in MATCH state with ids, id is type='controller' and id='line-smoother' which is unique.
# Then use controller id to find functions connected to controller?

# Other way. But this way will make it hard to add user functions AFTER. But maybe thats already fucked since callbacks for an element are shared
# ctrl1_id = {
#   'type': 'controller',
#   'scatter1-graph': 1,
#   'scatter2-graph': 0, # Can skip the zero ones?
#   'scatter3-graph': 1,
#   'callb-func': {}
# }
# What if two controllers are connected to the same graphs?
# Input(
#   {
#   'type': 'controller',
#   'scatter1-graph': 1,
#   'scatter2-graph': 0,
#   'scatter3-graph': 1,
#   },
#   'value'),
# State(
#   {
#   'scatter1-graph': 1,
#   'scatter2-graph': 0,
#   'scatter3-graph': 1,
#   },
#   'id'),

#  That would then come in as (control_values, control_funcs, fig).
# for value, func in zip(values, control_funcs):
#   fig = func(value, fig)
# This doesn't allow us to combine e.g. two control values into one control_func

# For a fig, define callback. Callback ~= control input values -> functions

# This dict can be shared amongst every callback.
# When callback fires, get the callback-info via graph-id from masterdict.
#
# {'graph-id': {
#   smooth_line: ['slider1-id', 'slider2-id']
#   # 'functions': [smooth_line, otherfunc],
#   # 'func_args':
# }}
# {smooth_line: ['fig', 'slider1-id', 'slider2-id']}
# def smooth_line(fig, slider1_value, slider2_value)
