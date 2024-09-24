import { Given, When, Then } from '@cucumber/cucumber';
import axios from 'axios';
import { expect } from 'chai';

// Paso When: Hacer una solicitud de actualización con los datos proporcionados
When('hago una solicitud de actualizacion de datos', async function () {
    this.requestData = {
        username: this.credentials.username,
        email: this.email,
        password: this.credentials.password
    };
    const url = `${this.apiUrl}/users/${this.userId}`;  // Usar el ID del usuario autenticado

    try {
        this.response = await axios.put(url, this.requestData, {
            headers: {
                Authorization: `Bearer ${this.authToken}`
            }
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

// Paso When: Hacer una solicitud de actualización con los datos proporcionados
When('hago una solicitud de actualizacion de datos a {string}', async function (endpoint) {
    this.requestData = {
        username: this.credentials.username,
        email: this.email,
        password: this.credentials.password
    };
    const url = `${this.apiUrl}${endpoint}`;

    try {
        this.response = await axios.put(url, this.requestData, {
            headers: {
                Authorization: `Bearer ${this.authToken}`
            }
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

When('hago una solicitud PUT a {string}', async function (endpoint) {
    this.requestData = {
        username: this.credentials.username,
        email: this.email,
        password: this.credentials.password
    };
    const url = `${this.apiUrl}${endpoint}`;
    try {
        this.response = await axios.put(url, this.requestData, {
            headers: {
                Authorization: `Bearer ${this.authToken}`
            }
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

// Paso Then: Verificar que los detalles de la cuenta se actualizaron correctamente
Then('los detalles de mi cuenta deberían actualizarse correctamente', function () {
    if (!this.response || !this.response.data) {
        throw new Error('No se recibió respuesta con datos');
    }

    // Comprobar que la respuesta tiene los datos actualizados
    const expectedUsername = this.requestData.username;
    const expectedEmail = this.requestData.email;

    expect(this.response.data.username).to.equal(expectedUsername);
    expect(this.response.data.email).to.equal(expectedEmail);
});
