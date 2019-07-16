"""
------------------------------------------------------------------------------
    Copyright (C) 2016-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
from typing import List, Dict, Any, Tuple
from ..view.plot_preview_widget import PlotPreviewWidget

ArgList = List[Any]
KwargDict = Dict[str, Any]

class PlotPreviewWidgetController(PlotPreviewWidget):

    def __init__(self, parent):
        PlotPreviewWidget.__init__(self, parent)

    def plot_image(self, img, args=[], kwargs={}):
        """
        Updates figure to show new image data.
        @param img Image data (as array).
        @param args List of arguments to be passed to call of axis' imshow function.
        @param kwargs Dictionary of key-word arguments to be passed to call of axis'
        imshow function.
        """
        self.ax.clear()
        self.ax.imshow(img, *args, **kwargs)
        self.ax.relim()
        self.ax.autoscale()
        self.canvas.draw()

    def plot_lines(self, data: np.ndarray, x_axis: int=None,
                   plot_by_column: bool=True,
                   args: List[ArgList]=[], kwargs: List[KwargDict]=[]):
        self.ax.clear()
        if data.ndim == 1:
            args_i, kwargs_i = _join_args_and_kwargs(0, args, kwargs)
            self.ax.plot(data, *args_i, **kwargs_i)
        elif data.ndim == 2:            
            if plot_by_column:
                if data.shape[1] > 10:
                    msg = 'Too many columns (n={}) to plot for preview!'
                    msg += '\nMaybe plot as an image?'
                    self.ax.text(0.1, 0.5, msg.format(data.shape[1]),
                                 {'color': 'red', 'size': 16})
                    self.canvas.draw()
                    return
                if x_axis is None:
                    for i in range(data.shape[1]):
                        args_i, kwargs_i = _join_args_and_kwargs(i, args, kwargs)
                        self.ax.plot(data[:, i], *args_i, **kwargs_i)
                else:
                    for i in range(data.shape[1]):
                        if i == x_axis:
                            continue
                        args_i, kwargs_i = _join_args_and_kwargs(i, args, kwargs)
                        self.ax.plot(data[:, x_axis], data[:, i], *args_i, **kwargs_i)
        self.ax.set_aspect('auto')
        self.ax.relim()
        self.ax.autoscale()
        self.canvas.draw()

def _join_args_and_kwargs(i: int,
                          args: List[ArgList],
                          kwargs: List[KwargDict]) -> Tuple[ArgList, KwargDict]:
    args_i = []
    kwargs_i = {}
    if len(args) > 1:
        args_i = args_i + args[i]
    elif len(args) == 1:
        args_i = args_i + args[0]        
    if len(kwargs) > 1:
        kwargs_i.update(kwargs[i])
    elif len(kwargs) == 1:
        kwargs_i.update(kwargs[0])
    return args_i, kwargs_i
