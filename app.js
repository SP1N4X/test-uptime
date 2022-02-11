const axios = require('axios')

axios
  .get('https://www.sisal.it/api-betting/vrol-api/vrol/palinsesto/getAlberaturaEventiSingoli/1')
  .then(res => {
    console.log(`statusCode: ${res.status}`)
    console.log(res)
  })
  .catch(error => {
    console.error(error)
  })
