#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <map>

// initialize 8x8 bicolor matrix
Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

// WiFi/MQTT parameters
#define WLAN_SSID "182RSu3"
#define WLAN_PASS "Redrum182u3"
#define BROKER_IP "10.0.0.179"

// initialize MQTT client
WiFiClient client;
PubSubClient mqttclient(client);

typedef std::pair<int, int> coord;

std::map<std::string, std::pair<int, int>> num2coord;
for (row = 0, col = 0, i = 0; i < 64; i++)
{
    /*
    this loop creates a mapping from number to coordinate on matrix
    e.g., "0" -> (0, 0),   "1" -> (0, 1)
    */
    num2coord.insert(str(i), coord(row, col);
    col++;

    if (col > 7)
    {
        col = 0;
        row++; // move one row up
    }
}

void callback(char *topic, byte *payload, unsigned int length)
{
    /*
    NOTE: pixel (0,0) is the bottom left, (0, 1) is one to the right, (5, 6) is 6 to the right and 5 up
    */

    payload[length] = '\0'; // add null terminator to byte payload so we can treat it as a string

    if (strcmp(topic, "/win") == 0)
    {
        if (strcmp((char *) payload, "1")
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
                matrix.print("You suck!");
                matrix.writeDisplay();
                delay(100);
            }
        }
    }

    else if (strcmp(topic, "/player1") == 0)
    {
        coordinate = coord[payload];
        matrix.drawPixel(coordinate.first, coordinate.second, LED_RED);
        matrix.writeDisplay();
    }

    else if (strcmp(topic, "/player2") == 0)
    {
        coordinate = coord[payload];
        matrix.drawPixel(coordinate.first, coordinate.second, LED_YELLOW);
        matrix.writeDisplay();
    }
}

void setup()
{
    //Serial.begin(115200);

    Serial.begin(9600);
    Serial.println("8x8 LED Matrix Test");

    matrix.begin(0x70); // pass in the address

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

    //setup pins
    pinMode(LED, OUTPUT); // setup pin for input
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
            mqttclient.subscribe("/win")
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