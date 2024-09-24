import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from 'chai';
import { faker } from '@faker-js/faker'; 
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv({strict: false});

addFormats(ajv);

// Esquema para `PublicUser` basado en tu definición en Pydantic
export const publicUserSchema = {
    type: 'object',
    properties: {
        public_id: { type: 'string' },
        username: { type: 'string', minLength: 3 },
        email: { type: 'string', format: 'email' }
    },
    required: ['public_id', 'username', 'email'], 
    additionalProperties: true
};


// Usar Faker.js para generar datos únicos del nuevo usuario
Given('Tengo los datos correspondientes al username, email y password del nuevo usuario', function () {
    this.requestData = {
        "username": faker.internet.userName(),
        "password": "StrongPassword123!",
        "email": faker.internet.email()
    };
});

Given('Tengo los datos invalidos correspondientes al username, email y password del nuevo usuario', function () {
    this.requestData = {
        "username": "user_" + 123,
        "password": "newpassword",
        "email": "user_" + 678 + "@example.com"
    };
});

// Validar los detalles del nuevo usuario usando AJV
Then('la respuesta debería incluir los detalles del nuevo usuario', function () {
    if (!this.response || !this.response.data) {
        throw new Error('No se recibió respuesta con datos');
    }

    const validate = ajv.compile(publicUserSchema);
    const valid = validate(this.response.data);

    if (!valid) {
        throw new Error('La respuesta no cumple con el esquema esperado');
    }
});

