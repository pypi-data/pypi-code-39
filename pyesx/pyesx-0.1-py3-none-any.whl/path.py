"""

A. Enguehard - 07/2019
"""

import os


class esxpath():
    """Object to make it easy to navigate in the esx directory structure
    """

    def __init__(self):
        """
        """
        self.pyesxpath = os.path.dirname(os.path.abspath(__file__))
        self.scriptpath = self.pyesxpath + '/..'
        self.esxpath = self.scriptpath + '/..'
        self.sourcepath = self.esxpath + '/src'
        self.runpath = self.esxpath + '/RUN'
        self.pyesxpath = self.scriptpath + '/pyesx'
        self.libpath = self.scriptpath + '/lib'
        self.projectsdirpath = self.esxpath + '/projects'
        self.projectsdict = {}
        return

    def _setup_existing_projects(self):
        """
        """
        # Go to the projects directory
        os.chdir(self.projectsdirpath)
        # List all the directories
        listdirs = [d for d in os.listdir(self.experimentsdirpath) if
             os.path.isdir(os.path.join(self.experimentsdirpath, d))]
        # Add their names to the projectsdict dictionnary
        for d in listdirs:
            self.projectsdict[d] = esxexppath(self.projectsdirpath, d)
        return


class esxprojectpath(esxpath):
    """
    """

    def __init__(self, project):
        super().__init__()
        self.project = project
        self.projectpath = self.projectsdirpath + '/' + project + ''
        self.scriptsdir_inproj_path = self.projectpath + '/scripts'
        self.experimentsdirpath = self.projectpath + '/experiments'
        self.outputsdirpath = self.projectpath + '/output'
        self.datapath = self.projectpath + '/data'
        self.experimentsdict = {}
        return

    def _setup_existing_experiments(self):
        """
        """
        # Go to the experiments directory
        os.chdir(self.experimentsdirpath)
        # List all the directories
        listdirs = [d for d in os.listdir(self.experimentsdirpath) if
                    os.path.isdir(os.path.join(self.experimentsdirpath, d))]
        # Add their names to the projectsdict dictionnary
        for d in listdirs:
            self.experimentsdict[d] = esxexppath(self.experimentsdirpath, d)
        return


class esxexppath(esxprojectpath):
    """
    """

    def __init__(self, project, experiment):
        super().__init__(project)
        self.experiment = experiment
        self.experimentpath = self.experimentsdirpath + '/' + experiment
        return


class esxrunpath(esxprojectpath):
    """
    """

    def __init__(self, project, runname):
        super().__init__(project)
        self.runname = runname
        self.outputpath = self.outputsdirpath + '/' + runname
        return
