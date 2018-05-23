var express = require('express');
var router = express.Router();
var spawn = require('child_process').spawn;
var fs = require('fs');
const fileUpload = require('express-fileupload');
var cmd = require('node-cmd')

router.use(fileUpload());

/* GET scripts listing. */
router.get('/', function(req, res, next) {
  res.send('ALLO');
});

router.post('/upload', function (req, res) {
    if (!req.files)
        return res.status(400).send('No files were uploaded.');
    
    req.files.sampleFile.mv('uploads/' + req.files.sampleFile.name, function(err) {
        if (err)
            return res.status(500).send(err);
    
        });

    var pyProcess = cmd.get('python3 Validate_ExercDSL.py ' + 'uploads/' + req.files.sampleFile.name + ' jsons/' + req.files.sampleFile.name,
      function(error,stdout,stderr) {
        if (!error && !stderr) {
            if(!stdout){
                res.send('Ficheiro criado com sucesso');
                res.end();
            }
            else {
                res.send('Erros encontrados:\n ' + stdout);
                res.end();
            }
        }
        else{
            res.send('Ficheiro não processado!');
            res.end();
        }
    });
});

module.exports = router;