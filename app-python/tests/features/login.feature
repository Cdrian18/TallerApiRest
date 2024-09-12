Feature: La API de usuarios permite la atennticacion de un usuario registrado
  Scenario: Como usuario puedo autenticarme y acceder a las funcionalidades
    When invoco al servicio login con un post
    Then obtengo un status 200
    And un token de autenticacion
