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
  logger.log_line(x, y, 'scatter2')


class LumiLogger:
  def __init__(self, outdir, env_id=None):
    if env_id is None:
      env_id = time.time()

    outdir.mkdir(exist_ok=True)
    self.outdir = outdir
    self.index_file = outdir / 'meta.lumi.csv'
    self.index = pd.DataFrame()

  def update_index_file(self, ele_id, path):
    row = dict(
      ele_id=ele_id,
      data_path=path,
      graph_type='scatter',
      last_modified=datetime.now(),
      callback_function='lumi.smoothing',
    )
    self.index = self.index.append(row, ignore_index=True)
    self.index.to_csv(self.index_file)

  def log_line(self, x, y, ele_id):
    df = pd.DataFrame(dict(y=y))
    path = self.outdir / f'{ele_id}.json'
    # df.to_json(path)

    fig = px.line(df)
    pio.write_json(fig, str(path))

    self.update_index_file(ele_id, path)


if __name__ == '__main__':
  main()

# TODO: index data specification
# CSV > json?
# Ele-id, graph-type, last-modified, function (e.g. smoothing), controller-element
