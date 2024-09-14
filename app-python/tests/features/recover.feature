Feature: La API permite enviar un correo de recuperación para la contraseña

  Scenario: Enviar instrucciones para recuperar contraseña
    Given tengo el correo electrónico "user@example.com"
    When hago una solicitud POST a "/password" con este correo
    Then la respuesta debería tener un código de estado 200
    And debería recibir un mensaje de éxito

  Scenario: Intentar restablecer contraseña con un token inválido
    Given tengo un correo no registrado "user111118@example.com"
    When hago una solicitud PUT a "/password"
    Then la respuesta debería tener un código de estado 400
    And la respuesta debería incluir un mensaje "Correo no registrado"