// Import the queryDatabase function from database.js
const queryDatabase = require('./db_connection');

// Now you can use the queryDatabase function here
const queryString = 'SELECT * FROM Users';

queryDatabase(queryString, function(err, result) {
    if (err) {
        console.error(err);
        return;
    }

    console.log(result);
});
