var pg = require('pg');

function connectAndQuery(query, callback) {
  let conString = "postgres://klzhcbxk:1HbbkUWWZxRHNJR_AkxBUg1Dk_8OMcjx@batyr.db.elephantsql.com/klzhcbxk" //Can be found in the Details page
  let client = new pg.Client(conString);
	client.connect(function(err) {
    if(err) {
      return callback('could not connect to postgres', err);
    }
    client.query(query, function(err, result) {
      if(err) {
        return callback('error running query', err);
      }
      callback(result.rows);
      client.end();
    });
  });
}

module.exports = connectAndQuery;