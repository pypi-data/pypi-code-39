#!/usr/bin/env python
"""A library for check-specific tests."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import collections
import io
import os


from future.builtins import zip
from future.utils import iteritems
from future.utils import iterkeys
import yaml

from grr_response_core import config
from grr_response_core.lib import parsers
from grr_response_core.lib import type_info
from grr_response_core.lib import utils
from grr_response_core.lib.parsers import linux_service_parser
from grr_response_core.lib.rdfvalues import anomaly as rdf_anomaly
from grr_response_core.lib.rdfvalues import client as rdf_client
from grr_response_core.lib.rdfvalues import client_fs as rdf_client_fs
from grr_response_core.lib.rdfvalues import paths as rdf_paths
from grr_response_core.lib.util import precondition
from grr_response_server.check_lib import checks
from grr_response_server.check_lib import filters
from grr_response_server.check_lib import hints
from grr.test_lib import artifact_test_lib
from grr.test_lib import test_lib


class HostCheckTest(test_lib.GRRBaseTest):
  """The base class for host check tests."""

  loaded_checks = None

  @classmethod
  def LoadCheck(cls, cfg_file, *check_ids):
    """Loads checks from a file once per Test class.

    LoadCheck will read a file containing a check configuration and instantiate
    the checks from it. Specific checks can be selected by providing the check
    ids that should be loaded from the file.

    Checks are stored as a class attribute to prevent re-loading as each test
    method is set up.

    Args:
      cfg_file: A path to the file that should be read.
      *check_ids: A list of check ids that should be loaded from the file.

    Returns:
      The loaded check objects.
    """
    if HostCheckTest.loaded_checks is None:
      HostCheckTest.loaded_checks = {}

    cfg = os.path.join(config.CONFIG["Test.srcdir"], "grr", "server",
                       "grr_response_server", "checks", cfg_file)
    if check_ids:
      key = "%s:%s" % (cfg, ",".join(check_ids))
      if key in HostCheckTest.loaded_checks:
        return HostCheckTest.loaded_checks[key]
      loaded = []
      for chk_id in check_ids:
        loaded.append(checks.LoadCheckFromFile(cfg, chk_id))
      HostCheckTest.loaded_checks[key] = loaded
      return loaded
    else:
      key = "%s:*" % cfg_file
      if key in HostCheckTest.loaded_checks:
        return HostCheckTest.loaded_checks[key]
      else:
        result = checks.LoadChecksFromFiles([cfg])
        HostCheckTest.loaded_checks[key] = result
        return result

  def TestDataPath(self, file_name):
    """Generates a full path to the test data."""
    path = os.path.join(config.CONFIG["Test.data_dir"], file_name)
    if not os.path.isfile(path):
      raise RuntimeError("Missing test data: %s" % file_name)
    return path

  @staticmethod
  def SetKnowledgeBase(fqdn="test.example.com", host_os="Linux",
                       host_data=None):
    """Generates a KnowledgeBase entry in the host_data used by checks."""
    if not host_data:
      host_data = {}
    host_data["KnowledgeBase"] = rdf_client.KnowledgeBase(fqdn=fqdn, os=host_os)
    return host_data

  def SetArtifactData(self, anomaly=None, parsed=None, raw=None, results=None):
    """Adds data in the format required by host_data."""
    if not results:
      results = {"ANOMALY": [], "PARSER": [], "RAW": []}
    results["ANOMALY"].extend(anomaly or [])
    results["PARSER"].extend(parsed or [])
    results["RAW"].extend(raw or [])
    return results

  def RunChecks(self, host_data, labels=None, restrict_checks=None):
    """Runs the registered checks against the provided host data.

    Args:
      host_data: A dictionary of artifact_names and results. Results are, in
        turn, a dictionary of {'ANOMALY': [], 'PARSED': [], 'RAW': []} items.
      labels: Additional labels attached to the host.
      restrict_checks: A list specifying a subset of check_ids to run.

    Returns:
      An iterator of check results.
    """
    return {
        r.check_id: r for r in checks.CheckHost(
            host_data, labels=labels, restrict_checks=restrict_checks)
    }

  def GetCheckErrors(self, check_spec):
    """Collect errors generated by host checking tools."""
    errors = []
    try:
      check = checks.Check(**check_spec)
      check.Validate()
    except (checks.Error, filters.Error, hints.Error, type_info.Error) as e:
      errors.append(str(e))
    except Exception as e:  # pylint: disable=broad-except
      # TODO(user): More granular exception handling.
      errors.append("Unknown error %s: %s" % (type(e), e))
    return errors

  def CreateStat(self, path, uid=0, gid=0, mode=0o0100640):
    """Given path, uid, gid and file mode, this returns a StatEntry."""
    pathspec = rdf_paths.PathSpec(path=path, pathtype="OS")
    return rdf_client_fs.StatEntry(
        pathspec=pathspec, st_uid=uid, st_gid=gid, st_mode=mode)

  def _AddToHostData(self, host_data, artifact, data, parser):
    """Parse raw data collected for an artifact into the host_data table."""
    precondition.AssertType(data, dict)

    rdfs = []
    stats = []
    files = []
    for path, lines in iteritems(data):
      stat = self.CreateStat(path)
      stats.append(stat)
      file_obj = io.BytesIO(utils.SmartStr(lines))
      files.append(file_obj)
      if isinstance(parser, parsers.SingleFileParser):
        rdfs.extend(parser.ParseFile(None, stat.pathspec, file_obj))
    if isinstance(parser, parsers.MultiFileParser):
      pathspecs = [stat_entry.pathspec for stat_entry in stats]
      rdfs.extend(parser.ParseFiles(None, pathspecs, files))
    host_data[artifact] = self.SetArtifactData(
        anomaly=[a for a in rdfs if isinstance(a, rdf_anomaly.Anomaly)],
        parsed=[r for r in rdfs if not isinstance(r, rdf_anomaly.Anomaly)],
        raw=stats,
        results=host_data.get(artifact))
    return host_data

  def GenResults(self, artifact_list, sources_list, parser_list=None):
    """Given a list of artifacts, sources and parsers, will RunChecks on them.

    Sample: (["Artifact1", "Artifact2"], [artifact1_data, artifact2_data],
             [config_file.artifact1_Parser(), config_file.artifact2_Parser()]

    artifact1_Parser().parse will run on artifact1_data & parsed results, along
    with raw and anomalies will be inserted into the host_data["Artifact1"].

    artifact2_Parser().parse will run on artifact2_data & parsed results, along
    with raw and anomalies will be inserted into the host_data["Artifact2"].

    Once artifacts added to host_data, loaded checks will be run against it.

    Args:
      artifact_list: list of artifacts to add to host_data for running checks
      sources_list: list of dictionaries containing file names and file data. If
        parser_list is empty then sources_list must contain a list of lists
        containing StatEntry or lists of other raw artifact data.
      parser_list: list of parsers to apply to file data from sources_list. This
        can be empty if no parser is to be applied.

    Returns:
      CheckResult containing any findings in sources_list against loaded checks.

    Raises:
      TypeError: If input lists are not actually lists.
      ValueError: If input lists are not of the same length.
    """
    if parser_list is None:
      parser_list = [None] * len(artifact_list)

    if not isinstance(artifact_list, list):
      raise TypeError("Given artifact list is not a list")
    if not isinstance(sources_list, list):
      raise TypeError("Given list of sources is not a list")
    if not isinstance(parser_list, list):
      raise TypeError("Given parser list is not a list")
    if not len(artifact_list) == len(sources_list) == len(parser_list):
      raise ValueError("All lists are not of the same length.")

    host_data = self.SetKnowledgeBase()
    for artifact, sources, parser in zip(artifact_list, sources_list,
                                         parser_list):
      if parser is None:
        host_data[artifact] = self.SetArtifactData(
            raw=sources, results=host_data.get(artifact))
      else:
        host_data = self._AddToHostData(host_data, artifact, sources, parser)
    return self.RunChecks(host_data)

  def GenProcessData(self, processes, **kwargs):
    """Create some process-based host data."""
    host_data = self.SetKnowledgeBase(**kwargs)
    data = []
    for (name, pid, cmdline) in processes:
      data.append(rdf_client.Process(name=name, pid=pid, cmdline=cmdline))
    # ListProcessesGrr is a flow artifact, thus it needs stored as raw.
    host_data["ListProcessesGrr"] = self.SetArtifactData(raw=data)
    return host_data

  def GenFileData(self, artifact, data, parser=None, modes=None, include=None):
    """Create a set of host_data results based on file parser results.

    Creates a host data result populated with a knowledge base, then processes
    each piece of host data as if it were file results using a parser. Specific
    stat values can be provided to the parser, if required, so that permissions,
    ownership and file types can be defined.

    Args:
      artifact: The artifact name that generated data will be mapped to.
      data: A dictionary of pathnames and data strings. The data strings are
        converted into file objects for the parser.
      parser: The FileParser that processes the data (and stats)
      modes: A dictionary of pathnames and stat values. Stat values are a dict
        of {st_uid: int, st_gid: int, st_mode: oct} entries.
      include: A list of pathnames to include in processing. If not provided,
        all paths are parsed.

    Returns:
      the host_data map populated with a knowledge base and artifact data.

    Raises:
      ValueError: When the handed parser was not initialized.
    """
    host_data = self.SetKnowledgeBase()
    if not parser:
      raise ValueError("Test method requires an initialized parser.")
    if not modes:
      modes = {}
    kb = host_data["KnowledgeBase"]
    files = []
    stats = []
    for path in data:
      if include and path not in include:
        continue
      file_modes = modes.get(path, {})
      stats, files = artifact_test_lib.GenFileData([path], [data[path]],
                                                   stats=stats,
                                                   files=files,
                                                   modes=file_modes)

    rdfs = []
    if isinstance(parser, parsers.SingleFileParser):
      for stat_entry, filedesc in zip(stats, files):
        pathspec = stat_entry.pathspec
        rdfs.extend(parser.ParseFile(kb, pathspec, filedesc))
    elif isinstance(parser, parsers.MultiFileParser):
      pathspecs = [stat_entry.pathspec for stat_entry in stats]
      rdfs.extend(parser.ParseFiles(kb, pathspecs, files))
    else:
      raise TypeError("Incorrect parser type: %s" % parser)

    anomaly = [a for a in rdfs if isinstance(a, rdf_anomaly.Anomaly)]
    parsed = [r for r in rdfs if not isinstance(r, rdf_anomaly.Anomaly)]
    host_data[artifact] = self.SetArtifactData(
        parsed=parsed, anomaly=anomaly, raw=stats)
    return host_data

  def GenSysVInitData(self, links):
    """Create some Sys V init host data."""
    return self.GenFileData(
        artifact="LinuxServices",
        data={x: "" for x in links},
        parser=linux_service_parser.LinuxSysVInitParser(),
        modes={x: {
            "st_mode": 41471
        } for x in links})

  # The assert methods

  def assertRanChecks(self, check_ids, results):
    """Tests that the specified checks were run."""
    self.assertContainsSubset(check_ids, iterkeys(results))

  def assertChecksNotRun(self, check_ids, results):
    """Tests that the specified checks were not run."""
    self.assertNoCommonElements(check_ids, iterkeys(results))

  def assertResultEqual(self, rslt1, rslt2):
    """Tests whether two check results are identical."""
    # Build a map of anomaly symptoms to findings.
    if rslt1.check_id != rslt2.check_id:
      self.fail("Check IDs differ: %s vs %s" % (rslt1.check_id, rslt2.check_id))

    # Quick check to see if anomaly counts are the same and they have the same
    # ordering, using symptoms as a measure.
    rslt1_anoms = {}
    for a in rslt1.anomaly:
      anoms = rslt1_anoms.setdefault(a.symptom, [])
      anoms.extend(a.finding)
    rslt2_anoms = {}
    for a in rslt2.anomaly:
      anoms = rslt2_anoms.setdefault(a.symptom, [])
      anoms.extend(a.finding)

    self.assertCountEqual(rslt1_anoms, rslt2_anoms)

    # Now check that the anomalies are the same, modulo newlines.
    for symptom, findings in iteritems(rslt1_anoms):
      rslt1_found = [f.strip() for f in findings]
      rslt2_found = [f.strip() for f in rslt2_anoms[symptom]]
      self.assertCountEqual(rslt1_found, rslt2_found)

  def assertIsCheckIdResult(self, rslt, expected):
    """Tests if a check has the expected check_id."""
    self.assertIsInstance(rslt, checks.CheckResult)
    self.assertEqual(expected, rslt.check_id)

  def assertValidCheck(self, check_spec):
    """Tests if a check definition generates structural errors."""
    errors = self.GetCheckErrors(check_spec)
    if errors:
      self.fail("\n".join(errors))

  def assertValidCheckFile(self, path):
    """Tests whether a check definition has a valid configuration."""
    # Figure out the relative path of the check files.
    prefix = os.path.commonprefix(config.CONFIG["Checks.config_dir"])
    relpath = os.path.relpath(path, prefix)
    # If the config can't load fail immediately.
    try:
      configs = checks.LoadConfigsFromFile(path)
    except yaml.error.YAMLError as e:
      self.fail("File %s could not be parsed: %s\n" % (relpath, e))
    # Otherwise, check all the configs and pass/fail at the end.
    errors = collections.OrderedDict()
    for check_id, check_spec in iteritems(configs):
      check_errors = self.GetCheckErrors(check_spec)
      if check_errors:
        msg = errors.setdefault(relpath, ["check_id: %s" % check_id])
        msg.append(check_errors)
    if errors:
      message = ""
      for k, v in iteritems(errors):
        message += "File %s errors:\n" % k
        message += "  %s\n" % v[0]
        for err in v[1]:
          message += "    %s\n" % err
      self.fail(message)

  def _HasSymptom(self, anomalies, sym):
    """Tests if one or more anomalies contain the expected symptom string."""
    if sym is None:
      return True
    rslts = {rslt.symptom: rslt for rslt in anomalies}
    rslt = rslts.get(sym)
    # Anomalies evaluate false if there are no finding strings.
    self.assertIsNotNone(
        rslt, "Didn't get expected symptom string '%s' in '%s'" %
        (sym, ",".join(rslts)))

  def _GetFindings(self, anomalies, sym):
    """Generate a set of findings from anomalies that match the symptom."""
    result = set()
    for anomaly in anomalies:
      if anomaly.symptom == sym:
        result.update(set(anomaly.finding))
    return result

  def _MatchFindings(self, expected, found):
    """Check that every expected finding is a substring of a found finding."""
    matched_so_far = set()
    for finding_str in expected:
      no_match = True
      for found_str in found:
        if finding_str in found_str:
          matched_so_far.add(found_str)
          no_match = False
          break
      if no_match:
        return False
    # If we got here, all expected's match at least one item.
    # Now check if every item in found was matched at least once.
    # If so, everything is as expected, If not, Badness.
    if not matched_so_far.symmetric_difference(found):
      return True

  def assertCheckDetectedAnom(self, check_id, results, sym=None, findings=None):
    """Assert a check was performed and specific anomalies were found.

    Results may contain multiple anomalies. The check will hold true if any
    one of them matches. As some results can contain multiple anomalies we
    will need to make sure the right anomalies are selected.

    If an symptom is provided, look for anomalies that matches the
    expression string and use those. Otherwise, all anomalies in the
    check should be used.

    If finding strings are provided, the check tests if the substring is present
    in the findings of the anomalies that are selected for testing. If the
    finding results can have variable ordering, use a substring that will remain
    constant for each finding.

    Args:
      check_id: The check_id as a string.
      results: A dictionary of check results, mapped to check_ids
      sym: An symptom string. This is the "title" of an advisory.
      findings: A list of finding strings that should be present in the findings
        of the selected anomaly.

    Returns:
      True if tests have succeeded and no further processing is required.
    """
    chk = results.get(check_id)
    self.assertIsNotNone(chk, "check %s did not run" % check_id)
    # Checks return true if there were anomalies.
    self.assertTrue(chk, "check %s did not generate anomalies" % check_id)
    # If sym or results are passed as args, look for anomalies with these
    # values.
    self._HasSymptom(chk.anomaly, sym)
    if findings is None:
      # We are not expecting to match on findings, so skip checking them.
      return True
    findings = set(findings)
    found = self._GetFindings(chk.anomaly, sym)
    if self._MatchFindings(findings, found):
      # Everything matches, and nothing unexpected, so all is good.
      return True
    # If we have made it here, we have the expected symptom but
    # the findings didn't match up.
    others = "\n".join([str(a) for a in chk.anomaly])
    self.fail("Findings don't match for symptom '%s':\nExpected:\n  %s\n"
              "Got:\n  %s\nFrom:\n%s" % (sym, ", ".join(findings),
                                         ", ".join(found), others))

  def assertCheckUndetected(self, check_id, results):
    """Assert a check_id was performed, and resulted in no anomalies."""
    if not isinstance(results, collections.Mapping):
      self.fail("Invalid arg, %s should be dict-like.\n" % type(results))
    if check_id not in results:
      self.fail("Check %s was not performed.\n" % check_id)
    # A check result will evaluate as True if it contains an anomaly.
    if results.get(check_id):
      self.fail("Check %s unexpectedly produced an anomaly.\nGot: %s\n" %
                (check_id, results.get(check_id).anomaly))

  def assertChecksUndetected(self, check_ids, results):
    """Assert multiple check_ids were performed & they produced no anomalies."""
    for check_id in check_ids:
      self.assertCheckUndetected(check_id, results)
