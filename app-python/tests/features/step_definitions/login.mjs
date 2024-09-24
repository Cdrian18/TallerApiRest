import { Given, When, Then } from '@cucumber/cucumber';
import axios from 'axios';
import { assert } from 'chai';

Given('tengo las siguientes credenciales incorrectas:', function (dataTable) {
  const data = dataTable.rowsHash();
  this.credentials = {
      username: data.username,
      password: data.password,
  };
});

When('hago una solicitud POST a \\/login', async function () {
  try {
    this.response = await axios.post(`${this.apiUrl}/login`, {
      "username": "Adrian12345",
      "password": "StrongPassword123!"
    });
  } catch (error) {
    this.response = error.response;
  }
});

When('hago una solicitud POST a {string} con estas credenciales', async function (endpoint) {
  try {
      this.response = await axios.post(`${this.apiUrl}${endpoint}`, this.credentials);
  } catch (error) {
      this.response = error.response || error;
  }
});

Then('obtengo un status {int}', function (statusCode) {
  assert.strictEqual(this.response.status, statusCode);
});

Then('un token de autenticacion', function () {
  assert(this.response.data.token, 'No se encontró el token de autenticación en la respuesta');
});
