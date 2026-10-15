pipeline {
    agent any

    parameters {
        choice(name: 'SUITE', choices: ['all', 'smoke', 'regression', 'api', 'ui'], description: 'Test Suite Marker to Run')
        string(name: 'WORKERS', defaultValue: '2', description: 'Number of parallel pytest-xdist workers')
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                            playwright install chromium
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                            playwright install chromium
                        '''
                    }
                }
            }
        }

        stage('Execute Playwright Pytest Suite') {
            steps {
                script {
                    def markerArg = (params.SUITE == 'all') ? '' : "-m ${params.SUITE}"
                    if (isUnix()) {
                        sh """
                            . venv/bin/activate
                            pytest ${markerArg} -n ${params.WORKERS} --browser chromium
                        """
                    } else {
                        bat """
                            call venv\\Scripts\\activate.bat
                            pytest ${markerArg} -n ${params.WORKERS} --browser chromium
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*, test-results/**/*', allowEmptyArchive: true
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Playwright Pytest HTML Report'
            ])
        }
    }
}