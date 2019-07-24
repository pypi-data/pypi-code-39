# from claim.models import ClaimDiagnosisCode
# from insuree.models import Gender
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from api_fhir.tests import GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiUpdateTestMixin, \
#     FhirApiCreateTestMixin, LocationTestMixin, PractitionerTestMixin, FhirApiDeleteTestMixin, PatientTestMixin
# from api_fhir.utils import TimeUtils
#
#
# class ClaimAPITests(GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiCreateTestMixin,
#                     FhirApiUpdateTestMixin, FhirApiDeleteTestMixin, APITestCase):
#
#     base_url = '/api_fhir/Claim/'
#     _test_json_path = "/test/test_claim.json"
#     _TEST_LOCATION_CODE = "12345678"
#     _TEST_CLAIM_ADMIN_CODE = "1234abcd"
#     _TEST_INSUREE_CODE = "TEST_CHF_ID"
#     _TEST_GENDER_CODE = "M"
#     _TEST_ADMIN_USER_ID = 1
#
#     def setUp(self):
#         super(ClaimAPITests, self).setUp()
#
#     def verify_updated_obj(self, updated_obj):
#         # self.assertTrue(isinstance(updated_obj, PractitionerRole))
#         # self.assertEqual(self._TEST_UPDATED_CLAIM_ADMIN_CODE,
#         #                  PractitionerConverter.get_resource_id_from_reference(updated_obj.practitioner))
#         pass
#
#     def update_resource(self, data):
#         # new_practitioner = self._create_and_save_claim_admin(self._TEST_UPDATED_CLAIM_ADMIN_CODE)
#         # data['practitioner'] = PractitionerConverter.build_fhir_resource_reference(new_practitioner).toDict()
#         pass
#
#     def create_dependencies(self):
#         gender = Gender()
#         gender.code = self._TEST_GENDER_CODE
#         gender.save()
#         main_icd = ClaimDiagnosisCode()
#         main_icd.code = "ICD_CD"
#         main_icd.validity_from = TimeUtils.now()
#         main_icd.audit_user_id = self._TEST_ADMIN_USER_ID
#         main_icd.save()
#         self._create_and_save_hf()
#         self._create_and_save_claim_admin()
#         self._create_and_save_insuree()
#
#     def _create_and_save_hf(self):
#         imis_hf = LocationTestMixin().create_test_imis_instance()
#         imis_hf.validity_from = TimeUtils.now()
#         imis_hf.offline = False
#         imis_hf.audit_user_id = self._TEST_ADMIN_USER_ID
#         imis_hf.code = self._TEST_LOCATION_CODE
#         imis_hf.save()
#         return imis_hf
#
#     def _create_and_save_claim_admin(self):
#         claim_admin = PractitionerTestMixin().create_test_imis_instance()
#         claim_admin.audit_user_id = self._TEST_ADMIN_USER_ID
#         claim_admin.code = self._TEST_CLAIM_ADMIN_CODE
#         claim_admin.save()
#         return claim_admin
#
#     def _create_and_save_insuree(self):
#         imis_insuree = PatientTestMixin().create_test_imis_instance()
#         imis_insuree.head = False
#         imis_insuree.card_issued = False
#         imis_insuree.validity_from = TimeUtils.now()
#         imis_insuree.audit_user_id = self._TEST_ADMIN_USER_ID
#         imis_insuree.chf_id = self._TEST_INSUREE_CODE
#         imis_insuree.save()
#         return imis_insuree
#
#     def verify_deleted_response(self, response):
#         self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
#
