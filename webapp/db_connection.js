var pg = require('pg');

var conString = "postgres://kpegbopk:O0WLMf2C4eEfAEaxy_LkQwejuD8Vj0kj@batyr.db.elephantsql.com/kpegbopk" //Can be found in the Details page
var client = new pg.Client(conString);
client.connect(function(err) {
  if(err) {
    return console.error('could not connect to postgres', err);
  }
  client.query('SELECT * FROM Users', function(err, result) {
    if(err) {
      return console.error('error running query', err);
    }
    console.log(result.rows);
    client.end();
  });
});