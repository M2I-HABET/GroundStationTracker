void resetCommandTimeout() {
  tic1.resetCommandTimeout();
  tic2.resetCommandTimeout();
}

void CommandTimeout(uint32_t ms) {
  uint32_t start = millis();
  do {
    resetCommandTimeout();
  } while ((uint32_t)(millis() - start) <= ms);
}

void CalculatePosition1(int32_t targetPosition) {
  do {
    resetCommandTimeout();
  } while (tic1.getCurrentPosition() != targetPosition && Serial.peek() != 'E');

  if(NegativeAzimuth1 == true) {
    Azimuth1 = Azimuth1 + 360; // move back to 0-360 range
    NegativeAzimuth1 = false;
  }
  
  if(NegativeAzimuth2 == true) {
    Azimuth2 = Azimuth2 + 360; // move back to 0-360 range
    NegativeAzimuth2 = false;
  }
  
  Azimuth1 = Azimuth2;
  tic1.haltAndSetPosition(0);
}

void CalculatePosition2(int32_t targetPosition) {
  do {
    resetCommandTimeout();
  } while (tic2.getCurrentPosition() != targetPosition && Serial.peek() != 'E');

  Elevation1 = Elevation2;
  tic2.haltAndSetPosition(0);
}

void MovePanAndTilt(String bytes_in) {
  for (int index = 1; index < bytes_in.length(); index++) {
    if (bytes_in[index] == ',') {
      Azimuth2 = bytes_in.substring(1, index).toFloat();
      Elevation2 = bytes_in.substring(index + 1).toFloat();
      break;
    }
  }

  tic1.exitSafeStart();
  tic2.exitSafeStart();

  int pan = MovePan();
  tic1.setTargetPosition(pan);
  CalculatePosition1(pan);
      
  int tilt = MoveTilt();
  tic2.setTargetPosition(tilt);
  CalculatePosition2(tilt);
      
  ResetDelay(125); 
}

int MovePan() {
  tic1.exitSafeStart();

  if(abs(Azimuth2 - (Azimuth1 - 360)) < abs(Azimuth2 - Azimuth1)) {
    Azimuth1 = Azimuth1 - 360;
    NegativeAzimuth1 = true;
  }

  else if(abs((Azimuth2 - 360) - Azimuth1) < abs(Azimuth2 - Azimuth1)) {
    Azimuth2 = Azimuth2 - 360;
    NegativeAzimuth2 = true;
  }

  return int(-119.33333 * (Azimuth2 - Azimuth1));
}

int MoveTilt() {
  tic2.exitSafeStart();
  
  return int(119.33333 * (Elevation2 - Elevation1)); 
}

void calibrate(String bytes_in) {
  for (int index = 1; index < bytes_in.length(); index++) {
    if (bytes_in[index] == ',') {
      Azimuth1 = bytes_in.substring(1, index).toFloat();
      Elevation1 = bytes_in.substring(index + 1).toFloat();
      break;
    }
  } 
  return;
}

void PanPositive(String bytes_in) {
  tic1.exitSafeStart();

  int NewPosition = bytes_in.substring(1).toFloat() * 119.3333;
  tic1.setTargetPosition(NewPosition);
  
  CalculatePosition1(NewPosition);
}

void PanNegative(String bytes_in) {
  tic1.exitSafeStart();
  
  int NewPosition = bytes_in.substring(1).toFloat() * 119.3333;
  tic1.setTargetPosition(-NewPosition);
  
  CalculatePosition1(-NewPosition);
}

void TiltUp(String bytes_in) {
  tic2.exitSafeStart();

  int NewPosition = bytes_in.substring(1).toFloat() * 119.3333;
  tic2.setTargetPosition(NewPosition);
  
  CalculatePosition2(NewPosition);
}

void TiltDown(String bytes_in) {
  tic2.exitSafeStart();

  int NewPosition = bytes_in.substring(1).toFloat() * 119.3333;
  tic2.setTargetPosition(-NewPosition);
  
  CalculatePosition2(-NewPosition);
}

void EmergencyStop(String bytes_in) {
  tic1.setTargetPosition(tic1.getCurrentPosition());
  tic2.setTargetPosition(tic1.getCurrentPosition());
}

void GPSData() { 
  if(GPS.fix) {
    GPSString = "" + String(GPS.latitudeDegrees, 4) + GPS.lat + "," + String(GPS.longitudeDegrees, 4) + GPS.lon + "," + String(GPS.altitude);
    Serial.println(GPSString);
  }
}
