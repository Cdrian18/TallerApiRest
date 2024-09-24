// tests/features/step_definitions/eliminar.mjs
import { Given, When, Then, Before } from '@cucumber/cucumber';
import axios from 'axios';
import { expect } from 'chai';

// Enviar solicitud DELETE para eliminar la cuenta del usuario
When('hago una solicitud DELETE a {string} acompañada de la id de mi usuario', async function(endpoint) {
    try {
        const fullEndpoint = `${this.apiUrl}${endpoint}${this.userId}`;
        this.response = await axios.delete(fullEndpoint, {
            headers: { Authorization: `Bearer ${this.authToken}` } // Incluimos el token en la cabecera
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

When('hago una solicitud DELETE a {string}', async function(endpoint) {
    try {
        const fullEndpoint = `${this.apiUrl}${endpoint}${'6c48cde4-5cbd-4474-b327-89e2d6181b9e'}`;
        this.response = await axios.delete(fullEndpoint, {
            headers: { Authorization: `Bearer ${this.authToken}` }
        });
    } catch (error) {
        this.response = error.response || error;
    }
});

// Verificar que la cuenta ha sido eliminada
Then('mi cuenta debería haber sido eliminada del sistema', async function() {
    try {
        // Intentar autenticarse con el usuario eliminado
        const authResponse = await axios.post(`${this.apiUrl}/login`, {
            username: this.credentials.username,
            password: this.credentials.password
        });

        // Si la autenticación es exitosa, significa que el usuario aún existe
        throw new Error('El usuario no fue eliminado correctamente');
    } catch (error) {
        // Validamos que el error sea un 401 (credenciales no válidas)
        if (!error.response && !error.response.status === 401) {
            throw new Error('Error al validar la eliminación del usuario');
        }
    }
});
