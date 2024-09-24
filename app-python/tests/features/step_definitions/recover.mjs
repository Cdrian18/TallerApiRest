import { Given ,When, Then } from '@cucumber/cucumber';
import axios from 'axios';
import { expect } from 'chai';

Given('tengo un correo no registrado {string}', function (email) {
    this.email = email;
});

// Paso When: Hacer la solicitud POST a "/password" con el correo
When('hago una solicitud POST a {string} con este correo', async function (endpoint) {
    try {
        this.response = await axios.post(`${this.apiUrl}${endpoint}`, {
            email: this.email,
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

