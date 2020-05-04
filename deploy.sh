if [ "$TRAVIS_BRANCH" == "feature/ST-1234-Testing" ]; then
    
    # Bumps the version
    node ./bump_dev_version.js

    # Generates the changelog 
    node ./generate_changelog.js
  
    commit_file() {
      git add *
      git commit --message "Updating the CHANGELOG.md and the _version file"
    }

    upload_files() {
      git remote add feature/ST-1234-Testing  https://${TOLKEN}@github.com/policyme/Testing-CI-CD-Node.js.git > /dev/null 2>&1
      git push feature/ST-1234-Testing HEAD:feature/ST-1234-Testing
    }
    commit_file
    upload_files

    # Run the jest unit tests
    cd app/gui 

    # Run the test command
    sudo npm run test 


fi