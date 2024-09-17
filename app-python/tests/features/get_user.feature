Feature: Obtener detalles de un usuario

  Scenario: Obtener detalles del usuario exitosamente
    Given que estoy autenticado con un token valido
    When hago una solicitud GET a "/users" acompañada de mi id publica
    Then la respuesta debería tener un código de estado 200
    And la respuesta debería incluir los detalles de mi usuario

  Scenario: Intentar obtener detalles de otro usuario
    Given que estoy autenticado con un token valido
    When hago una solicitud GET buscando la id de otro usuario a "/users/31108ead-6a4f-40dd-bd48-57c0bda90f99"
    Then la respuesta debería tener un código de estado 401
    And la respuesta debería incluir un mensaje "No autorizado"
