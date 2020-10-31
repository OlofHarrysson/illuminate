from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput
from dash.dependencies import MATCH, ALL


def init_callbacks(app):
  @app.callback(
    Output('sidebar', 'className'),
    Output('content-container', 'className'),
    Input('sidebar-toggle', 'n_clicks'),
    State('sidebar', 'className'),
  )
  def toggle_classname(n, classname):
    # TODO: Make it collapsable some other way?
    if 'collapsed' in classname:
      classname = classname.replace('collapsed', '')
      classname2 = ''
    else:
      classname = ' '.join([classname, 'collapsed'])
      classname2 = 'expanded-content'
    return classname, classname2

  @app.callback(
    Output({
      'type': 'card-view',
      'views': ALL
    }, 'className'),
    # Input({
    #   'type': 'card-button',
    #   'index': ALL
    # }, 'n_clicks_timestamp'),
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
        actives.append('inactive')

    return actives


# TODO
def find_experiments():
  paths = list(Path('').glob('**/meta.lumi.json'))
  options = [dict(label=p.name, value=p.name) for p in paths]

  dropdown = dcc.Dropdown(id='demo-dropdown', options=options)
  return dropdown, paths
