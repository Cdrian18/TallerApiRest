Feature: La API permite que el usuario autenticado actualice sus datos

  Scenario: Actualizar mi cuenta exitosamente
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud PUT a "/users/72032da0-4854-4721-8543-44f86cf8cdef" con los siguientes datos:
      | username | Adrian1234 |
      | email    | newemail@example.com |
    Then la respuesta debería tener un código de estado 200
    And los detalles de mi cuenta deberían actualizarse correctamente

  Scenario: Intentar actualizar la cuenta de otro usuario
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud PUT a "/users/98765" con los siguientes datos:
      | username | unauthorizeduser |
    Then la respuesta debería tener un código de estado 401
    And la respuesta debería incluir un mensaje "No autorizado"

  Scenario: Intentar actualizar una cuenta que no existe
    Given que estoy autenticado con el token de "Adrian1234"
    When hago una solicitud PUT a "/users/nonexistent" con los siguientes datos:
      | username | nonexistentuser |
    Then la respuesta debería tener un código de estado 404
    And la respuesta debería incluir un mensaje "Usuario no encontrado"
