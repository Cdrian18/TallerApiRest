pipeline {
    agent any
    environment {
        API_URL = 'http://api:8000'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Cdrian18/TallerApiRest.git'
            }
        }
        stage('Check Server Availability') {
            steps {
                script {
                    def serverUrl = "${API_URL}"
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' ${serverUrl}", returnStdout: true).trim()
                    echo "HTTP response code from API: ${response}"
                    if (response != '200') {
                        error("Server is not responding as expected: HTTP Status ${response}")
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                dir('app-python') {
                    echo 'Cleaning previous node modules'
                    sh 'rm -rf node_modules'
                    echo 'Installing dependencies'
                    sh 'npm install'
                }
            }
        }
        stage('Set Permissions') {
            steps {
                dir('app-python') {
                    echo 'Setting execute permissions on cucumber-js'
                    sh 'chmod +x node_modules/.bin/cucumber-js'
                }
            }
        }
        stage('Run Tests') {
            steps {
                dir('app-python') {
                    echo 'Creating reports directory'
                    sh 'mkdir -p reports'
                    echo 'Running cucumber tests and generating reports'
                    sh './node_modules/.bin/cucumber-js --format junit:reports/junit_report.xml --format html:reports/cucumber-report.html'
                    echo 'Listing report files:'
                    sh 'ls -l reports'
                }
            }
        }
    }
    post {
        always {
            dir('app-python') {
                echo 'Listing reports directory before archiving'
                sh 'ls -l reports'
                echo 'Archiving test results'
                junit 'reports/junit_report.xml'
            }
        }
    }
}
