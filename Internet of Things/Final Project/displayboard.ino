#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <vector>
#include <string>
#include <map>

// initialize 8x8 bicolor matrix
Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

// WiFi/MQTT parameters
#define WLAN_SSID ""
#define WLAN_PASS ""
#define BROKER_IP ""

// initialize MQTT client
WiFiClient client;
PubSubClient mqttclient(client);

typedef std::pair<int, int> coord;

std::map<int, coord> num2coord;

void flash_winning_move(std::string msg, bool is_AI)
{
    Serial.println(F("Flashing winning move"));
    std::vector<char> c1, c2, c3, c4;
    coord coord1, coord2, coord3, coord4;
    
    // get 4 board space numbers of winning 4-in-a-row from payload message
    c1 = {msg[0], msg[1]};
    c2 = {msg[3], msg[4]};
    c3 = {msg[6], msg[7]};
    c4 = {msg[9], msg[10]};

    // convert each of these numbers from string -> integer -> coordinate on board
    coord1 = num2coord[10 * (int(c1[0]) - 48) + (int(c1[1]) - 48)];
    coord2 = num2coord[10 * (int(c2[0]) - 48) + (int(c2[1]) - 48)];
    coord3 = num2coord[10 * (int(c3[0]) - 48) + (int(c3[1]) - 48)];
    coord4 = num2coord[10 * (int(c4[0]) - 48) + (int(c4[1]) - 48)];

    Serial.println(coord1.first);
    Serial.println(coord1.second);
    Serial.println(coord2.first);
    Serial.println(coord2.second);
    Serial.println(coord3.first);
    Serial.println(coord3.second);
    Serial.println(coord4.first);
    Serial.println(coord4.second);


    // put these 4 coordinates into a vector
    std::vector<coord> winning_coords = {coord1, coord2, coord3, coord4};

    // iterate through each of these coordinates
    for (int i = 0; i < 16; i++)
    {
        for (coord x : winning_coords)
        {
            // on even numbered iterations, turn the LEDs off, so it flashes
            if (i % 2 == 0)
                matrix.drawPixel(x.first, x.second, LED_OFF);
            else if (i % 2 != 0 && is_AI)
                matrix.drawPixel(x.first, x.second, LED_GREEN);
            else if (i % 2 != 0 && !is_AI)
                matrix.drawPixel(x.first, x.second, LED_RED);
        }
        matrix.writeDisplay();
        delay(250);
    }
    Serial.println(F("Finished flashing winning move"));

}

void callback(char *topic, byte *payload, unsigned int length)
{
    /*
    NOTE: pixel (0,0) is the bottom left, (0, 1) is one to the right, (5, 6) is 6 to the right and 5 up
    */

    payload[length] = '\0'; // add null terminator to byte payload so we can treat it as a string
    if (strcmp(topic, "/clear_board") == 0)
    {
        matrix.clear();
    }

    else if (strcmp(topic, "/win1") == 0)
    {
        // player has won, so display message accordingly
        std::string msg((char *)payload);
        flash_winning_move(msg, false);
        Serial.println(F("Flashed winning move for player 1"));


        matrix.setTextWrap(false); // we dont want text to wrap so it scrolls nicely
        matrix.setTextSize(1);
        matrix.setTextColor(LED_GREEN);
        for (int8_t x = 7; x >= -45; x--)
        {
            matrix.clear();
            matrix.setCursor(x, 0);
            matrix.print("You win!");
            matrix.writeDisplay();
            delay(100);
        }
        matrix.clear();
    }

    else if (strcmp(topic, "/win2") == 0)
    {
        std::string msg((char *)payload);
        flash_winning_move(msg, true);
        Serial.println(F("Flashed winning move for player 2"));


        // player has lost, so display message accordingly
        matrix.setTextWrap(false); // we dont want text to wrap so it scrolls nicely
        matrix.setTextSize(1);
        matrix.setTextColor(LED_RED);
        for (int8_t x = 7; x >= -55; x--)
        {
            matrix.clear();
            matrix.setCursor(x, 0);
            matrix.print("You suck!");
            matrix.writeDisplay();
            delay(100);
        }
        matrix.clear();
    }

    else if (strcmp(topic, "/tie") == 0)
    {
        // player has lost, so display message accordingly
        matrix.setTextWrap(false); // we dont want text to wrap so it scrolls nicely
        matrix.setTextSize(1);
        matrix.setTextColor(LED_RED);
        for (int8_t x = 7; x >= -45; x--)
        {
            matrix.clear();
            matrix.setCursor(x, 0);
            matrix.print("Tie!");
            matrix.writeDisplay();
            delay(100);
        }
        matrix.clear();
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

            mqttclient.subscribe("/clear_board");
            mqttclient.subscribe("/player1");
            mqttclient.subscribe("/player2");
            mqttclient.subscribe("/win1");
            mqttclient.subscribe("/win2");
            mqttclient.subscribe("/clear_board");

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
