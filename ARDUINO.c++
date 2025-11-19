#define LED_VERDE 2
#define LED_AMARILLO 3
#define LED_ROJO 4
#define TRIG 5
#define ECHO 6

long limite_rojo = 20;      
long limite_amarillo = 40;

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);

  Serial.begin(9600); 
}

long medirDistancia() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long duracion = pulseIn(ECHO, HIGH);
  long distancia = duracion * 0.034 / 2; 

  return distancia;
}

void loop() {

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int sep = data.indexOf(',');
    if (sep > 0) {
      limite_rojo = data.substring(0, sep).toInt();
      limite_amarillo = data.substring(sep + 1).toInt();
      Serial.print("Nuevos limites: ");
      Serial.print(limite_rojo);
      Serial.print(" / ");
      Serial.println(limite_amarillo);
    }
  long distancia = medirDistancia();
  Serial.print("Distancia: ");
  Serial.println(distancia);

  if (distancia <= limite_rojo) {
    digitalWrite(LED_ROJO, HIGH);
    digitalWrite(LED_AMARILLO, LOW);
    digitalWrite(LED_VERDE, LOW);
  }
  else if (distancia > limite_rojo && distancia <= limite_amarillo) {
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_AMARILLO, HIGH);
    digitalWrite(LED_VERDE, LOW);
  }
  else {
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_AMARILLO, LOW);
    digitalWrite(LED_VERDE, HIGH);
  }
  Serial.println(distancia);

  delay(200);
}