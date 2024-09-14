Feature: La API de usuarios permite la creación y registro de un usuario nuevo

    Scenario: Crear un usuario exitosamente
        Given Tengo los datos correspondientes al username, email y password del nuevo usuario
        When hago una solicitud POST a "/users" con estos datos
        Then la respuesta debería tener un código de estado 201
        And la respuesta debería incluir los detalles del nuevo usuario

    Scenario: Intentar crear un usuario con datos inválidos
        Scenario: Intentar crear un usuario con datos inválidos
        Given tengo los siguientes datos inválidos del usuario:
            | username | password | email   |
            | tu       | pass     | correo  |
        When hago una solicitud POST a "/users" con estos datos
        Then la respuesta debería tener un código de estado 400
        And la respuesta debería incluir un mensaje de error