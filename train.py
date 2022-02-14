import json
import pandas as pd
import time
import numpy as np
from pathlib import Path
import plotly.io as pio
import plotly.express as px

from datetime import datetime


def main():
  outdir = Path('output/exp')
  logger = LumiLogger(outdir)
  n_points = 500
  x = np.linspace(0, n_points - 1, n_points)
  y = np.random.random(n_points)

  logger.log_line(x, y, 'scatter1')
  logger.log_line(x, y, 'scatter2', ['images'])
  logger.log_line(x, y, 'scatter3', ['other', 'images'])
  logger.log_line(x, y, 'scatter4', ['other', 'images'])

  # TODO: Remove the ability to log to view. That should be handeled in the app/server

  # Logger(exp_type/base, exp_id)
  # Then we can create/edit layout in app and save the layout to somewhere. If the experiement name is known, we can load that same layout.
  # Or can we simply make an educated guess if two experiments are the same given that they have the same metadata-graphs?


class LumiLogger:
  def __init__(self, outdir, env_id=None):
    if env_id is None:
      env_id = time.time()

    outdir.mkdir(exist_ok=True)
    self.outdir = outdir
    self.index_file = outdir / 'meta.lumi.json'
    self.index = {}

  def update_index_file(self, entry):
    self.index[entry['ele_id']] = entry
    with open(self.index_file, 'w') as f:
      json.dump(self.index, f, indent=2)
    # self.index = self.index.append(row, ignore_index=True)
    # self.index.to_csv(self.index_file, index=False)

  def log_line(self, x, y, ele_id, views=None):
    if views is None:
      views = []
    views.insert(0, 'everything')

    df = pd.DataFrame(dict(y=y))
    path = self.outdir / f'{ele_id}.json'
    # df.to_json(path)

    fig = px.line(df)
    pio.write_json(fig, str(path))

    row = dict(
      ele_id=ele_id,
      view_ids=views,
      data_path=str(path),
      last_modified=str(datetime.now()),
      # callback_function_map='lumi-smoothing',
      callback_function_map=['lumi-smoothing', 'lumi-time-controller'],
    )
    if ele_id == 'scatter1':
      row['callback_function_map'] = []

    self.update_index_file(row)


if __name__ == '__main__':
  main()

# TODO: index data specification
# CSV > json?
# Ele-id, graph-type, last-modified, function (e.g. smoothing), controller-element
