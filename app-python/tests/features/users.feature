Feature:La API de usuarios permite a un usuario registrado observar la lista de usuarios
    Scenario: Como usuario autenticado puedo acceder a la lista de usuarios registrados
        Given soy un usuario autenticado con un token valido
        When hago una solicitud GET a "/users"
        Then obtengo un status 200
        And una lista de usuarios

    Scenario: Intentar listar usuarios sin estar autenticado
        When hago una solicitud GET a "/users"
        Then la respuesta debería tener un código de estado 401
        And la respuesta debería incluir un "Could not validate credentials"