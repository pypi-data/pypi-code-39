import hghave


@hghave.check("clang-format", "clang-format C code formatter")
def has_clang_format():
    m = hghave.matchoutput("clang-format --version", br"clang-format version (\d)")
    # style changed somewhere between 4.x and 6.x
    return m and int(m.group(1)) >= 6


@hghave.check("black", "black Python code formatter")
def has_black_format():
    m = hghave.matchoutput("which black", br"black")
    return bool(m)


@hghave.check("yapf", "yapf Python code formatter")
def has_yapf_format():
    m = hghave.matchoutput("yapf --version", br"yapf ([\w]+)")
    return bool(m)


@hghave.check("gofmt", "gofmt Go code formatter")
def has_gofmt_format():
    m = hghave.matchoutput("gofmt --help", br"usage: gofmt.*", ignorestatus=True)
    return bool(m)


@hghave.check("rustfmt", "rustfmt Rust code formatter")
def has_rustfmt_format():
    m = hghave.matchoutput("rustfmt --version", br"rustfmt ([\w]+)")
    return bool(m)


@hghave.check("prettier", "prettier javascript code formatter")
def has_prettier_format():
    m = hghave.matchoutput("prettier --version", br"[\d.]+")
    return bool(m)
