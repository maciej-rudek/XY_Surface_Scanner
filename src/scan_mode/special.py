class Once:
    
    stop = True
    
    def Reset_once():
        Once.stop = False
    
    def Run_once(f):
        def wrapper(*args, **kwargs):
            if not Once.stop:
                Once.stop = True
                return f(*args, **kwargs)
        Once.stop = False
        return wrapper