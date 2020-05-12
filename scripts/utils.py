def print_box(text, logger = None):
    """
    prints a box with text in the middle  
    """
    height = 5
    width = 50
    if logger:
        for i in range(height):
            if i in [0]:
                logger.info("# " * width)
            elif i in [(height - 1)]:
                logger.info("# " * width)
            elif i in [2]:
                logger.info(text.center(100, " "))
            else:
                logger.info("#" + " " * width - 2 + " #")
        logger.info("")

    else:
        for i in range(height):
            if i in [0]:
                print("# " * width)
            elif i in [(height - 1)]:
                print("# " * width)
            elif i in [2]:
                print(text.center(100, " "))
            else:
                print("#" + " " * (width * 2 - 4) + " #")
        print("")

def td_format(td_object):
    """
    formats time delta objects into a human readable format
    """
    seconds = int(td_object.total_seconds())
    periods = [
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 30),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = "s" if period_value > 1 else ""
            strings.append(f"%s %s%s" % (period_value, period_name, has_s))
    if len(strings) == 0:
        strings.append("< 1 second")
    return ", ".join(strings)

def time_this_function(name):
    '''
    wrapper function to time a function
    '''
    def wrap(original_function):
        def wrapped_f(*args, **kwargs):
            import datetime
            start_time = datetime.datetime.now()
            print_box(f'running {name}')
            original_function(*args, **kwargs)
            end_time = datetime.datetime.now()
            time_diff = end_time - start_time  
            time_diff = td_format(time_diff)
            print_box(f'finished running {name}, run_time: {time_diff}')
        return wrapped_f
    return(wrap)