try:
    from service.bangsheng.loan_risk import LoanRisk
    from service.bangsheng.lend_detail import LendDetail
    from service.bangsheng.loan_detail import LoanDetail
    from service.bangsheng.overdue_detail import OverdueDetail
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.bangsheng.loan_risk import LoanRisk
    from pysubway.service.bangsheng.lend_detail import LendDetail
    from pysubway.service.bangsheng.loan_detail import LoanDetail
    from pysubway.service.bangsheng.overdue_detail import OverdueDetail