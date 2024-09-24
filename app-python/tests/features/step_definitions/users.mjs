import { Given, When, Then } from '@cucumber/cucumber';
import axios from 'axios';
import { expect } from 'chai';

// Paso When: Hacer una solicitud GET a "/users"
When('hago una solicitud GET a {string}', async function (endpoint) {
    const url = `${this.apiUrl}${endpoint}`;

    try {
        this.response = await axios.get(url, {
            headers: {
                Authorization: `Bearer ${this.authToken}`
            }
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

// Paso Then: Verificar que la respuesta contiene una lista de usuarios
Then('una lista de usuarios', function () {
    if (!this.response || !this.response.data) {
        throw new Error('No se recibió respuesta con datos');
    }

    const usersList = this.response.data.users

    if (!Array.isArray(usersList)) {
        throw new Error('La respuesta no contiene una lista de usuarios válida');
    }

    // Verificar que la lista de usuarios no esté vacía
    expect(usersList.length).to.be.greaterThan(0);
});


