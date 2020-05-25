import flask_login


def conv_t(value):
    return flask_login.current_user.temperature.convert(value)


def conv_p(value):
    return flask_login.current_user.pressure.convert(value)


def conv_f(value):
    return flask_login.current_user.consumption.convert(value)


def deconv_t(value):
    return flask_login.current_user.temperature.deconvert(value)


def deconv_p(value):
    return flask_login.current_user.pressure.deconvert(value)


def deconv_f(value):
    return flask_login.current_user.consumption.deconvert(value)
