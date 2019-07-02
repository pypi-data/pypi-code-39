#!/usr/local/bin/python
# encoding: utf-8
"""
*import the panstarrs stream into the marshall*

:Author:
    David Young

:Date Created:
    June  6, 2019
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from ..data import data as basedata
from astrocalc.times import now


class data(basedata):
    """
    *The worker class for the data module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``dbConn`` -- the marshall database connection
        - ``settings`` -- the settings dictionary

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a data object, use the following:

        .. todo::

            - add usage info
            - create a sublime snippet for usage
            - create cl-util for this class
            - add a tutorial about ``data`` to documentation
            - create a blog post about what ``data`` does

        .. code-block:: python 

            usage code   
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            dbConn,
            settings=False,
    ):
        self.log = log
        log.debug("instansiating a new 'data' object")
        self.settings = settings
        self.dbConn = dbConn

        self.fsTableName = "fs_panstarrs"

        # xt-self-arg-tmpx

        # Initial Actions

        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """
        *get the data object*

        **Return:**
            - ``data``

        **Usage:**
        .. todo::

            - add usage info
            - create a sublime snippet for usage
            - create cl-util for this method
            - update the package tutorial if needed

        .. code-block:: python 

            usage code 
        """
        self.log.debug('starting the ``get`` method')

        self.log.debug('completed the ``get`` method')
        return data

    def _nullValue(
            self,
            value):
        """*convert blank values to None before database import*

        **Key Arguments:**
            - ``value`` -- the data value to report as null is empty.
            -

        **Return:**
            - ``value`` -- data value or None
        """
        self.log.debug('starting the ``_nullValue`` method')

        returnValue = None

        if value:
            returnValue = value

        self.log.debug('completed the ``_nullValue`` method')
        return value

    # use the tab-trigger below for new method
    def _floatValue(
            self,
            value):
        """*_floatValue*

        **Key Arguments:**
            # -

        **Return:**
            - ``returnValue`` -- the 

        **Usage:**
            ..  todo::

                - add usage info
                - create a sublime snippet for usage
                - write a command-line tool for this method
                - update package tutorial with command-line tool info if needed

            .. code-block:: python 

                usage code 

        """
        self.log.debug('starting the ``_floatValue`` method')

        returnValue = None

        if value:
            try:
                returnValue = float(value)
            except ValueError, e:
                pass

        self.log.debug('completed the ``_floatValue`` method')
        return returnValue

    def _clean_data_pre_ingest(
            self,
            surveyName,
            withinLastDays=False):
        """*clean up the list of dictionaries containing the PS data, pre-ingest*

        **Key Arguments:**
            - ``surveyName`` -- the PS survey name
            -  ``withinLastDays`` -- the lower limit of observations to include (within the last N days from now). Default *False*, i.e. no limit

        **Return:**
            - ``dictList`` -- the cleaned list of dictionaries ready for ingest

        **Usage:**

            To clean the data from the PS 3pi survey:

            .. code-block:: python 

                dictList = ingesters._clean_data_pre_ingest(surveyName="3pi")

            Note you will also be able to access the data via ``ingester.dictList``
        """
        self.log.debug('starting the ``_clean_data_pre_ingest`` method')

        self.dictList = []

        # CALC MJD LIMIT
        if withinLastDays:
            mjdLimit = now(
                log=self.log
            ).get_mjd() - float(withinLastDays)

        for row in self.csvDicts:
            # IF NOW IN THE LAST N DAYS - SKIP
            if withinLastDays and float(row["mjd_obs"]) < mjdLimit:
                continue
            if row["ra_psf"] < 0:
                row["ra_psf"] = 360. + row["ra_psf"]
            thisDictionary = {}
            thisDictionary["candidateID"] = row["ps1_designation"]
            thisDictionary["ra_deg"] = row["ra_psf"]
            thisDictionary["dec_deg"] = row["dec_psf"]
            thisDictionary["mag"] = row["cal_psf_mag"]
            thisDictionary["magerr"] = row["psf_inst_mag_sig"]
            thisDictionary["observationMJD"] = row["mjd_obs"]
            thisDictionary["filter"] = row["filter"]
            try:
                thisDictionary["discDate"] = row["followup_flag_date"]
            except:
                pass
            thisDictionary["discMag"] = row["cal_psf_mag"]
            thisDictionary[
                "objectURL"] = "http://star.pst.qub.ac.uk/sne/%(surveyName)s/psdb/candidate/" % locals() + row["id"]

            target = row["target"]
            if target:
                id, mjdString, diffId, ippIdet, type = target.split('_')
                thisDictionary["targetImageURL"] = "http://star.pst.qub.ac.uk/sne/%(surveyName)s/site_media/images/data/%(surveyName)s" % locals() + '/' + \
                    str(int(float(mjdString))) + '/' + target + '.jpeg'

            ref = row["ref"]
            if ref:
                id, mjdString, diffId, ippIdet, type = ref.split('_')
                thisDictionary["refImageURL"]  = "http://star.pst.qub.ac.uk/sne/%(surveyName)s/site_media/images/data/%(surveyName)s" % locals() + '/' + \
                    str(int(float(mjdString))) + '/' + ref + '.jpeg'

            diff = row["diff"]
            if diff:
                id, mjdString, diffId, ippIdet, type = diff.split('_')
                thisDictionary["diffImageURL"] = "http://star.pst.qub.ac.uk/sne/%(surveyName)s/site_media/images/data/%(surveyName)s" % locals() + '/' + \
                    str(int(float(mjdString))) + '/' + diff + '.jpeg'

            self.dictList.append(thisDictionary)

        self.log.debug('completed the ``_clean_data_pre_ingest`` method')
        return self.dictList

    def ingest(
            self,
            withinLastDays):
        """*Ingest the data into the marshall feeder survey table*

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Usage:**
            ..  todo::

                - add usage info
                - create a sublime snippet for usage
                - write a command-line tool for this method
                - update package tutorial with command-line tool info if needed

            .. code-block:: python 

                usage code 

        """
        self.log.debug('starting the ``ingest`` method')

        self.get_csv_data(
            url=self.settings["panstarrs urls"]["3pi"]["summary csv"],
            user=self.settings["credentials"]["ps1-3pi"]["username"],
            pwd=self.settings["credentials"]["ps1-3pi"]["password"]
        )
        self._clean_data_pre_ingest(
            surveyName="3pi", withinLastDays=withinLastDays)
        self._import_to_feeder_survey_table()

        self.get_csv_data(
            url=self.settings["panstarrs urls"]["3pi"]["recurrance csv"],
            user=self.settings["credentials"]["ps1-3pi"]["username"],
            pwd=self.settings["credentials"]["ps1-3pi"]["password"]
        )
        self._clean_data_pre_ingest(
            surveyName="3pi", withinLastDays=withinLastDays)
        self._import_to_feeder_survey_table()

        self.log.debug('completed the ``ingest`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx
