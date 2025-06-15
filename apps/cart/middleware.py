class SaveSessionKeyBeforeLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/users/login/' and not request.user.is_authenticated:
            # Guardamos la session key previa al login
            request.session['pre_login_session_key'] = request.session.session_key
        return self.get_response(request)
