// Initiate value so the LED does not blink
int value = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  // Make LED_BUILTIN as the output so it is controlled
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Check if something is sent to the serial
  if (Serial.available() > 0) {
    // Read the content
    Serial.println("Yes");
    String content = Serial.readStringUntil('\n');
    // If the content is a number, make it equal to value
    if (content.toInt() > 0 || content == "0") {
      value = content.toInt();
    }
    // If it is a character, make value 0 and say that it
    // must be an integer
    else {
      Serial.println("Must be an integer");
      value = 0;
    }
  }

  // BLINKING PART //
  // Given the value, make LED on within that duration
  // then turn it off by that duration, then repeat
  if (value > 0){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(value);
    digitalWrite(LED_BUILTIN, LOW);
    delay(value);
  }
  // If value is zero, just turn the LED off
  else if (value == 0) {
    digitalWrite(LED_BUILTIN, LOW);
  }

  // Serial.println(value);
}
