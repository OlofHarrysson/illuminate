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
  n_points = 50
  x = np.linspace(0, n_points - 1, n_points)
  y = np.random.random(n_points)

  logger.log_line(x, y, 'scatter1')
  logger.log_line(x, y, 'scatter2', ['main'])
  logger.log_line(x, y, 'scatter3', ['main', 'images'])


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
      views = ['everything']

    df = pd.DataFrame(dict(y=y))
    path = self.outdir / f'{ele_id}.json'
    # df.to_json(path)

    fig = px.line(df)
    pio.write_json(fig, str(path))

    row = dict(
      ele_id=ele_id,
      window_id=views,
      data_path=str(path),
      last_modified=str(datetime.now()),
      callback_function_map='lumi-smoothing',
      # callback_function_map=['lumi-smoothing', 'lumi-time-controller'],
    )
    if ele_id == 'scatter1' or ele_id == 'scatter3':
      del row['callback_function_map']

    self.update_index_file(row)


if __name__ == '__main__':
  main()

# TODO: index data specification
# CSV > json?
# Ele-id, graph-type, last-modified, function (e.g. smoothing), controller-element
