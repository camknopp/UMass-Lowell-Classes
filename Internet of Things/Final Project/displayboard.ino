#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <string>
#include <map>

// initialize 8x8 bicolor matrix
Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

// WiFi/MQTT parameters
#define WLAN_SSID "KNOPPNET_5GHZ"
#define WLAN_PASS "AAAAABBBBBCCCCCDDDDDEEEEEF"
#define BROKER_IP "10.0.0.179"


// initialize MQTT client
WiFiClient client;
PubSubClient mqttclient(client);

typedef std::pair<int, int> coord;

std::map<int, coord> num2coord;

void callback(char *topic, byte *payload, unsigned int length)
{
    /*
    NOTE: pixel (0,0) is the bottom left, (0, 1) is one to the right, (5, 6) is 6 to the right and 5 up
    */

    payload[length] = '\0'; // add null terminator to byte payload so we can treat it as a string

    if (strcmp(topic, "/win") == 0)
    {

        Serial.println(F("win message received"));

        if (strcmp((char *)payload, "1") == 0)
        {
            // player has won, so display message accordingly

            matrix.setTextWrap(false); // we dont want text to wrap so it scrolls nicely
            matrix.setTextSize(1);
            matrix.setTextColor(LED_GREEN);
            for (int8_t x = 7; x >= -36; x--)
            {
                matrix.clear();
                matrix.setCursor(x, 0);
                matrix.print("You win!");
                matrix.writeDisplay();
                delay(100);
            }
            matrix.clear();
        }
        else if (strcmp((char*)payload, "2") == 0)
        {
            // player has lost, so display message accordingly
            matrix.setTextWrap(false); // we dont want text to wrap so it scrolls nicely
            matrix.setTextSize(1);
            matrix.setTextColor(LED_RED);
            for (int8_t x = 7; x >= -36; x--)
            {
                matrix.clear();
                matrix.setCursor(x, 0);
                matrix.print("You suck!");
                matrix.writeDisplay();
                delay(100);
            }
            matrix.clear();
        }
        else
        {
            // player has lost, so display message accordingly
            matrix.setTextWrap(false); // we dont want text to wrap so it scrolls nicely
            matrix.setTextSize(1);
            matrix.setTextColor(LED_RED);
            for (int8_t x = 7; x >= -36; x--)
            {
                matrix.clear();
                matrix.setCursor(x, 0);
                matrix.print("Tie!");
                matrix.writeDisplay();
                delay(100);
            }
            matrix.clear();
        }
        
    }

    else if (strcmp(topic, "/player1") == 0)
    {
        int num;
        Serial.println(F("player 1 message received"));

        if (strlen((char *)payload) == 1)
            num = ((char *)payload)[0] - 48;
        else if (strlen((char *)payload) == 2)
            num = 10 * (int(((char *)payload)[0]) - 48) + int(((char *)payload[1])) - 48;

        coord c = num2coord[num];
        matrix.drawPixel(c.first, c.second, LED_RED);
        matrix.writeDisplay();
    }

    else if (strcmp(topic, "/player2") == 0)
    {  
        int num;
        Serial.println(F("player 2 message received"));

        if (strlen((char *)payload) == 1)
            num = ((char *)payload)[0] - 48;
        else if (strlen((char *)payload) == 2)
            num = 10 * (int(((char *)payload)[0]) - 48) + int(((char *)payload[1])) - 48;

        coord c = num2coord[num];
        matrix.drawPixel(c.first, c.second, LED_GREEN);
        matrix.writeDisplay();
    }
}

void setup()
{
    Serial.println(F("entering setup"));

    int row = 0;
    int col = 0;

    for (int i = 0; i < 64; i++)
    {
        /*
    this loop creates a mapping from number to coordinate on matrix
    e.g., "0" -> (0, 0),   "1" -> (0, 1) 
    */
        num2coord[i] = coord(row, col);
        col++;

        if (col > 7)
        {
            col = 0;
            row++; // move one row up
        }
    }
    //Serial.begin(115200);

    Serial.begin(9600);
    Serial.println("8x8 LED Matrix Test");

    matrix.begin(0x70); // pass in the address
    matrix.clear();

    // connect to wifi
    WiFi.mode(WIFI_STA);
    WiFi.begin(WLAN_SSID, WLAN_PASS);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(F("."));
    }

    Serial.println(F("WiFi connected"));
    Serial.println(F("IP address: "));
    Serial.println(WiFi.localIP());

    // connect to mqtt server
    mqttclient.setServer(BROKER_IP, 1883);
    mqttclient.setCallback(callback);
    connect();
    Serial.println(F("Leaving setup"));
}

void loop()
{
    if (!mqttclient.connected())
    {
        connect();
    }

    mqttclient.loop();
}

void connect()
{
    matrix.clear();
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println(F("Wifi issue"));
        delay(3000);
    }
    Serial.print(F("Connecting to MQTT server... "));
    while (!mqttclient.connected())
    {
        if (mqttclient.connect(WiFi.macAddress().c_str()))
        {
            Serial.println(F("MQTT server Connected!"));

            mqttclient.subscribe("/player1");
            mqttclient.subscribe("/player2");
            mqttclient.subscribe("/win");
        }
        else
        {
            Serial.print(F("MQTT server connection failed! rc="));
            Serial.print(mqttclient.state());
            Serial.println("try again in 10 seconds");
            // Wait 5 seconds before retrying
            delay(20000);
        }
    }
}