def with_envelope(func):
    func._with_envelope = True
    return func
