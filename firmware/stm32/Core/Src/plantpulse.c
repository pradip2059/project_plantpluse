#include "plantpulse.h"
#include "main.h"
#include <stdio.h>
#include <string.h>
extern UART_HandleTypeDef huart1;
void PlantPulse_SendTelemetry(float rpm,float current_a,float temp_c,float vib,float pressure){
  char b[160];
  int n=snprintf(b,sizeof(b),"RPM=%.0f,CURRENT=%.2f,TEMP=%.1f,VIB=%.2f,PRESSURE=%.1f,STATE=RUNNING,FAULT=NONE\r\n",rpm,current_a,temp_c,vib,pressure);
  HAL_UART_Transmit(&huart1,(uint8_t*)b,(uint16_t)n,100);
}
