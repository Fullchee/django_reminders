from api.responses import JsonResponseBadRequest


def required_parameter(**methods_to_required_parameter):
    """
    Raises:
        JsonResponseBadRequest if the request is missing a list attribute

    Example:
        @required_parameter(GET=("earner", "month"), POST=("earner",))
        def some_function(request, ...):
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]

            request_parameters = getattr(request, request.method, {})
            required_parameters = methods_to_required_parameter.get(request.method, [])
            missing_parameters = set(required_parameters) - set(request_parameters)
            if missing_parameters:
                return JsonResponseBadRequest(
                    {
                        "title": "Bad request",
                        "message": f"Missing parameters: {list(missing_parameters)}.",
                    }
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
