Feature: La API permite que el usuario autenticado pueda eliminarse


  Scenario: Eliminar mi cuenta exitosamente
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud DELETE a "/users/72032da0-4854-4721-8543-44f86cf8cdef"
    Then la respuesta debería tener un código de estado 204
    And mi cuenta debería haber sido eliminada del sistema

  Scenario: Intentar eliminar la cuenta de otro usuario
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud DELETE a "/users/98765"
    Then la respuesta debería tener un código de estado 401
    And la respuesta debería incluir un mensaje "No autorizado"

  Scenario: Intentar eliminar una cuenta que no existe
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud DELETE a "/users/nonexistent"
    Then la respuesta debería tener un código de estado 404
    And la respuesta debería incluir un mensaje "Usuario no encontrado"
