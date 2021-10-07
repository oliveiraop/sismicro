/*#define F_CPU 8000000UL     Define CPU Frequency e.g. here its 8MHz */
#include <avr/io.h>   /* Include AVR std. library file */
/*#include <stdio.h>    /* Include std. library file */
#include <avr/interrupt.h>
#include <util/delay.h>   /* Include Delay header file */
#include "usart_irq.h"

#ifndef F_CPU
#define F_CPU 8000000
#endif
#define VERTICALCENTER 500
#define HORIZONTALCENTER 500
#define BAUD 9600
#define UBRR_VAL F_CPU/16/BAUD-1







int main(void)
{
  DDRB = 0x06; /* Make OC1A e OC1B pin as output */ 
  TCNT1 = 0;    /* Set timer1 count zero */
  ICR1 = 2499;    /* Set TOP count for timer1 in ICR1 register */
  /* Set Fast PWM, TOP in ICR1, Clear OC1A on compare match, clk/64 */
  TCCR1A = (1<<WGM11)|(1<<COM1A1)|(1<<COM1B1);
  TCCR1B = (1<<WGM12)|(1<<WGM13)|(1<<CS10)|(1<<CS11);
  OCR1A = 370;
  OCR1B = 370;
  USART0_Init(UBRR_VAL);
  sei();
  
  char horPosTempLow;
  char horPosTempHigh;
  char verPosTempLow;
  char verPosTempHigh;
  while(1)
  {
    char data;
    data = USART0_Receive();
    
    switch(data) {
      case 'h':
      horPosTempLow = USART0_Receive();
      horPosTempHigh = USART0_Receive();
      OCR1AH = horPosTempHigh;
      OCR1AL = horPosTempLow;      
      break;
      
      case 'v':
      verPosTempLow = USART0_Receive();
      verPosTempHigh = USART0_Receive();
      OCR1BH = verPosTempHigh;
      OCR1BL = verPosTempLow;
      break;
      
      
      
    }
  }
} 
