from tests.app.web.modules.internal_user.test_case import InternalUserTestCase, auth_user_already_logged

class TestInternalUserRoutes(InternalUserTestCase):

    def __init__(self, *args, **kwargs):
        super(TestInternalUserRoutes, self).__init__(*args, **kwargs)

    def test_routes_without_login(self):
        routes = [
            ("/internal_user/","get"),
            ("/internal_user/add/","get"),
            ("/internal_user/add/","post"),
            ("/internal_user/modify_1/","get"),
            ("/internal_user/modify_1/","post"),
            ("/internal_user/delete/","post")]
        for route in routes:
            response = getattr(self.client, route[1])(route[0])
            self.assertRedirectToLogin(response)

    @auth_user_already_logged
    def test_dashboard(self):
        response = self.client.get("/internal_user/")
        self.assertOk(response)
        self.assertTextIn("Usuarios registrados", response)
        self.assertTextIn("clark_kent", response)

    @auth_user_already_logged
    def test_add_by_route(self):
        response = self.client.get("/internal_user/add/")
        self.assertOk(response)
        self.assertTextIn("Agregar Usuarios", response)
        self.assertTextIn("Usuario", response)
        self.assertTextIn("Contraseña", response)
        self.assertTextIn("Repita la contraseña", response)
        self.assertTextIn("¿Es administrador?", response)
        self.assertTextIn("Aceptar", response)
        self.assertTextIn("Cancelar", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        
        username = "bruno_diaz"
        password = "imbatman123"
        is_admin = True
        response = self.client.post("/internal_user/add/", data={
            "username":username,
            "password":password,
            "confirm":password,
            "is_admin":is_admin}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")

        users = self.root_system.internal_user_system.select_all()
        self.assertLengthEqual(users, 2)
        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username=username)
        self.assertEqual(bruno_diaz.username, username)
        self.assertIsNone(bruno_diaz.last_connection)
        self.assertTrue(bruno_diaz.is_admin)

    @auth_user_already_logged
    def test_add_by_route_without_username(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"",
            "password":"imbatman123",
            "confirm":"imbatman123",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.add")
        self.assertTextIn("Ingrese un usuario.", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)

    @auth_user_already_logged
    def test_add_by_route_with_long_username(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        very_long_username = self.random_string(65)
        response = self.client.post("/internal_user/add/", data={
            "username":very_long_username,
            "password":"imbatman123",
            "confirm":"imbatman123",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.add")
        self.assertTextIn("Debe tener a lo sumo 64 caracteres.", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)

    @auth_user_already_logged
    def test_add_by_route_without_password(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"bruno_diaz",
            "password":"",
            "confirm":"imbatman123",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.add")
        self.assertTextIn("Ingrese una contraseña.", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)

    @auth_user_already_logged
    def test_add_by_route_without_confirm(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"bruno_diaz",
            "password":"imbatman123",
            "confirm":"",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.add")
        self.assertTextIn("Repita la contraseña.", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)

    @auth_user_already_logged
    def test_add_by_route_with_different_passwords(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"bruno_diaz",
            "password":"imbatman123",
            "confirm":"imnotsuperman456",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.add")
        self.assertTextIn("Las contraseñas deben coincidir.", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)

    @auth_user_already_logged
    def test_add_by_route_with_default_admin_value(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"bruno_diaz",
            "password":"imbatman123",
            "confirm":"imbatman123"}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        self.assertTextIn("bruno_diaz", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 2)

    @auth_user_already_logged
    def test_modify_by_route(self):
        old_username = "bruno_diaz"
        response = self.client.post("/internal_user/add/", data={
            "username":old_username,
            "password":"imbatman123",
            "confirm":"imbatman123",
            "is_admin":False}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username=old_username)
        self.assertEqual(bruno_diaz.username, old_username)

        response = self.client.get(f"/internal_user/modify_{bruno_diaz.id}/")
        self.assertOk(response)
        self.assertTextIn("Modificar Usuarios", response)
        self.assertTextIn("Usuario", response)
        self.assertTextIn(old_username, response)
        self.assertTextIn("¿Es administrador?", response)
        self.assertTextIn("Aceptar", response)
        self.assertTextIn("Cancelar", response)
        
        new_username = "brunoDiaz"
        response = self.client.post(f"/internal_user/modify_{bruno_diaz.id}/", data={"username":new_username, "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username=new_username)
        self.assertEqual(bruno_diaz.username, new_username)
        self.assertNotEqual(bruno_diaz.username, old_username)
        self.assertTrue(bruno_diaz.is_admin)
        self.assertIsEmpty(self.root_system.internal_user_system.select_all_filter_by(username=old_username))

    @auth_user_already_logged
    def test_modify_by_route_without_username(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"bruno_diaz",
            "password":"imbatman123",
            "confirm":"imbatman123",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 2)
        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username="bruno_diaz")
        response = self.client.post(f"/internal_user/modify_{bruno_diaz.id}/", data={"username":""}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.add")
        self.assertTextIn("Ingrese un usuario.", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 2)
        self.assertIsNone(self.root_system.internal_user_system.select_one_filter_by(username="", using="first"))

    @auth_user_already_logged
    def test_modify_by_route_with_long_username(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"bruno_diaz",
            "password":"imbatman123",
            "confirm":"imbatman123",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 2)
        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username="bruno_diaz")
        very_long_username = self.random_string(65)
        response = self.client.post(f"/internal_user/modify_{bruno_diaz.id}/", data={"username":very_long_username}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.add")
        self.assertTextIn("Debe tener a lo sumo 64 caracteres.", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 2)
        self.assertIsNone(self.root_system.internal_user_system.select_one_filter_by(username=very_long_username, using="first"))

    @auth_user_already_logged
    def test_modify_by_route_with_default_admin_value(self):
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":"bruno_diaz",
            "password":"imbatman123",
            "confirm":"imbatman123",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 2)
        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username="bruno_diaz")
        response = self.client.post(f"/internal_user/modify_{bruno_diaz.id}/", data={"username":"brunoDiaz"}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        self.assertTextIn("brunoDiaz", response)
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 2)
        self.assertIsNotNone(self.root_system.internal_user_system.select_one_filter_by(username="brunoDiaz"))
        self.assertIsNone(self.root_system.internal_user_system.select_one_filter_by(username="bruno_diaz", using="first"))

    @auth_user_already_logged
    def test_delete_by_route(self):
        username = "bruno_diaz"
        response = self.client.post("/internal_user/add/", data={
            "username":username,
            "password":"imbatman123",
            "confirm":"imbatman123",
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")
        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username=username)
        self.assertEqual(bruno_diaz.username, username)
        
        response = self.client.post(f"/internal_user/delete/", data={"element_id":bruno_diaz.id}, follow_redirects=True)
        self.assertOk(response)
        self.assertIsEmpty(self.root_system.internal_user_system.select_all_filter_by(username=username))

    @auth_user_already_logged
    def test_check_password(self):
        username = "bruno_diaz"
        password = "imbatman123"
        self.assertLengthEqual(self.root_system.internal_user_system.select_all(), 1)
        response = self.client.post("/internal_user/add/", data={
            "username":username,
            "password":password,
            "confirm":password,
            "is_admin":True}, follow_redirects=True)
        self.assertMovesOkTo(response, "internal_user.dashboard")

        bruno_diaz = self.root_system.internal_user_system.select_one_filter_by(username=username)
        self.assertTrue(self.root_system.internal_user_system.check_password(bruno_diaz, password))
        
    def test_update_last_connection(self):
        last_connection = self.root_system.time_system.tz_now()
        bruno_diaz = self.internal_user(last_connection=last_connection)
        bruno_diaz = self.root_system.internal_user_system.add(bruno_diaz)
        last_connection = bruno_diaz.last_connection
        self.root_system.time_system.sleep_for(2)
        bruno_diaz = self.root_system.internal_user_system.update_last_connection(bruno_diaz)
        self.assertLess(last_connection, bruno_diaz.last_connection)