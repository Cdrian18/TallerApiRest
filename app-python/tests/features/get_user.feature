Feature: Obtener detalles de un usuario

  Scenario: Obtener detalles del usuario exitosamente
    Given soy un usuario autenticado con un token valido
    When hago una solicitud GET a "/users/" acompañada de mi id publica
    Then la respuesta debería tener un código de estado 200
    And la respuesta debería incluir los detalles de mi usuario

  Scenario: Intentar obtener detalles de otro usuario
    Given soy un usuario autenticado con un token valido
    When hago una solicitud GET buscando la id de otro usuario a "/users/"
    Then la respuesta debería tener un código de estado 403
    And la respuesta debería incluir un "Acceso denegado"
