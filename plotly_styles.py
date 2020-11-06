import plotly.express as px
import plotly.graph_objects as go


def get_colors(n_colors):
  ''' Returns the first Plotly colors '''
  colors = px.colors.qualitative.Plotly
  return colors[:n_colors]


def base_layout():
  ''' Base layout for Plotly figures '''
  return go.Layout(
    margin=margins(),
    font=dict(size=12),
  )


def margins(margin=0, pad=0):
  ''' Spacing for Plotly figure '''
  return dict(l=margin, r=margin, t=30, b=margin, pad=pad)
