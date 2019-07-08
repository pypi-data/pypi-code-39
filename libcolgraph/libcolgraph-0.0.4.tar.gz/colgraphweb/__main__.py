#!/usr/bin/env python3

import argparse
import subprocess
import webbrowser
import sys
from os.path import expanduser
from pathlib import Path
from flask import Flask, url_for, request, render_template, json
from collections import defaultdict
import webbrowser
import random
import PySimpleGUI as sg

import libcolgraph as lcg


app = Flask(__name__)

global args
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', type=str,
                    help='read in BaseGraph from adjacency matrix file',
                    default=None)
                    # default=str(Path(__file__).parent/'../in/hexmod.in'))
parser.add_argument('-n', '--new', default=True, action='store_true',
                    help='open a blank canvas?')
parser.add_argument('-s', '--select_file', default=False, action='store_true',
                    help='open file choosing gui dialogue?')
parser.add_argument('-k', '--colors', type=int, default=3,
                    help='number of colors to use to create ColoringGraph')
parser.add_argument('-v', '--verbosity', action='count', default=0,
                    help='set output verbosity')
parser.add_argument('-p', '--port', default='5000', type=str,
                    help='port to launch GUI on')
parser.add_argument('-w', '--webbrowser', default=False, action='store_true',
                    help='open app in default web browser window?')
parser.add_argument('-r', '--render_on_launch', default=False, 
                    action='store_true', help='render to-generate componenets '
                                              'on initial launch?')
parser.add_argument('-d', '--debug', default=False, action='store_true',
                    help='launch Flask app in debug mode?')
args = parser.parse_args()

global data
data = dict()


colors = {
            'red': '#ef5350',
            'blue': '#039be5',
            'green': '#4caf50',
            'yellow': '#ffee58',
            'pink': '#f48fb1',
            'purple': '#673ab7',
            'brown': '#795548',
            'white': 'white',#'#f5f5f5',
         }
colorarray = ['yellow', 'green', 'purple', 'white', 'pink', 'brown']

randomcolors = {}
randomcolors.update(colors)
randomcolors.pop('red')
randomcolors.pop('blue')
randomcolors = [*randomcolors.keys()]



@app.route('/', methods=['GET'])
def index():
    '''
    '''
    # if request.method != 'GET':
    #     raise RuntimeError

    global data
    print('handling GET on index!')
    data.update(dict(colors=str(args.colors)))

    app.cghtml = None
    app.statsdict = defaultdict(None)

    return render_template('defaultview.html', **data)


def cvcolorfngen(cut_verts):
    return lambda v: 'red' if v.get_name() in cut_verts else None


def update_bg_data(bg):
    '''
    '''
    global data
    data.update(lcg.viz.to_visjs(bg, colordict=colors, colorfn=lambda v: None))


def update_cg_data(cg):
    '''
    '''
    global data
    data.update(lcg.viz.to_visjs(cg, colordict=colors,
                                 colorfn=cvcolorfngen(app.cut_verts)))


def update_mcg_data(mcg):
    '''
    '''
    global data
    data.update(lcg.viz.to_visjs(mcg))


def update_pcg_data(pcg):
    '''
    '''
    global data
    data.update(lcg.viz.to_visjs(pcg, force_type='pcg', colordict=colors,
                                 colorfn=cvcolorfngen(app.cut_verts)))


@app.route('/generate', methods=['POST'])
def generate():
    '''
    '''
    requestdata = request.get_json()
    # print(requestdata)
    print('handling POST on generate!')

    global data

    graphdata = requestdata[0]
    args.colors = int(requestdata[1])
    data.update(dict(colors=args.colors))

    app.bg = bg = lcg.viz.from_visjs(graphdata)
    update_bg_data(bg)

    app.cg = cg = bg.build_coloring_graph(args.colors)
    app.mcg = mcg = cg.tarjans()
    app.cut_verts = cut_verts = [*mcg.get_cut_vertices()]
    update_mcg_data(mcg)

    app.pcg = pcg = mcg.rebuild_partial_graph()
    update_pcg_data(pcg)

    app.statsdict = statsdict = dict(
            cgsize=len(cg),
            is_connected=cg.is_connected(),
            is_biconnected=cg.is_biconnected(),
        )

    retdict = {
        'bgcontainer': render_template('graphcontainer.html',
                                        container_type='bg', **data),
        'mcgcontainer': render_template('graphcontainer.html',
                                        container_type='mcg', **data),
        'pcgcontainer': render_template('graphcontainer.html',
                                        container_type='pcg', **data),
        'cgsize': app.statsdict['cgsize'],
                }
    

    if len(cg) <= 512:
        update_cg_data(cg)
        app.cghtml = render_template('graphcontainer.html',
                                 container_type='cg', **data)
        retdict.update({'cgcontainer': app.cghtml})

    response = app.response_class(status=200, response=json.dumps(retdict),
                                  mimetype='application/json')

    return response


