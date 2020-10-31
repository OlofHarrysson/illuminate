from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput
from dash.dependencies import MATCH, ALL


def init_callbacks(app):
  @app.callback(
    Output('sidebar', 'className'),
    Output('content-container', 'className'),
    Output({
      'type': 'controller',
      'id': ALL
    }, 'className'),
    Input('sidebar-toggle', 'n_clicks'),
    State('sidebar', 'className'),
    State({
      'type': 'controller',
      'id': ALL
    }, 'className'),
  )
  def toggle_classname(n, classname, ctrl_classname):
    # TODO: Make it collapsable some other way?
    if 'collapsed' in classname:
      classname = classname.replace('collapsed', '')
      classname2 = ''
      ctrl_classname = ['active-control'] * len(ctrl_classname)
    else:
      classname = ' '.join([classname, 'collapsed'])
      classname2 = 'expanded-content'
      ctrl_classname = ['inactive-control'] * len(ctrl_classname)
    return classname, classname2, ctrl_classname

  @app.callback(
    Output({
      'type': 'card-view',
      'views': ALL
    }, 'className'),
    Input('view-dropdown', 'value'),
    State({
      'type': 'card-button',
      'index': ALL
    }, 'id'),
    State({
      'type': 'card-view',
      'views': ALL
    }, 'id'),
  )
  def toggle_classname(active_view, view_ids, graph_ids):
    actives = []
    for graph_id in graph_ids:
      if active_view in graph_id['views']:
        actives.append('')
      else:
        actives.append('inactive-graph')

    return actives


# TODO
def find_experiments():
  paths = list(Path('').glob('**/meta.lumi.json'))
  options = [dict(label=p.name, value=p.name) for p in paths]

  dropdown = dcc.Dropdown(id='demo-dropdown', options=options)
  return dropdown, paths
