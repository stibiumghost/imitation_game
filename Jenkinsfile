pipeline{
    agent any
    
    stages{
        
        stage ('Install Libraries') {
            steps{
                sh 'pip3 install -r requirements.txt'
            }
        }
        
        stage('Download Files'){
            steps{
                sh 'dvc pull'
            }
        }
        
        stage ('Run Tests'){
            steps{
                sh 'pytest'
            }
        }
        
        stage ('Docker Build'){
            steps{
                sh 'docker build -t imitation_game_image .'
            }
        }
    }
}