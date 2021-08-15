# logging configure_logger(app)
class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.request_id = None
        record.remote_addr = None
        record.url = None
        if has_request_context():
            record.request_id = g.request_id
            record.remote_addr = request.remote_addr
            record.url = request.url
        return super().format(record)


formatter = RequestFormatter(
    fmt=app.config['LOG_FORMAT'],
    datefmt=app.config['LOG_FORMAT_DATE']
)
default_handler.setFormatter(formatter)
app.logger.setLevel(logging.DEBUG)
