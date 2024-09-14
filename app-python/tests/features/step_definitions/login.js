const { When, Then } = require('@cucumber/cucumber');
const axios = require('axios');
const assert = require('assert');

let response; // Variable para almacenar la respuesta del servicio

When('hago una solicitud POST a /login', async function () {
  try {
    response = await axios.post('http://localhost:8000/login', {
      "username": "Adrian1234",
      "password": "StrongPassword184!"
    });
  } catch (error) {
    response = error.response;
  }
});

Then('obtengo un status {int}', function (statusCode) {
  assert.strictEqual(response.status, statusCode);
});

Then('un token de autenticacion', function () {
  assert(response.data.token, 'No se encontró el token de autenticación en la respuesta');
});
