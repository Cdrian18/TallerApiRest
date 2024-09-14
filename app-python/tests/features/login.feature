Feature: La API de usuarios permite la atennticacion de un usuario registrado
  Scenario: Como usuario puedo autenticarme y acceder a las funcionalidades
    Given tengo las siguientes credenciales de usuario
      | username   | password           |
      | Adrian1234 | StrongPassword184! |
    When hago una solicitud POST a /login
    Then obtengo un status 200
    And un token de autenticacion

  Scenario: Intentar autenticar con credenciales incorrectas
    Given tengo las siguientes credenciales incorrectas:
      | username  | password  |
      | wronguser | wrongpass |
    When hago una solicitud POST a "/login" con estas credenciales
    Then la respuesta debería tener un código de estado 401
    And la respuesta debería incluir un mensaje "Credenciales inválidas"