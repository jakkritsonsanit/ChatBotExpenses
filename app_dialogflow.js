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
    const preObject_expenses = document.getElementById('object_expenses');
    const preObject_income = document.getElementById('object_income');

    // Create references
    const dbRefObject_expenses = firebase.database().ref().child('expenses');
    const dbRefObject_income = firebase.database().ref().child('income');

    // Sync object changes
    var expenses = 0
    var income = 0
    console.log(income)
    
    dbRefObject_expenses.once('value', snap => {
      
      snap.forEach(function(transaction) {
        expenses = expenses + transaction.val().money;
      });
      console.log(expenses)
      preObject_expenses.innerText = "Expenses : ".concat(expenses);
    });
    
    dbRefObject_income.once('value', snap => {
      
      snap.forEach(function(transaction) {
        income = income + transaction.val().money;
      });
      console.log(income)
      preObject_income.innerText = "Income : ".concat(income);
      document.getElementById('object_total').innerText = "Total : ".concat((income - expenses));
    });

  }());
// preObject.innerText = JSON.stringify(snap.val(), null, 3);
// for each ตรง snap ได้เลย 