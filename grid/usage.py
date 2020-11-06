import dash_responsive_grid_layout as drgl
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import json

fig = {
  'data': [
    {
      'x': [1, 2, 3],
      'y': [4, 1, 2],
      'type': 'bar',
      'name': 'SF'
    },
    {
      'x': [1, 2, 3],
      'y': [2, 4, 5],
      'type': 'bar',
      'name': 'Montréal'
    },
  ],
  'layout': {
    'title': 'Dash Data Visualization'
  }
}

style = {'borderStyle': 'solid', 'height': '100%'}
graph_a = dcc.Graph(id='a-graph',
                    figure=fig,
                    config={'autosizable': True},
                    style=style,
                    className='titlebar')

graph_b = dcc.Graph(
  id='b-graph',
  figure=fig,
  config={
    'autosizable': True,
    'doubleClick': 'autosize',
    'frameMargins': 0,
  },
  style=style,
  className='titlebar',
)

graph_c = dcc.Graph(
  id='c-graph',
  figure=fig,
  config={
    'autosizable': True,
    'doubleClick': 'autosize',
    'frameMargins': 0,
  },
  style=style,
  className='titlebar',
)

div_d = html.Div(
  [
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
    html.H4('asodjaoisdjaiosd'),
  ],
  id='div-d',
)

app = dash.Dash('')

app.scripts.config.serve_locally = True

layouts = {
  'lg': [{
    'i': 'a-graph',
    'x': 0,
    'y': 0,
    'w': 1,
    'h': 2,
    'static': False
  }, {
    'i': 'b-graph',
    'x': 1,
    'y': 0,
    'w': 2,
    'h': 4,
    'minW': 1,
    'maxW': 3
  }, {
    'i': 'c-div',
    'x': 1,
    'y': 2,
    'w': 2,
    'h': 4,
  }, {
    'i': 'd-div',
    'x': 1,
    'y': 2,
    'w': 1,
    'h': 1,
  }]
}

cols = {'lg': 5}
breakpoints = {'lg': 1200}

a = drgl

app.layout = html.Div([
  drgl.ResponsiveGridLayout(
    [
      graph_a,
      graph_b,
      html.H1('HELLO WORLD', id='c-div', className='titlebar'),
      div_d,
    ],
    id='grid-layout',
    cols=cols,
    layouts=layouts,
    breakpoints=breakpoints,
    draggableHandle='.titlebar',
  ),  #drgl.GridLayout
  html.Div('layout-temp', id='data-node')
])  #html.Div


@app.callback(Output('data-node', 'children'),
              [Input('grid-layout', 'layouts')])
def myfunc(lay):
  print(lay)
  return json.dumps(lay)


if __name__ == '__main__':
  app.run_server(debug=True)
