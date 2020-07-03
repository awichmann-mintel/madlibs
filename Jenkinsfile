@Library('everest-shared') _
node('docker&&virtualenv') {
    properties([
        buildDiscarder(
            logRotator(
                artifactDaysToKeepStr: '14',
                artifactNumToKeepStr: '30',
                daysToKeepStr: '14',
                numToKeepStr: '30'
            )
        ),
        [$class: 'JobRestrictionProperty'],
        gitLabConnection('Gitlab'),
    ])
    withEnv(['DJANGO_SECRET_KEY=foobar', 'DJANGO_DEBUG=true']) {
        gitlabCommitStatus("jenkins-pipeline"){
            com.mintel.jenkins.EverestPipeline.builder(this)
                .withFlowdockNotification("bac6aea4efa3cbee8a7e7169a8a800ab")
                .withEcsService("mad-libz", "docker/Dockerfile")
                // .withSentryArtifact(<SENTRY_PROJECT_NAME>) # You must set up sentry integration yourself. This cookiecutter will not do it for you at the moment.
                .build()
                .execute()
        }
    }
}