@app.route('/cgdata', methods=['POST'])
def get_cg_data():
    '''
    '''
    requestdata = request.get_json()
    # print(requestdata)
    print('handling POST on get_cg_data!')

    update_cg_data(app.cg)
    app.cghtml = render_template('graphcontainer.html',
                                 container_type='cg', **data)
    retdict = {'cgcontainer': app.cghtml}

    response = app.response_class(status=200, response=json.dumps(retdict),
                                  mimetype='application/json')

    return response


@app.route('/cgstats', methods=['POST'])
def get_stats():
    '''
    '''
    requestdata = request.get_json()
    # print(requestdata)
    print('handling POST on get_stats!')

    retdict = {
        'cgstats': ' '.join(['{}: {},'.format(k, v)
                             for k, v in app.statsdict.items()]),
              }

    response = app.response_class(status=200, response=json.dumps(retdict),
                                  mimetype='application/json')

    return response



@app.route('/colorbg_from_mcg', methods=['POST'])
def colorbg_from_mcg():
    '''
    returns a coloring specification to pass to the graph drawing utility
    using a vertex of the meta coloring graph. the important thing to note is
    that a MetaVertex can represent multiple colorings, so only the fixed
    coloring positions will be so colored in the basegraph
    '''
    requestdata = request.get_json()
    selected_vertex = requestdata[0]

    vertices = [*app.mcg.get_vertex(selected_vertex).get_vertices()]
    vname = vertices[0]
    coloring = [app.bg.get_vertex_color(vname, i, app.mcg.colors)
                for i in range(len(app.bg))]

    for vname in vertices:
        altcoloring = [app.bg.get_vertex_color(vname, i, app.mcg.colors)
                       for i in range(len(app.bg))]
        for i, (a, b) in enumerate(zip(coloring, altcoloring)):
            if a != b:
                coloring[i] = -1

    return colorbg(coloring)


@app.route('/colorbg_from_cg', methods=['POST'])
def colorbg_from_cg():
    '''
    returns a colorfn to pass to the graph drawing utility. a single coloring
    vertex fully specifies the coloring of the basegraph, and so the basegraph
    will be fully colored based on the output of this method
    '''
    requestdata = request.get_json()
    selected_vertex = requestdata[0]

    coloring = [app.bg.get_vertex_color(selected_vertex, i, app.cg.colors)
                for i in range(len(app.bg))]

    return colorbg(coloring)


@app.route('/colorbg', methods=['POST'])
def colorbg(coloring_list=None):
    '''
    given a list of colors (or indetermined colors) for the basegraph, with
    each position in the list corresponding to a vertex, returns a colored
    view of the basegraphbased on that coloring. this function defines the
    colorfn based on supplied coloring_list
    '''
    if not coloring_list:
        requestdata = request.get_json()
        coloring_list = requestdata[0]

    def color_from_coloring_list(v):
        name = v.get_name()
        if coloring_list[name] >= 0:
            return colorarray[coloring_list[name]]
        return None

    data.update(lcg.viz.to_visjs(app.bg, colordict=colors,
                                 colorfn=color_from_coloring_list))

    retdict = {
        'bgcontainer': render_template('graphcontainer.html',
                                        container_type='bg', **data),
              }

    response = app.response_class(status=200, response=json.dumps(retdict),
                                  mimetype='application/json')

    return response



@app.route('/save', methods=['POST'])
def save_graphs():
    '''
    '''
    raise NotImplementedError


def runflaskgui(url='http://localhost', port='5000'):
    '''
    '''
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = args.debug
    app.config['TESTING'] = True

    bg = lcg.BaseGraph()
    if args.input_file:
        bg.load_txt(args.input_file)

    update_bg_data(bg)

    if args.render_on_launch:
        app.cg = cg = bg.build_coloring_graph(args.colors)
        app.mcg = mcg = cg.tarjans()
        app.pcg = pcg = mcg.rebuild_partial_graph()
        app.cut_verts = cut_verts = [*mcg.get_cut_vertices()]
        app.pcg = pcg = mcg.rebuild_partial_graph()
        
        update_mcg_data(mcg)
        update_cg_data(cg)
        update_pcg_data(pcg)

        app.statsdict = statsdict = dict(
            cgsize=len(cg),
            is_connected=cg.is_connected(),
            is_biconnected=cg.is_biconnected(),
        )
        data.update({'cgstats': ' '.join(['{}: {},'.format(k, v)
                                for k, v in app.statsdict.items()])}) 

    app.run(port=port)


def main():
    '''
    '''
    url = 'http://localhost'
    port = args.port
    if args.webbrowser:
        webbrowser.open_new(url + ':{port}'.format(port=port))

    if args.select_file:
        # resp = sg.PopupGetFile('Choose a file if you\'d like to load a graph. '
        #                        'To open a blank canvas, click cancel.',
        #                        title='Load graph from a file?')
        w = sg.Window('Get filename example').Layout([[sg.Text('Filename')], [sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()] ])
        event, values = w.Read()
        w.Close()
        if event == 'OK':
            resp = values[0]
            if resp and Path(resp).exists():
                args.input_file = resp
            else:
                print('Unable to load file. Opening blank canvas')

    runflaskgui(url, port)


if __name__ == '__main__':
    main()
