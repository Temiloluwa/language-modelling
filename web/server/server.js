const path = require('path');
const express = require('express');
const app = express();
const publicPath = path.join(__dirname, '..', 'public')
const port = 3000;

app.use(express.static(publicPath));
app.use((req, res, next)=>{
    res.header("Access-Control-Allow-Origin", "http://localhost:3000");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});


//const handler = (req, res, next) => {
//    next();
//};

app.get('/', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'))
})
  
app.listen(port, () => console.log(`listening at ${port}`));