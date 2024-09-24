import { setWorldConstructor, Given, When, Then, Before } from '@cucumber/cucumber';
import axios from 'axios';
import { expect } from 'chai';
import Ajv from 'ajv';
import { faker } from '@faker-js/faker';

// Crear un nuevo constructor para el World
class CustomWorld {
    constructor() {
        this.apiUrl = process.env.API_URL || 'http://localhost:8000';
        this.response = null;
        this.requestData = {};
        this.apiEndpoint = '';
        this.authToken = '';
        this.userId = '';
        this.email = '';
        this.credentials = {};
    }
}

setWorldConstructor(CustomWorld);

const ajv = new Ajv({strict: false});

// Esquemas de validación
const errorResponseSchemaCode = {
    type: 'object',
    properties: {
        code: { type: 'integer' },
        message: { type: 'string' },
        details: { type: 'string', nullable: true }
    },
    required: ['code', 'message'],
    additionalProperties: false
};

const errorResponseSchemaDetail = {
    type: 'object',
    properties: {
        detail: { type: 'string' }
    },
    required: ['detail'],
    additionalProperties: false
};

Before(function() {
    this.response = null;
    this.requestData = {};
    this.apiEndpoint = '';
    this.authToken = '';
    this.userId = '';
    this.email = '';
    this.credentials = {};
});

Given('el endpoint {string} está disponible', async function (endpoint) {
    this.apiEndpoint = `${this.apiUrl}${endpoint}`;
});

// Crear un nuevo usuario antes de la prueba
Given('soy un usuario autenticado con un token valido', async function() {
    try {
        // Crear un nuevo usuario
        const newUser = {
            username: faker.internet.userName(),
            password: 'PasswordSeguro123!',
            email: faker.internet.email()
        };

        this.credentials = {username: newUser.username, password: newUser.password};

        // Crear usuario
        const createResponse = await axios.post(`${this.apiUrl}/users`, newUser);

        // Autenticarse con el nuevo usuario
        const authResponse = await axios.post(`${this.apiUrl}/login`, {
            username: newUser.username,
            password: newUser.password
        });

        // Guardamos el token y el ID del usuario para usarlo más adelante
        this.authToken = authResponse.data.token;
        this.userId = createResponse.data.public_id; // Suponiendo que el ID del usuario viene en la respuesta
        this.email = newUser.email;

    } catch (error) {
        throw new Error('Error al crear o autenticar al usuario');
    }
});


Given('soy un usuario registrado con datos validos', async function() {
    try {
        // Crear un nuevo usuario
        const newUser = {
            username: faker.internet.userName(),
            password: 'PasswordSeguro123!',
            email: faker.internet.email()
        };

        this.credentials = {username: newUser.username, password: newUser.password};

        // Crear usuario
        const createResponse = await axios.post(`${this.apiUrl}/users`, newUser);

        this.userId = createResponse.data.public_id;
        this.email = newUser.email;

    } catch (error) {
        throw new Error('Error al crear o autenticar al usuario');
    }
});


// Enviar solicitud POST con los datos de la tabla Gherkin
When('envío una solicitud POST con los siguientes datos:', async function (dataTable) {
    const data = dataTable.rowsHash();
    try {
        this.response = await axios.post(this.apiEndpoint, data);
    } catch (error) {
        this.response = error.this.response || error;
    }
});

// Enviar solicitud POST con los datos definidos en el Given
When('hago una solicitud POST a {string} con estos datos', async function (endpoint) {
    try {
        this.response = await axios.post(`${this.apiUrl}${endpoint}`, this.requestData);
    } catch (error) {
        this.response = error.response || error;
    }
});

// Verificar el código de estado en la respuesta
Then('la respuesta debería tener un código de estado {int}', function (statusCode) {
    if (!this.response || !this.response.status) {
        throw new Error('No se recibió respuesta del servidor');
    }
    expect(this.response.status).to.equal(statusCode);
});

// Verificar que la respuesta contiene una clave específica
Then('la respuesta debería incluir un {string}', function (expectedMessage) {
    if (!this.response || !this.response.data) {
        throw new Error('No se recibió respuesta con datos');
    }

    const actualMessage = this.response.data.message || this.response.data.detail?.message || this.response.data.detail;

    if (!actualMessage) {
        throw new Error('No se encontró ni "message" ni "detail" en la respuesta');
    }

    // Comparar el mensaje actual con el esperado
    expect(actualMessage).to.equal(expectedMessage);
});



// Verificar que la respuesta contiene una clave con un valor específico
Then('la respuesta debe contener {string} con valor {string}', function (key, expectedValue) {
    if (!this.response || !this.response.data) {
        throw new Error('No se recibió respuesta con datos');
    }
    expect(this.response.data[key]).to.equal(expectedValue);
});

Then('la respuesta debería incluir un mensaje de error', function () {
    if (!this.response || !this.response.data) {
        throw new Error('No se recibió respuesta con datos');
    }

    // Intentar validar con el esquema que tiene 'code' y 'message'
    const validateCode = ajv.compile(errorResponseSchemaCode);
    const validCode = validateCode(this.response.data);

    // Intentar validar con el esquema que tiene 'detail'
    const validateDetail = ajv.compile(errorResponseSchemaDetail);
    const validDetail = validateDetail(this.response.data);

    // Si ninguno de los dos esquemas es válido, lanzamos un error
    if (!validCode && !validDetail) {
        throw new Error('La respuesta no cumple con ninguno de los esquemas de ErrorResponse');
    }
});

