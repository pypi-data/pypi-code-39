


def weblog_tex(weblog, threshold_requests_per_session,weblog_columns_dict):
    """
    Write in latex file weblog important caracteristics
    """
    f = open("../Latex_file/CL_variables.tex", "w")
    list_of_log_pages=list(set(weblog[weblog_columns_dict['requested_page_column']].unique())|\
                           set(weblog[weblog_columns_dict['referrer_page_column']].unique()))
    f.write("\n% 1. General variables")
    f.write("\n\\newcommand{\\%s}{%d}"%('ThresholdRequestsPerSessions',threshold_requests_per_session))
    f.write("\n\\newcommand{\\%s}{%d}"%('TotalNumberRequests',weblog.shape[0]))
    f.write("\n\\newcommand{\\%s}{%d}"%('TotalNumberUsers',len(weblog[weblog_columns_dict['user_id_column']].unique())))
    f.write("\n\\newcommand{\\%s}{%d}"%('TotalNumberSessions',len(weblog.session_id.unique())))
    f.write("\n\\newcommand{\\%s}{%d}"%('TotalNumberPages',len(list_of_log_pages)))
    f.write("\n\\newcommand{\\%s}{%s}"%('LogFirstTimestamp',weblog[weblog_columns_dict['timestamp_column']].min()))
    f.write("\n\\newcommand{\\%s}{%s}"%('LogLastTimestamp',weblog[weblog_columns_dict['timestamp_column']].max()))
    return f;