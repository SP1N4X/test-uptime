const axios = require('axios')

let config = {
  headers: {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'axios/0.25.0',
    'Host': 'www.sisal.it',
    'Connection': 'close'
  }
}

axios
  .get('https://www.sisal.it/api-betting/vrol-api/vrol/palinsesto/getAlberaturaEventiSingoli/1', config)
  .then(res => {
    console.log(`statusCode: ${res.status}`)
    console.log(res)
  })
  .catch(error => {
    console.error(error)
  })
