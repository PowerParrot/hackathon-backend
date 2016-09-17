'use strict';

var async = require('async');
var fs = require('fs');
var path = require('path');
var grpc = require('grpc');
var googleProtoFiles = require('google-proto-files');
var googleAuth = require('google-auto-auth');
var Transform = require('stream').Transform;

// server and sockets
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var call;

app.get('/', function(req, res){
  res.send('<h1>Hello world</h1>');
});

http.listen(5000, function(){
  console.log('listening on *:5000');
});

io.on('connection', function(socket) {
  socket.on('init', function(msg) {
      getSpeechService('speech.googleapis.com', function(speechService) {
        call = speechService.streamingRecognize();

        // Listen for various responses
        call.on('error', function(err) {
          console.log(err);
        });

        call.on('data', function (recognizeResponse) {
          console.log(recognizeResponse);
          if (recognizeResponse && recognizeResponse.results.length > 0) {
            for (var result in recognizeResponse.results) {
              console.log(result.alternatives);
              io.emit('message', results.alternatives);
            }
          }
        });

        call.on('end', function () {
          console.log('ended');
        });

        // Write the initial recognize reqeust
        console.log('write initial recognize request');
        call.write({
          streamingConfig: {
            config: {
              encoding: 'LINEAR16',
              sampleRate: 16000
            },
            interimResults: false,
            singleUtterance: false
          }
        });

      });
  });

  socket.on('audio', function(msg) {
    console.log('.');
    call.write({
      audioContent: msg
    });
  });
});

// [START proto]
var PROTO_ROOT_DIR = googleProtoFiles('..');

var protoDescriptor = grpc.load({
  root: PROTO_ROOT_DIR,
  file: path.relative(PROTO_ROOT_DIR, googleProtoFiles.speech.v1beta1)
}, 'proto', {
  binaryAsBase64: true,
  convertFieldsToCamelCase: true
});
var speechProto = protoDescriptor.google.cloud.speech.v1beta1;
// [END proto]

// [START authenticating]
function getSpeechService (host, callback) {
  var googleAuthClient = googleAuth({
    scopes: [
      'https://www.googleapis.com/auth/cloud-platform'
    ]
  });

  googleAuthClient.getAuthClient(function (err, authClient) {
    if (err) {
      return console.log(err);
    }

    var credentials = grpc.credentials.combineChannelCredentials(
      grpc.credentials.createSsl(),
      grpc.credentials.createFromGoogleCredential(authClient)
    );

    console.log('Loading speech service...');
    var stub = new speechProto.Speech(host, credentials);
    return callback(stub);
  });
}
// [END authenticating]
