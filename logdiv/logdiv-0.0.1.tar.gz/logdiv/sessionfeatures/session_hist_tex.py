

def session_hist_tex(f, session_data,threshold_requests_per_session):
    """
    Write session caracteristics in latex file
    """
    digit_dic={'0':'Zero','1':'One','2':'Two','3':'Three','4':'Four','5':'Five','6':'Six','7':'Seven','8':'Eight','9':'Nine'}
    f.write("\n% 2. Histogram sessions with given requests")
    f.write("\n\\newcommand{\\%s}{%d}"%('ThresholdRequestsPerSession',threshold_requests_per_session))
    for reqs in range(1,threshold_requests_per_session+1):
        num_of_sessions=session_data[session_data.requests==reqs].shape[0]
        pc_of_sessions=100.0*num_of_sessions/session_data.shape[0]
        f.write("\n\\newcommand{\\%s}{%d}"%('SessionsWith%sRequests'%digit_dic[str(reqs)],num_of_sessions))
        f.write("\n\\newcommand{\\%s}{%.1f}"%('PCSessionsWith%sRequests'%digit_dic[str(reqs)],pc_of_sessions))
    num_of_sessions=session_data[session_data.requests>threshold_requests_per_session].shape[0]
    pc_of_sessions=100.0*num_of_sessions/session_data.shape[0]
    f.write("\n\\newcommand{\\%s}{%d}"%('SessionsWithMT%sRequests'%digit_dic[str(threshold_requests_per_session)],num_of_sessions))
    f.write("\n\\newcommand{\\%s}{%.1f}"%('PCSessionsWithMT%sRequests'%digit_dic[str(threshold_requests_per_session)],pc_of_sessions))
    return f;

