from datetime import datetime
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from wrktoolbox.reports.writer import ReportWriter
from wrktoolbox.results import SuiteReport
from wrktoolbox.wrkoutput import BenchmarkOutput
from wrktoolbox.benchmarks import PerformanceGoalResult
from enum import IntEnum


class Sizes(IntEnum):

    GUID = 40
    IP = 15
    DATETIME = 20
    LOCATION = 20
    DATE = 10
    URL = 40


class XLSXWriter(ReportWriter):

    type_name = 'xlsx'

    def __init__(self, file_name: str = None):
        if not file_name:
            file_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '-output.xlsx'
        self.file_name = file_name
        self.workbook = Workbook(file_name, {'strings_to_urls': False})
        self.section = self.workbook.add_format({
            'bold': True,
            'bg_color': '#9fcbf1'
        })
        self.error = self.workbook.add_format({
            'bold': True,
            'bg_color': '#ef2854'
        })
        self.success = self.workbook.add_format({
            'bold': True,
            'bg_color': '#29ef28'
        })
        self.date_format = self.workbook.add_format({'num_format': 'yyyy-mm-dd'})
        self.datetime_format = self.workbook.add_format({'num_format': 'yyyy-mm-dd HH:MM:SS'})
        self.row_format1 = self.workbook.add_format({'bg_color': '#FFFFFF'})
        self.row_format2 = self.workbook.add_format({'bg_color': '#f0f8ff'})
        self.suites = self._prepare_suites_sheet()
        self.goals = self._prepare_goals_sheet()
        self.benchmarks = self._prepare_benchmarks_sheet()
        self.suites_row = 1
        self.goals_row = 1
        self.benchmarks_row = 1
        self._configured_goals = []

    def _prepare_suites_sheet(self):
        workbook = self.workbook
        section = self.section
        worksheet = workbook.add_worksheet('suites')
        worksheet.set_column(0, 0, Sizes.GUID)
        worksheet.set_column(1, 1, Sizes.LOCATION)
        worksheet.set_column(2, 2, Sizes.IP)
        worksheet.set_column(3, 4, Sizes.DATETIME)

        worksheet.write('A1', 'Suite id', section)
        worksheet.write('B1', 'Location', section)
        worksheet.write('C1', 'Client IP', section)
        worksheet.write('D1', 'Start time', section)
        worksheet.write('E1', 'End time', section)
        return worksheet

    def _prepare_goals_sheet(self) -> Worksheet:
        workbook = self.workbook
        section = self.section
        worksheet = workbook.add_worksheet('goals')

        worksheet.write('A1', 'Suite id', section)
        worksheet.write('B1', 'Type', section)
        worksheet.write('C1', 'Description', section)
        return worksheet

    def _write_goals(self, report: SuiteReport):
        suite = report.suite
        worksheet = self.goals
        row = self.goals_row

        if report.suite.goals is None:
            return

        for goal in report.suite.goals:
            worksheet.write(row, 0, suite.id)
            worksheet.write(row, 1, goal.get_class_name())
            worksheet.write(row, 2, repr(goal))
            row += 1

        self.goals_row = row

    def _prepare_benchmarks_sheet(self):
        workbook = self.workbook
        section = self.section
        worksheet = workbook.add_worksheet('benchmarks')
        worksheet.set_column(0, 1, Sizes.GUID)
        worksheet.set_column(2, 2, Sizes.URL)
        worksheet.set_column(3, 4, Sizes.DATETIME)

        worksheet.write('A1', 'Id', section)
        worksheet.write('B1', 'Suite id', section)
        worksheet.write('C1', 'Location', section)
        worksheet.write('D1', 'URL', section)
        worksheet.write('E1', 'Start time', section)
        worksheet.write('F1', 'End time', section)
        worksheet.write('G1', 'Reqs/s', section)
        worksheet.write('H1', 'Avg latency (ms)', section)
        worksheet.write('I1', 'Stdev latency (ms)', section)
        worksheet.write('J1', 'Max latency (ms)', section)
        worksheet.write('K1', 'Has errors', section)
        worksheet.write('L1', 'Non-2xx or 3xx responses', section)
        worksheet.write('M1', 'Socket connect errors', section)
        worksheet.write('N1', 'Socket timeout errors', section)
        worksheet.write('O1', 'Socket read errors', section)
        worksheet.write('P1', 'Socket write errors', section)

        return worksheet

    def _write_benchmarks_goals_columns(self,
                                        location,
                                        output: BenchmarkOutput,
                                        worksheet: Worksheet,
                                        row: int,
                                        col: int):
        for goal_result in output.goals_results:  # type: PerformanceGoalResult
            worksheet.write_comment(row, col, goal_result.goal + f' {location}')

            if goal_result.success:
                worksheet.write(row, col, 'Success', self.success)
            else:
                worksheet.write(row, col, 'Fail', self.error)
            col += 1
        return col

    def write(self, report: SuiteReport):
        worksheet = self.suites
        suite = report.suite
        row = self.suites_row

        worksheet.write(row, 0, suite.id)
        worksheet.write(row, 1, suite.location)
        worksheet.write(row, 2, suite.public_ip)
        worksheet.write_datetime(row, 3, suite.start_time, self.datetime_format)
        worksheet.write_datetime(row, 4, suite.end_time, self.datetime_format)
        row += 1

        self._write_goals(report)

        self.suites_row = row

    def write_output(self, report: SuiteReport, output: BenchmarkOutput):
        worksheet = self.benchmarks
        row = self.benchmarks_row
        location = report.suite.location

        row_format = self.row_format1 if row % 2 == 0 else self.row_format2
        worksheet.set_row(row, cell_format=row_format)

        worksheet.write(row, 0, output.id)
        worksheet.write(row, 1, output.suite_id)
        worksheet.write(row, 2, location)
        worksheet.write(row, 3, output.url)
        worksheet.write_datetime(row, 4, output.start_time, self.datetime_format)
        worksheet.write_datetime(row, 5, output.end_time, self.datetime_format)
        worksheet.write_number(row, 6, output.requests_per_second)
        worksheet.write_number(row, 7, output.latency.avg.ms)
        worksheet.write_number(row, 8, output.latency.stdev.ms)
        worksheet.write_number(row, 9, output.latency.max.ms)
        if output.has_errors:
            worksheet.write(row, 10, 'Yes', self.error)
        else:
            worksheet.write(row, 10, 'No', self.success)
        worksheet.write_number(row, 11, output.not_successful_responses)

        col = 12
        if output.socket_errors:
            worksheet.write_number(row, col, output.socket_errors.connect_errors)
            worksheet.write_number(row, col + 1, output.socket_errors.timeout_errors)
            worksheet.write_number(row, col + 2, output.socket_errors.read_errors)
            worksheet.write_number(row, col + 3, output.socket_errors.write_errors)
        else:
            worksheet.write_number(row, col, 0)
            worksheet.write_number(row, col + 1, 0)
            worksheet.write_number(row, col + 2, 0)
            worksheet.write_number(row, col + 3, 0)
        col = 16

        percentiles = output.latency_distribution.percentiles

        for key, value in percentiles.items():
            worksheet.write_number(row, col, value.ms)
            worksheet.write_comment(row, col, f'{key}% percentile (ms) {location}')
            col += 1

        self._write_benchmarks_goals_columns(location, output, worksheet, row, col)
        self.benchmarks_row = row + 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.workbook.close()
