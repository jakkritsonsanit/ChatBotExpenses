(function () {

  // Initialize Firebase
    const config = {
      apiKey: "AIzaSyCVkw9pASu2SBMsuBdNppz_OmQgAyjAWw0",
      authDomain: "line-bot-chrins.firebaseapp.com",
      databaseURL: "https://line-bot-chrins.firebaseio.com/",
      storageBucket: "line-bot-chrins.appspot.com"
    };
    firebase.initializeApp(config);

    // Get element
    const preObject = document.getElementById('object');

    // Create references
    const dbRefObject = firebase.database().ref().child('expenses');

    // Sync object changes
    dbRefObject.on('value', snap => {
      preObject.innerText = JSON.stringify(snap.val(), null, 3);
    });

}());