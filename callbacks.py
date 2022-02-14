from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput
from dash.dependencies import MATCH, ALL
import dash
import json
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import components


def init_callbacks(app, index):
  @app.callback(
    Output('sidebar', 'className'),
    Output('content-container', 'className'),
    Output({
      'type': 'controller-container',
      'id': ALL
    }, 'className'),
    Input('sidebar-toggle', 'n_clicks'),
    State('sidebar', 'className'),
    State({
      'type': 'controller-container',
      'id': ALL
    }, 'className'),
  )
  def toggle_classname(n, classname, ctrl_classname):
    # TODO: Make it collapsable some other way?
    # TODO: Grid content doesnt expand/shrink on update. Need a way to trigger its redraw considering that it calculates height/width for things
    if 'collapsed' in classname:
      classname = classname.replace('collapsed', '')
      classname2 = ''
      ctrl_classname = ['active-control'] * len(ctrl_classname)
    else:
      classname = ' '.join([classname, 'collapsed'])
      classname2 = 'expanded-content'
      ctrl_classname = ['inactive-control'] * len(ctrl_classname)
    return classname, classname2, ctrl_classname

  # @app.callback(
  #   Output({
  #     'type': 'card-view',
  #     'views': ALL
  #   }, 'className'),
  #   Input('view-dropdown', 'value'),
  #   State({
  #     'type': 'card-button',
  #     'index': ALL
  #   }, 'id'),
  #   State({
  #     'type': 'card-view',
  #     'views': ALL
  #   }, 'id'),
  # )
  # def toggle_classname(active_view, view_ids, graph_ids):
  #   actives = []
  #   for graph_id in graph_ids:
  #     if active_view in graph_id['views']:
  #       actives.append('')
  #     else:
  #       actives.append('inactive-graph')

  #   return actives

  @app.callback(
    Output('grid-layout', 'layouts'),
    Input('view-dropdown', 'value'),
    State('layout-store', 'data'),
    prevent_initial_call=False,
  )
  def pack_graphs(view_value, in_layouts):
    layout = in_layouts[view_value]

    # TODO: Some smarter packing. This is just reset.
    # Like sort on y & x. Then go from first, add and then change second x+y (or just x?) to the sum of previous ones
    out_layout = []
    for ele in layout:
      item = dict(ele)
      # TODO: Translate off things? Or solve via the edit views button
      # if view_value not in ele['i']:
      #   item['y'] = -10000

      out_layout.append(item)

    return dict(lg=out_layout)

  @app.callback(
    Output('layout-store', 'data'),
    Input('grid-layout', 'layouts'),
    Input('save-view-button', 'n_clicks'),
    State('layout-store', 'data'),
    State('view-dropdown', 'value'),
    State('edit-views-selected-graphs', 'value'),
  )
  def update_layout(in_layout, n_clicks, stored_layout, view_value,
                    selected_graphs):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print(trigger)
    if trigger == 'save-view-button':
      print(selected_graphs)
      pass todo save new view into layout

    stored_layout[view_value] = in_layout['lg']
    return stored_layout

  @app.callback(
    Output('expanded-graph-modal', 'is_open'),
    Output('expanded-graph', 'figure'),
    Input({
      'type': 'controller-modal',
      'id': ALL
    }, 'n_clicks'),
    State({
      'type': 'controller',
      'id': ALL,
    }, 'value'),
    State({
      'type': 'controller',
      'id': ALL,
    }, 'id'),
  )
  def toggle_modal(clicks, values, ids):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    graph_id = json.loads(trigger)['id']
    controller_group = index[graph_id]

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

    return True, fig_copy

  @app.callback(
    Output('edit-views-modal', 'is_open'),
    Output('edit-views-modal', 'children'),
    Input('edit-views-button', 'n_clicks'),
    State('layout-store', 'data'),
    State('view-dropdown', 'value'),
  )
  def update_layout(n_clicks, layout, current_view):
    modal_content = components.create_edit_view(layout, current_view)
    return True, modal_content


# TODO
def find_experiments():
  paths = list(Path('').glob('**/meta.lumi.json'))
  options = [dict(label=p.name, value=p.name) for p in paths]

  dropdown = dcc.Dropdown(id='demo-dropdown', options=options)
  return dropdown, paths
