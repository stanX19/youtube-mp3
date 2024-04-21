from wininhibit import WindowsInhibitor


def anti_sleep(func):
    def newfn(*args, **kwargs):
        inhibitor = WindowsInhibitor(quiet=True)
        inhibitor.inhibit()
        ret = func(*args, **kwargs)
        inhibitor.uninhibit()
        return ret
    return newfn


def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param exceptions: Lists of exceptions that trigger a retry attempt
    :type exceptions: Tuple of Exceptions
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    args_str = ", ".join(args)
                    if kwargs:
                        kwargs_str = ", ".join(f"{key}={val}" for key, val in kwargs.items())
                        args_str += ", " + kwargs_str
                    attempt += 1
                    print(f"Exception when running {func.__name__}({args_str}); retrying {attempt}/{times}")
            return func(*args, **kwargs)

        return newfn

    return decorator