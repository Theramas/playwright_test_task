import time

def wait_until(func, condition=None, count=None, reverse=False, timeout=30, *args, **kwargs):
    start_time = time.time()
    while time.time() < (start_time + timeout):
        result = func(*args, **kwargs)
        if result:
            if condition:
                if count:
                    if condition(result, count):
                        return True
                elif reverse:
                    if result != condition:
                        return True
                else:
                    if result == condition:
                        return True
            elif count:
                if result >= count:
                    return True
            else:
                return result
        time.sleep(1)
    return False
