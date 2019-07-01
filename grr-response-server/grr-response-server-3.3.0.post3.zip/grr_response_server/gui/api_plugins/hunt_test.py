#!/usr/bin/env python
"""This modules contains tests for hunts API handlers."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import io
import os
import tarfile
import zipfile


from absl import app
from future.builtins import range
import yaml

from grr_response_core.lib import rdfvalue
from grr_response_core.lib import utils
from grr_response_core.lib.rdfvalues import file_finder as rdf_file_finder
from grr_response_core.lib.rdfvalues import flows as rdf_flows
from grr_response_core.lib.rdfvalues import test_base as rdf_test_base
from grr_response_server import access_control
from grr_response_server import aff4
from grr_response_server import data_store
from grr_response_server import hunt
from grr_response_server.aff4_objects import aff4_grr
from grr_response_server.databases import db
from grr_response_server.flows.general import file_finder
from grr_response_server.gui import api_test_lib
from grr_response_server.gui.api_plugins import hunt as hunt_plugin
from grr_response_server.hunts import implementation
from grr_response_server.output_plugins import test_plugins
from grr_response_server.rdfvalues import flow_runner as rdf_flow_runner
from grr_response_server.rdfvalues import output_plugin as rdf_output_plugin
from grr.test_lib import action_mocks
from grr.test_lib import db_test_lib
from grr.test_lib import flow_test_lib
from grr.test_lib import hunt_test_lib
from grr.test_lib import test_lib


class ApiHuntIdTest(rdf_test_base.RDFValueTestMixin, test_lib.GRRBaseTest):
  """Test for ApiHuntId."""

  rdfvalue_class = hunt_plugin.ApiHuntId

  def GenerateSample(self, number=0):
    return hunt_plugin.ApiHuntId("H:%d" % number)

  def testRaisesWhenInitializedFromInvalidValues(self):
    with self.assertRaises(ValueError):
      hunt_plugin.ApiHuntId("bl%ah")

    with self.assertRaises(ValueError):
      hunt_plugin.ApiHuntId("H:")

    with self.assertRaises(ValueError):
      hunt_plugin.ApiHuntId("H:1234/foo")

  def testRaisesWhenToURNCalledOnUninitializedValue(self):
    hunt_id = hunt_plugin.ApiHuntId()
    with self.assertRaises(ValueError):
      hunt_id.ToURN()

  def testConvertsToHuntURN(self):
    hunt_id = hunt_plugin.ApiHuntId("H:1234")
    hunt_urn = hunt_id.ToURN()

    self.assertEqual(hunt_urn.Basename(), hunt_id)
    self.assertEqual(hunt_urn, "aff4:/hunts/H:1234")


@db_test_lib.DualDBTest
class ApiCreateHuntHandlerTest(api_test_lib.ApiCallHandlerTest,
                               hunt_test_lib.StandardHuntTestMixin):
  """Test for ApiCreateHuntHandler."""

  def setUp(self):
    super(ApiCreateHuntHandlerTest, self).setUp()
    self.handler = hunt_plugin.ApiCreateHuntHandler()

  def testQueueHuntRunnerArgumentIsNotRespected(self):
    args = hunt_plugin.ApiCreateHuntArgs(
        flow_name=file_finder.FileFinder.__name__)
    args.hunt_runner_args.queue = "BLAH"
    result = self.handler.Handle(args, token=self.token)
    self.assertFalse(result.hunt_runner_args.HasField("queue"))


@db_test_lib.DualDBTest
class ApiListHuntsHandlerTest(api_test_lib.ApiCallHandlerTest,
                              hunt_test_lib.StandardHuntTestMixin):
  """Test for ApiListHuntsHandler."""

  def setUp(self):
    super(ApiListHuntsHandlerTest, self).setUp()
    self.handler = hunt_plugin.ApiListHuntsHandler()

  def testHandlesListOfHuntObjects(self):
    for i in range(10):
      self.CreateHunt(description="hunt_%d" % i)

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(), token=self.token)
    descriptions = set(r.description for r in result.items)

    self.assertLen(descriptions, 10)
    for i in range(10):
      self.assertIn("hunt_%d" % i, descriptions)

  def testHuntListIsSortedInReversedCreationTimestampOrder(self):
    for i in range(1, 11):
      with test_lib.FakeTime(i * 1000):
        self.CreateHunt(description="hunt_%d" % i)

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(), token=self.token)
    create_times = [r.created.AsMicrosecondsSinceEpoch() for r in result.items]

    self.assertLen(create_times, 10)
    for index, expected_time in enumerate(reversed(range(1, 11))):
      self.assertEqual(create_times[index], expected_time * 1000000000)

  def testHandlesSubrangeOfListOfHuntObjects(self):
    for i in range(1, 11):
      with test_lib.FakeTime(i * 1000):
        self.CreateHunt(description="hunt_%d" % i)

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(offset=2, count=2), token=self.token)
    create_times = [r.created.AsMicrosecondsSinceEpoch() for r in result.items]

    self.assertLen(create_times, 2)
    self.assertEqual(create_times[0], 8 * 1000000000)
    self.assertEqual(create_times[1], 7 * 1000000000)

  def testFiltersHuntsByActivityTime(self):
    for i in range(1, 11):
      with test_lib.FakeTime(i * 60):
        self.CreateHunt(description="hunt_%d" % i)

    with test_lib.FakeTime(10 * 60 + 1):
      result = self.handler.Handle(
          hunt_plugin.ApiListHuntsArgs(active_within="2m"), token=self.token)

    create_times = [r.created for r in result.items]

    self.assertLen(create_times, 2)
    self.assertEqual(create_times[0], 10 * 60 * 1000000)
    self.assertEqual(create_times[1], 9 * 60 * 1000000)

  # New implementation doesn't have this resriction.
  @db_test_lib.LegacyDataStoreOnly
  def testRaisesIfCreatedByFilterUsedWithoutActiveWithinFilter(self):
    self.assertRaises(
        ValueError,
        self.handler.Handle,
        hunt_plugin.ApiListHuntsArgs(created_by="user-bar"),
        token=self.token)

  def testFiltersHuntsByCreator(self):
    for i in range(5):
      self.CreateHunt(
          description="foo_hunt_%d" % i,
          token=access_control.ACLToken(username="user-foo"))

    for i in range(3):
      self.CreateHunt(
          description="bar_hunt_%d" % i,
          token=access_control.ACLToken(username="user-bar"))

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(created_by="user-foo", active_within="1d"),
        token=self.token)
    self.assertLen(result.items, 5)
    for item in result.items:
      self.assertEqual(item.creator, "user-foo")

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(created_by="user-bar", active_within="1d"),
        token=self.token)
    self.assertLen(result.items, 3)
    for item in result.items:
      self.assertEqual(item.creator, "user-bar")

  def testRaisesIfDescriptionContainsFilterUsedWithoutActiveWithinFilter(self):
    self.assertRaises(
        ValueError,
        self.handler.Handle,
        hunt_plugin.ApiListHuntsArgs(description_contains="foo"),
        token=self.token)

  def testFiltersHuntsByDescriptionContainsMatch(self):
    for i in range(5):
      self.CreateHunt(description="foo_hunt_%d" % i)

    for i in range(3):
      self.CreateHunt(description="bar_hunt_%d")

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(
            description_contains="foo", active_within="1d"),
        token=self.token)
    self.assertLen(result.items, 5)
    for item in result.items:
      self.assertIn("foo", item.description)

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(
            description_contains="bar", active_within="1d"),
        token=self.token)
    self.assertLen(result.items, 3)
    for item in result.items:
      self.assertIn("bar", item.description)

  def testOffsetIsRelativeToFilteredResultsWhenFilterIsPresent(self):
    for i in range(5):
      self.CreateHunt(description="foo_hunt_%d" % i)

    for i in range(3):
      self.CreateHunt(description="bar_hunt_%d" % i)

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(
            description_contains="bar", active_within="1d", offset=1),
        token=self.token)
    self.assertLen(result.items, 2)
    for item in result.items:
      self.assertIn("bar", item.description)

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(
            description_contains="bar", active_within="1d", offset=2),
        token=self.token)
    self.assertLen(result.items, 1)
    for item in result.items:
      self.assertIn("bar", item.description)

    result = self.handler.Handle(
        hunt_plugin.ApiListHuntsArgs(
            description_contains="bar", active_within="1d", offset=3),
        token=self.token)
    self.assertEmpty(result.items)


@db_test_lib.DualDBTest
class ApiGetHuntFilesArchiveHandlerTest(hunt_test_lib.StandardHuntTestMixin,
                                        api_test_lib.ApiCallHandlerTest):

  def setUp(self):
    super(ApiGetHuntFilesArchiveHandlerTest, self).setUp()

    self.handler = hunt_plugin.ApiGetHuntFilesArchiveHandler()

    self.client_ids = self.SetupClients(10)
    self.hunt_urn = self.StartHunt(
        flow_runner_args=rdf_flow_runner.FlowRunnerArgs(
            flow_name=file_finder.FileFinder.__name__),
        flow_args=rdf_file_finder.FileFinderArgs(
            paths=[os.path.join(self.base_path, "test.plist")],
            action=rdf_file_finder.FileFinderAction(action_type="DOWNLOAD"),
        ),
        client_rate=0,
        token=self.token)
    self.hunt_id = self.hunt_urn.Basename()

    self.RunHunt(
        client_ids=self.client_ids,
        client_mock=action_mocks.FileFinderClientMock())

  def testGeneratesZipArchive(self):
    result = self.handler.Handle(
        hunt_plugin.ApiGetHuntFilesArchiveArgs(
            hunt_id=self.hunt_id, archive_format="ZIP"),
        token=self.token)

    out_fd = io.BytesIO()
    for chunk in result.GenerateContent():
      out_fd.write(chunk)

    zip_fd = zipfile.ZipFile(out_fd, "r")
    manifest = None
    for name in zip_fd.namelist():
      if name.endswith("MANIFEST"):
        manifest = yaml.safe_load(zip_fd.read(name))

    self.assertDictContainsSubset(
        {
            "archived_files": 10,
            "failed_files": 0,
            "processed_files": 10,
            "ignored_files": 0,
        }, manifest)

  def testGeneratesTarGzArchive(self):
    result = self.handler.Handle(
        hunt_plugin.ApiGetHuntFilesArchiveArgs(
            hunt_id=self.hunt_id, archive_format="TAR_GZ"),
        token=self.token)

    with utils.TempDirectory() as temp_dir:
      tar_path = os.path.join(temp_dir, "archive.tar.gz")
      with open(tar_path, "wb") as fd:
        for chunk in result.GenerateContent():
          fd.write(chunk)

      with tarfile.open(tar_path) as tar_fd:
        tar_fd.extractall(path=temp_dir)

      manifest_file_path = None
      for parent, _, files in os.walk(temp_dir):
        if "MANIFEST" in files:
          manifest_file_path = os.path.join(parent, "MANIFEST")
          break

      self.assertTrue(manifest_file_path)
      with open(manifest_file_path, "rb") as fd:
        manifest = yaml.safe_load(fd.read())

        self.assertDictContainsSubset(
            {
                "archived_files": 10,
                "failed_files": 0,
                "processed_files": 10,
                "ignored_files": 0,
            }, manifest)


@db_test_lib.DualDBTest
class ApiGetHuntFileHandlerTest(api_test_lib.ApiCallHandlerTest,
                                hunt_test_lib.StandardHuntTestMixin):

  def setUp(self):
    super(ApiGetHuntFileHandlerTest, self).setUp()

    self.handler = hunt_plugin.ApiGetHuntFileHandler()

    self.file_path = os.path.join(self.base_path, "test.plist")
    self.aff4_file_path = "fs/os/%s" % self.file_path

    self.hunt_urn = self.StartHunt(
        flow_runner_args=rdf_flow_runner.FlowRunnerArgs(
            flow_name=file_finder.FileFinder.__name__),
        flow_args=rdf_file_finder.FileFinderArgs(
            paths=[self.file_path],
            action=rdf_file_finder.FileFinderAction(action_type="DOWNLOAD"),
        ),
        client_rate=0,
        token=self.token)
    self.hunt_id = self.hunt_urn.Basename()

    self.client_id = self.SetupClient(0)
    self.RunHunt(
        client_ids=[self.client_id],
        client_mock=action_mocks.FileFinderClientMock())

  def testRaisesIfOneOfArgumentAttributesIsNone(self):
    model_args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path=self.aff4_file_path,
        timestamp=rdfvalue.RDFDatetime.Now())

    args = model_args.Copy()
    args.hunt_id = None
    with self.assertRaises(ValueError):
      self.handler.Handle(args)

    args = model_args.Copy()
    args.client_id = None
    with self.assertRaises(ValueError):
      self.handler.Handle(args)

    args = model_args.Copy()
    args.vfs_path = None
    with self.assertRaises(ValueError):
      self.handler.Handle(args)

    args = model_args.Copy()
    args.timestamp = None
    with self.assertRaises(ValueError):
      self.handler.Handle(args)

  def testRaisesIfVfsRootIsNotWhitelisted(self):
    args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path="flows/W:123456",
        timestamp=rdfvalue.RDFDatetime().Now())

    with self.assertRaises(ValueError):
      self.handler.Handle(args)

  def testRaisesIfResultIsBeforeTimestamp(self):
    if data_store.RelationalDBEnabled():
      results = data_store.REL_DB.ReadHuntResults(self.hunt_id, 0, 1)
    else:
      results = implementation.GRRHunt.ResultCollectionForHID(
          self.hunt_urn, token=self.token)

    args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path=self.aff4_file_path,
        timestamp=results[0].age + rdfvalue.Duration("1s"))
    with self.assertRaises(hunt_plugin.HuntFileNotFoundError):
      self.handler.Handle(args, token=self.token)

  def _FillInStubResults(self):
    results = implementation.GRRHunt.ResultCollectionForHID(
        self.hunt_urn, token=self.token)
    result = results[0]

    with data_store.DB.GetMutationPool() as pool:
      for i in range(self.handler.MAX_RECORDS_TO_CHECK):
        wrong_result = rdf_flows.GrrMessage(
            payload=rdfvalue.RDFString("foo/bar"),
            age=(result.age - (self.handler.MAX_RECORDS_TO_CHECK - i + 1) *
                 rdfvalue.Duration("1s")),
            source=self.client_id)
        results.Add(
            wrong_result, timestamp=wrong_result.age, mutation_pool=pool)

    return result

  # The whole MAX_RECORDS approach is specific to AFF4 table-scanning.
  @db_test_lib.LegacyDataStoreOnly
  def testRaisesIfResultIsAfterMaxRecordsAfterTimestamp(self):
    original_result = self._FillInStubResults()

    args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path=self.aff4_file_path,
        timestamp=original_result.age -
        (self.handler.MAX_RECORDS_TO_CHECK + 1) * rdfvalue.Duration("1s"))

    with self.assertRaises(hunt_plugin.HuntFileNotFoundError):
      self.handler.Handle(args, token=self.token)

  # The whole MAX_RECORDS approach is specific to AFF4 table-scanning.
  @db_test_lib.LegacyDataStoreOnly
  def testReturnsResultIfWithinMaxRecordsAfterTimestamp(self):
    original_result = self._FillInStubResults()

    args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path=self.aff4_file_path,
        timestamp=original_result.age -
        self.handler.MAX_RECORDS_TO_CHECK * rdfvalue.Duration("1s"))

    self.handler.Handle(args, token=self.token)

  def testRaisesIfResultFileDoesNotExist(self):
    if data_store.RelationalDBEnabled():
      results = data_store.REL_DB.ReadHuntResults(self.hunt_id, 0, 1)
      original_result = results[0]

      with test_lib.FakeTime(original_result.timestamp -
                             rdfvalue.Duration("1s")):
        wrong_result = original_result.Copy()
        payload = wrong_result.payload
        payload.stat_entry.pathspec.path += "blah"
        data_store.REL_DB.WriteFlowResults([wrong_result])

      wrong_result_timestamp = wrong_result.timestamp
    else:
      results = implementation.GRRHunt.ResultCollectionForHID(
          self.hunt_urn, token=self.token)
      original_result = results[0]

      with data_store.DB.GetMutationPool() as pool:
        wrong_result = original_result.Copy()
        payload = wrong_result.payload
        payload.stat_entry.pathspec.path += "blah"
        wrong_result.payload = payload
        wrong_result.age -= rdfvalue.Duration("1s")

        results.Add(
            wrong_result, timestamp=wrong_result.age, mutation_pool=pool)

      wrong_result_timestamp = wrong_result.age

    args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path=self.aff4_file_path + "blah",
        timestamp=wrong_result_timestamp)

    with self.assertRaises(hunt_plugin.HuntFileNotFoundError):
      self.handler.Handle(args, token=self.token)

  # There is no notion of "empty stream" in the new datastore model.
  @db_test_lib.LegacyDataStoreOnly
  def testRaisesIfResultIsEmptyStream(self):
    original_results = implementation.GRRHunt.ResultCollectionForHID(
        self.hunt_urn, token=self.token)
    original_result = original_results[0]

    urn = original_result.payload.stat_entry.AFF4Path(self.client_id)
    aff4.FACTORY.Delete(urn, token=self.token)
    with aff4.FACTORY.Create(urn, aff4_type=aff4_grr.VFSFile, token=self.token):
      pass

    args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path=self.aff4_file_path,
        timestamp=original_result.age)

    with self.assertRaises(hunt_plugin.HuntFileNotFoundError):
      self.handler.Handle(args, token=self.token)

  def testReturnsBinaryStreamIfResultFound(self):
    if data_store.RelationalDBEnabled():
      results = data_store.REL_DB.ReadHuntResults(self.hunt_id, 0, 1)
      timestamp = results[0].timestamp
    else:
      results = implementation.GRRHunt.ResultCollectionForHID(
          self.hunt_urn, token=self.token)
      timestamp = results[0].age

    args = hunt_plugin.ApiGetHuntFileArgs(
        hunt_id=self.hunt_id,
        client_id=self.client_id,
        vfs_path=self.aff4_file_path,
        timestamp=timestamp)

    result = self.handler.Handle(args, token=self.token)
    self.assertTrue(hasattr(result, "GenerateContent"))
    self.assertEqual(result.content_length,
                     results[0].payload.stat_entry.st_size)


@db_test_lib.DualDBTest
class ApiListHuntOutputPluginLogsHandlerTest(api_test_lib.ApiCallHandlerTest,
                                             hunt_test_lib.StandardHuntTestMixin
                                            ):
  """Test for ApiListHuntOutputPluginLogsHandler."""

  def setUp(self):
    super(ApiListHuntOutputPluginLogsHandlerTest, self).setUp()

    self.client_ids = self.SetupClients(5)
    self.handler = hunt_plugin.ApiListHuntOutputPluginLogsHandler()
    self.output_plugins = [
        rdf_output_plugin.OutputPluginDescriptor(
            plugin_name=test_plugins.DummyHuntTestOutputPlugin.__name__,
            plugin_args=test_plugins.DummyHuntTestOutputPlugin.args_type(
                filename_regex="foo")),
        rdf_output_plugin.OutputPluginDescriptor(
            plugin_name=test_plugins.DummyHuntTestOutputPlugin.__name__,
            plugin_args=test_plugins.DummyHuntTestOutputPlugin.args_type(
                filename_regex="bar"))
    ]

  def RunHuntWithOutputPlugins(self, output_plugins):
    hunt_urn = self.StartHunt(
        description="the hunt", output_plugins=output_plugins)

    for client_id in self.client_ids:
      self.RunHunt(client_ids=[client_id], failrate=-1)
      self.ProcessHuntOutputPlugins()

    return hunt_urn

  def testReturnsLogsWhenJustOnePlugin(self):
    hunt_urn = self.RunHuntWithOutputPlugins([self.output_plugins[0]])
    result = self.handler.Handle(
        hunt_plugin.ApiListHuntOutputPluginLogsArgs(
            hunt_id=hunt_urn.Basename(),
            plugin_id=test_plugins.DummyHuntTestOutputPlugin.__name__ + "_0"),
        token=self.token)

    self.assertEqual(result.total_count, 5)
    self.assertLen(result.items, 5)

  def testReturnsLogsWhenMultiplePlugins(self):
    hunt_urn = self.RunHuntWithOutputPlugins(self.output_plugins)
    result = self.handler.Handle(
        hunt_plugin.ApiListHuntOutputPluginLogsArgs(
            hunt_id=hunt_urn.Basename(),
            plugin_id=test_plugins.DummyHuntTestOutputPlugin.__name__ + "_1"),
        token=self.token)

    self.assertEqual(result.total_count, 5)
    self.assertLen(result.items, 5)

  def testSlicesLogsWhenJustOnePlugin(self):
    hunt_urn = self.RunHuntWithOutputPlugins([self.output_plugins[0]])
    result = self.handler.Handle(
        hunt_plugin.ApiListHuntOutputPluginLogsArgs(
            hunt_id=hunt_urn.Basename(),
            offset=2,
            count=2,
            plugin_id=test_plugins.DummyHuntTestOutputPlugin.__name__ + "_0"),
        token=self.token)

    self.assertEqual(result.total_count, 5)
    self.assertLen(result.items, 2)

  def testSlicesLogsWhenMultiplePlugins(self):
    hunt_urn = self.RunHuntWithOutputPlugins(self.output_plugins)
    result = self.handler.Handle(
        hunt_plugin.ApiListHuntOutputPluginLogsArgs(
            hunt_id=hunt_urn.Basename(),
            offset=2,
            count=2,
            plugin_id=test_plugins.DummyHuntTestOutputPlugin.__name__ + "_1"),
        token=self.token)

    self.assertEqual(result.total_count, 5)
    self.assertLen(result.items, 2)


@db_test_lib.DualDBTest
class ApiModifyHuntHandlerTest(api_test_lib.ApiCallHandlerTest,
                               hunt_test_lib.StandardHuntTestMixin):
  """Test for ApiModifyHuntHandler."""

  def setUp(self):
    super(ApiModifyHuntHandlerTest, self).setUp()

    self.handler = hunt_plugin.ApiModifyHuntHandler()

    if data_store.RelationalDBEnabled():
      self.hunt_id = self.CreateHunt(description="the hunt")
    else:
      self.hunt_obj = self.CreateHunt(description="the hunt")
      self.hunt_urn = self.hunt_obj.urn
      self.hunt_id = self.hunt_urn.Basename()

    self.args = hunt_plugin.ApiModifyHuntArgs(hunt_id=self.hunt_id)

  def testDoesNothingIfArgsHaveNoChanges(self):
    if data_store.RelationalDBEnabled():
      before = hunt_plugin.ApiHunt().InitFromHuntObject(
          data_store.REL_DB.ReadHuntObject(self.hunt_id))
    else:
      before = hunt_plugin.ApiHunt().InitFromAff4Object(
          aff4.FACTORY.Open(self.hunt_urn, token=self.token))

    self.handler.Handle(self.args, token=self.token)

    if data_store.RelationalDBEnabled():
      after = hunt_plugin.ApiHunt().InitFromHuntObject(
          data_store.REL_DB.ReadHuntObject(self.hunt_id))
    else:
      after = hunt_plugin.ApiHunt().InitFromAff4Object(
          aff4.FACTORY.Open(self.hunt_urn, token=self.token))

    self.assertEqual(before, after)

  def testRaisesIfStateIsSetToNotStartedOrStopped(self):
    self.args.state = "COMPLETED"
    with self.assertRaises(hunt_plugin.InvalidHuntStateError):
      self.handler.Handle(self.args, token=self.token)

  def testRaisesWhenStartingHuntInTheWrongState(self):
    if data_store.RelationalDBEnabled():
      hunt.StartHunt(self.hunt_id)
      hunt.StopHunt(self.hunt_id)
    else:
      self.hunt_obj.Run()
      self.hunt_obj.Stop()

    self.args.state = "STARTED"
    with self.assertRaises(hunt_plugin.HuntNotStartableError):
      self.handler.Handle(self.args, token=self.token)

  def testRaisesWhenStoppingHuntInTheWrongState(self):
    if data_store.RelationalDBEnabled():
      hunt.StartHunt(self.hunt_id)
      hunt.StopHunt(self.hunt_id)
    else:
      self.hunt_obj.Run()
      self.hunt_obj.Stop()

    self.args.state = "STOPPED"
    with self.assertRaises(hunt_plugin.HuntNotStoppableError):
      self.handler.Handle(self.args, token=self.token)

  def testStartsHuntCorrectly(self):
    self.args.state = "STARTED"
    self.handler.Handle(self.args, token=self.token)

    if data_store.RelationalDBEnabled():
      h = data_store.REL_DB.ReadHuntObject(self.hunt_id)
      self.assertEqual(h.hunt_state, h.HuntState.STARTED)
    else:
      hunt_obj = aff4.FACTORY.Open(self.hunt_urn, token=self.token)
      self.assertEqual(hunt_obj.Get(hunt_obj.Schema.STATE), "STARTED")

  def testStopsHuntCorrectly(self):
    self.args.state = "STOPPED"
    self.handler.Handle(self.args, token=self.token)

    if data_store.RelationalDBEnabled():
      h = data_store.REL_DB.ReadHuntObject(self.hunt_id)
      self.assertEqual(h.hunt_state, h.HuntState.STOPPED)
    else:
      hunt_obj = aff4.FACTORY.Open(self.hunt_urn, token=self.token)
      self.assertEqual(hunt_obj.Get(hunt_obj.Schema.STATE), "STOPPED")

  def testRaisesWhenModifyingHuntInNonPausedState(self):
    if data_store.RelationalDBEnabled():
      hunt.StartHunt(self.hunt_id)
    else:
      self.hunt_obj.Run()

    self.args.client_rate = 100
    with self.assertRaises(hunt_plugin.HuntNotModifiableError):
      self.handler.Handle(self.args, token=self.token)

  def testModifiesHuntCorrectly(self):
    self.args.client_rate = 100
    self.args.client_limit = 42
    self.args.duration = rdfvalue.Duration("1d")

    self.handler.Handle(self.args, token=self.token)

    if data_store.RelationalDBEnabled():
      after = hunt_plugin.ApiHunt().InitFromHuntObject(
          data_store.REL_DB.ReadHuntObject(self.hunt_id))
    else:
      after = hunt_plugin.ApiHunt().InitFromAff4Object(
          aff4.FACTORY.Open(self.hunt_urn, token=self.token))

    self.assertEqual(after.client_rate, 100)
    self.assertEqual(after.client_limit, 42)
    self.assertEqual(after.duration, rdfvalue.Duration("1d"))

  # New datastore implementation has a slightly different behavior.
  # client_rate/limit modification is applied before an attempt
  # to change the state is made. These modifications stay even
  # if the state change attempt fails.
  @db_test_lib.LegacyDataStoreOnly
  def testDoesNotModifyHuntIfStateChangeFails(self):
    self.args.client_limit = 42
    self.args.state = "COMPLETED"
    with self.assertRaises(hunt_plugin.InvalidHuntStateError):
      self.handler.Handle(self.args, token=self.token)

    if data_store.RelationalDBEnabled():
      after = hunt_plugin.ApiHunt().InitFromHuntObject(
          data_store.REL_DB.ReadHuntObject(self.hunt_id))
    else:
      after = hunt_plugin.ApiHunt().InitFromAff4Object(
          aff4.FACTORY.Open(self.hunt_urn, token=self.token))
    self.assertNotEqual(after.client_limit, 42)


@db_test_lib.DualDBTest
class ApiDeleteHuntHandlerTest(api_test_lib.ApiCallHandlerTest,
                               hunt_test_lib.StandardHuntTestMixin):
  """Test for ApiDeleteHuntHandler."""

  def setUp(self):
    super(ApiDeleteHuntHandlerTest, self).setUp()

    self.handler = hunt_plugin.ApiDeleteHuntHandler()

    if data_store.RelationalDBEnabled():
      self.hunt_id = self.CreateHunt(description="the hunt")
    else:
      self.hunt_obj = self.CreateHunt(description="the hunt")
      self.hunt_id = self.hunt_obj.urn.Basename()

    self.args = hunt_plugin.ApiDeleteHuntArgs(hunt_id=self.hunt_id)

  def testRaisesIfHuntNotFound(self):
    with self.assertRaises(hunt_plugin.HuntNotFoundError):
      self.handler.Handle(
          hunt_plugin.ApiDeleteHuntArgs(hunt_id="H:123456"), token=self.token)

  def testRaisesIfHuntIsRunning(self):
    if data_store.RelationalDBEnabled():
      hunt.StartHunt(self.hunt_id)
    else:
      self.hunt_obj.Run()

    with self.assertRaises(hunt_plugin.HuntNotDeletableError):
      self.handler.Handle(self.args, token=self.token)

  def testDeletesHunt(self):
    self.handler.Handle(self.args, token=self.token)

    if data_store.RelationalDBEnabled():
      with self.assertRaises(db.UnknownHuntError):
        data_store.REL_DB.ReadHuntObject(self.hunt_id)
    else:
      with self.assertRaises(aff4.InstantiationError):
        aff4.FACTORY.Open(
            self.hunt_obj.urn,
            aff4_type=implementation.GRRHunt,
            token=self.token)


@db_test_lib.DualDBTest
class ApiGetExportedHuntResultsHandlerTest(test_lib.GRRBaseTest,
                                           hunt_test_lib.StandardHuntTestMixin):

  def setUp(self):
    super(ApiGetExportedHuntResultsHandlerTest, self).setUp()

    self.handler = hunt_plugin.ApiGetExportedHuntResultsHandler()

    hunt_urn = self.StartHunt(
        flow_runner_args=rdf_flow_runner.FlowRunnerArgs(
            flow_name=flow_test_lib.DummyFlowWithSingleReply.__name__),
        client_rate=0)
    self.hunt_id = hunt_urn.Basename()

    self.client_ids = self.SetupClients(5)
    # Ensure that clients are processed sequentially - this way the test won't
    # depend on the order of results in the collection (which is normally
    # random).
    for cid in self.client_ids:
      self.RunHunt(client_ids=[cid], failrate=-1)

  def testWorksCorrectlyWithTestOutputPluginOnFlowWithSingleResult(self):
    result = self.handler.Handle(
        hunt_plugin.ApiGetExportedHuntResultsArgs(
            hunt_id=self.hunt_id,
            plugin_name=test_plugins.TestInstantOutputPlugin.plugin_name),
        token=self.token)

    chunks = list(result.GenerateContent())

    self.assertListEqual(chunks, [
        "Start: aff4:/hunts/%s" % self.hunt_id,
        "Values of type: RDFString",
        "First pass: oh (source=%s)" % self.client_ids[0],
        "First pass: oh (source=%s)" % self.client_ids[1],
        "First pass: oh (source=%s)" % self.client_ids[2],
        "First pass: oh (source=%s)" % self.client_ids[3],
        "First pass: oh (source=%s)" % self.client_ids[4],
        "Second pass: oh (source=%s)" % self.client_ids[0],
        "Second pass: oh (source=%s)" % self.client_ids[1],
        "Second pass: oh (source=%s)" % self.client_ids[2],
        "Second pass: oh (source=%s)" % self.client_ids[3],
        "Second pass: oh (source=%s)" % self.client_ids[4],
        "Finish: aff4:/hunts/%s" % self.hunt_id,
    ])


def main(argv):
  test_lib.main(argv)


if __name__ == "__main__":
  app.run(main)
