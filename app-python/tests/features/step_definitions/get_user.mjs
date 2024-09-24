import { Given, When, Then } from '@cucumber/cucumber';
import axios from 'axios';
import { expect } from 'chai';
import { publicUserSchema } from './create_user.mjs';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

// Configuración de Ajv
const ajv = new Ajv({ strict: false });
addFormats(ajv);

// Paso When: Hacer la solicitud GET con ID pública
When('hago una solicitud GET a {string} acompañada de mi id publica', async function (endpoint) {
    try {
        const userId = this.userId;  // Obtener el ID público del usuario autenticado
        const url = `${this.apiUrl}${endpoint}${userId}`;  // Construir la URL con el ID

        this.response = await axios.get(url, {
            headers: {
                Authorization: `Bearer ${this.authToken}`,  // Incluir el token de autenticación
            },
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

When('hago una solicitud GET buscando la id de otro usuario a {string}', async function (endpoint) {
    try {
        const otherUserId = '189fd7ab-28de-488a-b717-77d851468284';  // Aquí debes pasar la ID del otro usuario
        const url = `${this.apiUrl}${endpoint}${otherUserId}`;
        this.response = await axios.get(url, {
            headers: {
                Authorization: `Bearer ${this.authToken}`,  // Usa el token autenticado del usuario actual
            },
        });
    } catch (error) {
        this.response = error.response || error;
    }
});


// Paso Then: Validar que la respuesta incluye los detalles de mi usuario
Then('la respuesta debería incluir los detalles de mi usuario', function () {
    if (!this.response || !this.response.data) {
        throw new Error('No se recibió una respuesta válida o los datos están vacíos');
    }

    const validate = ajv.compile(publicUserSchema);
    const valid = validate(this.response.data);

    if (!valid) {
        throw new Error('La respuesta no cumple con el esquema de PublicUser');
    }
});
