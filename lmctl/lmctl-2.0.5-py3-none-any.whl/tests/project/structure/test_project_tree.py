import unittest
from lmctllib.project.structure import ProjectTree, BuildTree, PackageWrapperTree, VnfcsTree, ServiceBehaviourTree, DescriptorTree

class TestProjectTree(unittest.TestCase):

    def setUp(self):
        self.project_tree = ProjectTree('testing')

    def testProjectFile(self):
        self.assertEqual(self.project_tree.projectFile(), 'testing/lmproject.yml')

    def testDirectory(self):
        self.assertEqual(self.project_tree.directory(), 'testing')

    def testBackupDirectory(self):
        self.assertEqual(self.project_tree.backupDirectory(), 'testing/_lmctl/_prepull')

    def testBackup(self):
        backup_tree = self.project_tree.backup()
        self.assertEqual(backup_tree.directory(), self.project_tree.backupDirectory())

    def testBuild(self):
        build_tree = self.project_tree.build()
        self.assertIsInstance(build_tree, BuildTree)
        self.assertEqual(build_tree.directory(), 'testing/_lmctl/_build')

    def testPushWorkspace(self):
        push_tree = self.project_tree.pushWorkspace()
        self.assertIsInstance(push_tree, PackageWrapperTree)
        self.assertEqual(push_tree.directory(), 'testing/_lmctl/_pushpkg')

    def testVnfcs(self):
        vnfc_tree = self.project_tree.vnfcs()
        self.assertIsInstance(vnfc_tree, VnfcsTree)
        self.assertEqual(vnfc_tree.directory(), 'testing/VNFCs')

    def testServiceBehaviour(self):
        service_behaviour_tree = self.project_tree.serviceBehaviour()
        self.assertIsInstance(service_behaviour_tree, ServiceBehaviourTree)
        self.assertEqual(service_behaviour_tree.directory(), 'testing/Behaviour')

    def testServiceDescriptor(self):
        descriptor_tree = self.project_tree.serviceDescriptor()
        self.assertIsInstance(descriptor_tree, DescriptorTree)
        self.assertEqual(descriptor_tree.directory(), 'testing/Descriptor')
