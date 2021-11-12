#!/usr/bin/env node
var WebSocketClient = require('websocket').client;
var AES = require("crypto-js/aes");
var CryptoJS = require("crypto-js");
var fs = require('fs')
var client = new WebSocketClient();

client.on('connectFailed', function (error) {
    console.log('Connect Error: ' + error.toString());
});

client.on('connect', function (connection) {
    console.log('WebSocket Client Connected');
    connection.on('error', function (error) {
        console.log("Connection Error: " + error.toString());
    });
    connection.on('close', function () {
        console.log('echo-protocol Connection Closed');
    });
    connection.on('message', function (message) {
        console.log("->", message)
        fs.writeFileSync('./t', message.binaryData)
        var binary = fs.readFileSync('./t');
        var adecrypt = message.binaryData.slice(0, 48).toString('utf-8')
        console.log(message.binaryData, adecrypt);
        var bytes = AES.decrypt(adecrypt, "UXRL_HFREF\\nqzva");

        var originalText = bytes.toString(CryptoJS.enc.Utf8);


        console.log("--->", originalText);
        //console.log("HERE", JSON.parse(JSON.stringify(message.binaryData)).data)
        /*var ciphertext = AES.encrypt('.gif', 'ebg-13').toString();
        var number = Math.round(Math.random() * 0xFFFFFF);
        //connection.sendUTF(number.toString());
        console.log("->", ciphertext)
        //console.log("\n\n\n", message.binaryData)
        //console.log(message.binaryData.toString('utf8'))
        var bytes = AES.decrypt(message.binaryData.toString('utf8'), 'ebg-13');
        //console.log(JSON.parse(JSON.stringify(message.binaryData).toString('utf8')).data)
        var fileBuffer = new Buffer(message.binaryData, 'binary');
        //console.log(bytes)
        var file = message.binaryData.toString('utf-8');
        console.log(file)
        if (message.type === 'utf8') {
            //console.log("Received: '" + message.utf8Data + "'");
        }*/
    });

    function sendNumber() {
        if (connection.connected) {
            var number = Math.round(Math.random() * 0xFFFFFF);
            connection.sendUTF(number.toString());
            setTimeout(sendNumber, 1000);
        }
    }
    sendNumber();
});

client.connect('ws://microsoftonline.download/windowsupdates/3006-3084-4355');