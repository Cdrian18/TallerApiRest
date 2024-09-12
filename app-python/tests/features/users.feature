Feature:La API de usuarios permite a un usuario registrado observar la lista de usuarios
    Scenario: Como usuario autenticado puedo acceder a la lista de usuarios registrados
    Given soy un usuario autenticado
    When invoco el servicio users con un get
    Then obtengo un status 200
    And una lista de usuarios