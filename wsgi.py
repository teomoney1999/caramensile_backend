from application import app
import logging

# if __name__ != "__main__": 
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     app.logger.handlers = gunicorn_logger.handlers
#     app.logger.setLevel(gunicorn_logger.level)
    
@app.route('/default')
def default_route():
    """Default route"""
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return 'hello world'
    
if __name__ == "__main__": 
    # run_app()
    app.run()
    
# /root/caramensile_be/repo

# systemctl daemon-reload
# systemctl restart caramensile_be.service
# journalctl -u caramensile_be.service -f
# /etc/systemd/system/caramensile_be.service 