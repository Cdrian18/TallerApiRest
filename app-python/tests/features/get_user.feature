Feature: Obtener detalles de un usuario
  Como un usuario autenticado
  Quiero ver los detalles de mi cuenta
  Para gestionar mi información personal

  Scenario: Obtener detalles del usuario exitosamente
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud GET a "/users/72032da0-4854-4721-8543-44f86cf8cdef"
    Then la respuesta debería tener un código de estado 200
    And la respuesta debería incluir los detalles de "Adrian1234"

  Scenario: Intentar obtener detalles de otro usuario
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud GET buscando la id de otro usuario a "/users/31108ead-6a4f-40dd-bd48-57c0bda90f99"
    Then la respuesta debería tener un código de estado 401
    And la respuesta debería incluir un mensaje "No autorizado"
