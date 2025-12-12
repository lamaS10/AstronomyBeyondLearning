class DisableBrowserCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/accounts/password-reset") \
           or request.path.startswith("/accounts/login") \
           or request.path.startswith("/accounts/logout"):
            return self.get_response(request)

        response = self.get_response(request)

        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        return response
