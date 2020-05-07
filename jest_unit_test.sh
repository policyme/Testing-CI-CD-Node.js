if [ "$TRAVIS_BRANCH" == "feature/ST-1234-Testing" ]; then

    run_test(){
    # Run the jest unit tests
        cd app/gui 
    # Installing the node dependency 
        npm install
    # Run the test command
        npm run test 
        }

    run_test
fi