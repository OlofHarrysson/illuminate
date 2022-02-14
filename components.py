import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def create_edit_view(layout, current_view):
  view_ids = layout.keys()
  options = [dict(label=win_id, value=win_id) for win_id in view_ids]
  view_dropdown = html.Div(
    dcc.Dropdown(
      options=options,
      clearable=False,
      # id='view-dropdown',
      value='everything',
    ),
    className='nav-item',
  )

  graph_ids = [
    dict(label=ele['i'], value=ele['i']) for ele in layout[current_view]
  ]
  graphs = dcc.Dropdown(
    options=graph_ids,
    multi=True,
    value=[graph_id['value'] for graph_id in graph_ids],
    id='edit-views-selected-graphs',
  )

  save_button = dbc.Button('Save', color='primary', id='save-view-button')

  return dbc.Card(
    [
      dbc.CardHeader('Edit Views'),
      view_dropdown,
      graphs,
      save_button,
    ],
    body=True,
  )
