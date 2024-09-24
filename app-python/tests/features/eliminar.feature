Feature: La API permite que el usuario autenticado pueda eliminarse


  Scenario: Eliminar mi cuenta exitosamente
    Given soy un usuario autenticado con un token valido
    When hago una solicitud DELETE a "/users/" acompañada de la id de mi usuario
    Then la respuesta debería tener un código de estado 204
    And mi cuenta debería haber sido eliminada del sistema

  Scenario: Intentar eliminar la cuenta de otro usuario
    Given soy un usuario autenticado con un token valido
    When hago una solicitud DELETE a "/users/"
    Then la respuesta debería tener un código de estado 403
    And la respuesta debería incluir un "Acceso denegado"

