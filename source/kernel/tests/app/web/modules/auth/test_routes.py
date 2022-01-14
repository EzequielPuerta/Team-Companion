from tests.app.web.modules.auth.test_case import AuthTestCase, auth_user_already_logged

class TestAuthRoutes(AuthTestCase):

    def __init__(self, *args, **kwargs):
        super(TestAuthRoutes, self).__init__(*args, **kwargs)

    def test_routes_without_login(self):
        routes = {"/logout/":"get"}
        for route, action in routes.items():
            response = getattr(self.client, action)(route)
            self.assertRedirectToLogin(response)

    def test_enter_login(self):
        response = self.client.get("/login/")
        self.assertOk(response)
        self.assertTextIn("Usuario", response)
        self.assertTextIn("Contraseña", response)
        self.assertTextIn("No cerrar la sesión", response)
        self.assertTextIn("Ingresar", response)

    def test_first_login(self):
        self.assertIsEmpty(self.root_system.internal_user_system.select_all())
        response = self.client.post("/login/", data={
            "username":"user",
            "password":"pass",
            "remember_me":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "main.dashboard")
        first_user = self.root_system.internal_user_system.select_one_filter_by(username="user")
        self.assertJustOneElementIn(self.root_system.internal_user_system.select_all(), first_user)

    @auth_user_already_logged
    def test_logout(self):
        response = self.client.get("/logout/")
        self.assertRedirects(response, "auth.login")

    @auth_user_already_logged
    def test_login(self):
        response = self.client.get("/logout/")
        self.assertRedirects(response, "auth.login")
        superman = self.root_system.internal_user_system.select_one_filter_by(username="clark_kent")
        self.assertJustOneElementIn(self.root_system.internal_user_system.select_all(), superman)
        
        response = self.client.post("/login/", data={
            "username":superman.username,
            "password":superman.password,
            "remember_me":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "main.dashboard")
        superman = self.root_system.internal_user_system.select_one_filter_by(username="clark_kent")
        self.assertJustOneElementIn(self.root_system.internal_user_system.select_all(), superman)

    @auth_user_already_logged
    def test_login_for_already_authenticated(self):
        response = self.client.get("/login/")
        self.assertRedirects(response, "main.dashboard")