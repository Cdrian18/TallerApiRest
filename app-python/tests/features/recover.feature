Feature: La API permite enviar un correo de recuperación para la contraseña

  Scenario: Enviar instrucciones para recuperar contraseña
    Given soy un usuario registrado con datos validos
    When hago una solicitud POST a "/password" con este correo
    Then la respuesta debería tener un código de estado 200
    And la respuesta debería incluir un "Se ha enviado un correo con las instrucciones de recuperación de contraseña"

  Scenario: Intentar restablecer contraseña con un token inválido
    Given tengo un correo no registrado "user111118@example.com"
    When hago una solicitud POST a "/password" con este correo
    Then la respuesta debería tener un código de estado 404
    And la respuesta debería incluir un "Correo no registrado"