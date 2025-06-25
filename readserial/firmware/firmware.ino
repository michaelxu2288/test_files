/**********************************************************************
 * Seesaw encoder → fuelChange + Heartbeat publisher (brace framing)
 * Hardware : Adafruit Seesaw rotary encoder
 * Depends  : Adafruit_seesaw, seesaw_neopixel, ArduinoJson, TimeLib
 *********************************************************************/
#include "Adafruit_seesaw.h"
#include <seesaw_neopixel.h>
#include <ArduinoJson.h>
#include <TimeLib.h>

#define SS_SWITCH      24
#define SS_NEOPIX       6
#define SEESAW_ADDR  0x3A

#define DEVICE_ID     0x3A
#define ID_SOURCE  "src_ng_ac"

Adafruit_seesaw  ss;
seesaw_NeoPixel  pixel(1, SS_NEOPIX, NEO_GRB + NEO_KHZ800);

int32_t  lastEncPos = 0;
int8_t   fuelLevel  = 0;          // 0–100
uint32_t hbSeq      = 0;          // heartbeat counter

/* ---------- prototypes ----------- */
void sendFuelChange();
void sendHeartbeat();
uint32_t wheel(byte);

void setup() {
  Serial.begin(115200);
  while (!Serial) ;

  if (!ss.begin(SEESAW_ADDR) || !pixel.begin(SEESAW_ADDR)) {
    Serial.println(F("Seesaw not found")); while (true);
  }
  pixel.setBrightness(25); pixel.show();
  ss.pinMode(SS_SWITCH, INPUT_PULLUP);

  lastEncPos = ss.getEncoderPosition();

  /* seed clock (replace with RTC/NTP later) */
  setTime(1717611090);   // 5 Jun 2025 15:51:30 CDT
}

void loop() {
  /* --- knob turns → fuelChange --- */
  int32_t pos  = ss.getEncoderPosition();
  int32_t diff = pos - lastEncPos;
  if (diff != 0) {
    fuelLevel  = constrain(fuelLevel + (int8_t)diff, 0, 100);
    lastEncPos = pos;

    pixel.setPixelColor(0, wheel(fuelLevel * 255 / 100));
    pixel.show();

    sendFuelChange();
  }

  /* --- hold button → heartbeat spam --- */
  if (!ss.digitalRead(SS_SWITCH)) {
    sendHeartbeat();
  }

  delay(10);
}

/* ================= helpers ================= */

void openFrame()  { Serial.println('{'); }
void closeFrame() { Serial.println('}'); Serial.println(); }

void commonHeader(const char* topic, const char* dtype)
{
  const unsigned long ms  = millis();
  char iso[25];
  snprintf(iso, sizeof(iso), "%04u-%02u-%02uT%02u:%02u:%02u CDT",
           year(), month(), day(), hour(), minute(), second());

  Serial.print("deviceIdSource="); Serial.println(ID_SOURCE);
  Serial.print("publishedTime=");  Serial.println(ms);
  Serial.print("publishedTime=");  Serial.println(iso);
  Serial.print("receivedTime=");   Serial.println(ms);
  Serial.print("receivedTime=");   Serial.println(iso);
  Serial.print("topic=");          Serial.println(topic);
  Serial.print("dataType=");       Serial.println(dtype);
}

void sendFuelChange()
{
  StaticJsonDocument<64> doc;
  doc["deviceId"]  = DEVICE_ID;
  doc["fuelLevel"] = fuelLevel;

  char buf[64];
  serializeJson(doc, buf, sizeof(buf));

  openFrame();
  commonHeader("fuelChange", "tms.fuelChange");
  Serial.print("jsonTopicData="); Serial.println(buf);
  closeFrame();
}

void sendHeartbeat()
{
  StaticJsonDocument<64> doc;
  doc["deviceId"]       = DEVICE_ID;
  doc["fuelLevel"] = fuelLevel;

  char buf[64];
  serializeJson(doc, buf, sizeof(buf));

  openFrame();
  commonHeader("Heartbeat", "tms.Heartbeat");
  Serial.print("jsonTopicData="); Serial.println(buf);
  closeFrame();
}

/* rainbow helper */
uint32_t wheel(byte p) {
  p = 255 - p;
  if (p < 85)   return pixel.Color(255 - p * 3, 0, p * 3);
  if (p < 170) { p -= 85; return pixel.Color(0, p * 3, 255 - p * 3); }
  p -= 170;     return pixel.Color(p * 3, 255 - p * 3, 0);
}
