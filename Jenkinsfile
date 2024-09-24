pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clonar el repositorio de Git
                git 'https://github.com/Cdrian18/TallerApiRest/tree/main'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Instalar dependencias con npm
                sh 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                // Ejecutar las pruebas
                sh 'npm test'
            }
        }
    }

    post {
        always {
            // Publicar los resultados de la construcción y limpiar
            junit '**/test-results.xml'
            cleanWs()
        }
    }
}
