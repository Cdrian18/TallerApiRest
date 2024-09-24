Feature: La API permite que el usuario autenticado actualice sus datos

  Scenario: Actualizar mi cuenta exitosamente
    Given soy un usuario autenticado con un token valido
    When hago una solicitud de actualizacion de datos
    Then la respuesta debería tener un código de estado 200
    And los detalles de mi cuenta deberían actualizarse correctamente

  Scenario: Intentar actualizar la cuenta de otro usuario
    Given soy un usuario autenticado con un token valido
    When hago una solicitud de actualizacion de datos a "/users/d06bbc3a-3683-4377-97f4-0cc195ed2bff"
    Then la respuesta debería tener un código de estado 403
    And la respuesta debería incluir un "Acceso denegado"

  Scenario: Intentar actualizar una cuenta que no existe
    Given soy un usuario autenticado con un token valido
    When hago una solicitud PUT a "/users/123456789"
    Then la respuesta debería tener un código de estado 403
    And la respuesta debería incluir un "Acceso denegado"
