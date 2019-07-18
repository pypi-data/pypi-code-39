from keeper_cnab240.banks.bank import Bank
from keeper_cnab240.banks.Itau.file_header import FileHeader
from keeper_cnab240.banks.Itau.file_footer import FileFooter
from keeper_cnab240.banks.Itau.payment_methods import PaymentMethods
from keeper_cnab240.banks.Itau.payment_status import PaymentStatus
from keeper_cnab240.banks.Itau.segments.A import SegmentA, SegmentAFooter, SegmentAHeader
from keeper_cnab240.banks.Itau.segments.ANF import SegmentANF
from keeper_cnab240.banks.Itau.segments.J import SegmentJ, SegmentJFooter, SegmentJHeader
from keeper_cnab240.banks.Itau.segments.J52 import SegmentJ52


class Itau(Bank):
    def __init__(self):
        super().__init__('Itaú', 'Itau', 341, 13, 1, 'payment_way', payments_status=PaymentStatus)

        # Segment A
        super().set_segment('AHeader', SegmentAHeader, PaymentMethods.segment_a_anf(), shipping_only=True)
        super().set_segment('A', SegmentA, PaymentMethods.segment_a())
        super().set_segment('ANF', SegmentANF, PaymentMethods.segment_anf(), 'A')
        super().set_segment('AFooter', SegmentAFooter, PaymentMethods.segment_a_anf(), shipping_only=True)

        # Segment J
        super().set_segment('JHeader', SegmentJHeader, PaymentMethods.segment_j(), shipping_only=True)
        super().set_segment('J', SegmentJ, PaymentMethods.segment_j())
        super().set_segment('J52', SegmentJ52, PaymentMethods.segment_j(), shipping_only=True)
        super().set_segment('JFooter', SegmentJFooter, PaymentMethods.segment_j(), shipping_only=True)
    
    def get_file_header(self):
        file_header = FileHeader()
        file_header.set_bank(self)
        return file_header
    
    def get_file_footer(self):
        file_footer = FileFooter()
        file_footer.set_bank(self)
        return file_footer
    
    @staticmethod
    def get_company_document_id(document_type):
        return 2 if document_type == 'cnpj' else 1
