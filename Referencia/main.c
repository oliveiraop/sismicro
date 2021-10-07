/*
 * adc_ldr_read.c
 *
 * Created: 19/11/2019 11:46:19
 * Author : Levi Murici
 */ 
#define F_CPU 16000000
#define BAUD 9600
#define UBRR_VAL F_CPU/16/BAUD-1

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "usart_irq.h"

void ADCiniciar(void);
unsigned int ADCleitura();

volatile float somador = 0; // teremos várias amostras possivelmente grandes, por isso 32bits
volatile float  media = 0;
volatile float amostras = 0;
volatile float ADC_10bit_valor = 0;
volatile uint8_t ADC_8bit_low_nibble = 0;
volatile uint8_t ADC_8bit_high_nibble = 0;


volatile char adc_valor_string[16];

int main(void)
{
	DDRB=0xFF;
	PORTB &= ~(1<<PORTB2);
	USART0_Init(UBRR_VAL);
	sei();
	ADCiniciar();                                    // Executa a subrotina

	while(1)
	{	
		uint16_t valor_sensor;
		uint8_t valor_high, valor_low;
		
		valor_sensor = 	ADCleitura();
		valor_high = ADC_8bit_high_nibble;
		valor_low = ADC_8bit_low_nibble;
		
		//valor_sensor = (valor_high>>8) | valor_low;
		
		//valor_sensor = (ADC)/200;
		
		valor_sensor = ADC;
		
		char data_temp = USART0_Receive();
		
		switch(data_temp)
		{
			case 'g':
			
			USART0_Transmit(valor_sensor);
			
			break;
			
			case 'a':
			
			PORTB |= (1<<PORTB2);
			
			break;
			
			case 'c':
			
			PORTB &= ~(1<<PORTB2);
			
			break;
		 }
	}
}

void ADCiniciar(void)		                                // Inicialização do ADC
{
	/* ADMUX:
	 * RFSn = 0b11, 1,1v de tensão interna de referencia
	 * MUX  = 0b000, ajusta o ADC0 (A0). É selecionado na subrotina ADCleitura
	 * ADLAR = (1<<ADLAR)
	 */
	ADMUX=(1<<REFS1)|(1<<REFS0);
	
	 /* ADCRA:
      *	ADEN = 0b1, ativa o ADC
	  * ADPS = 0b111, prescaler 128. Precisamos de uma frequencia entre 50 khz e 200 khz, 16000000/128 = 125000 khz
	  */ 
	ADCSRA=(1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}
unsigned int ADCleitura()
{
	ADMUX |=0x00;					
	ADCSRA|=(1<<ADSC);					// Inicia a conversão colocando 1 nesse registrador
	while(ADCSRA==0x9f);		        // Compara todo registrador (0x9f eq. 0b1001111), quando a conversão estiver completa,
	ADCSRA|=(1<<ADIF);					// apaga o registrador
	ADC_8bit_low_nibble = ADCL;
	ADC_8bit_high_nibble = ADCH;
	return (ADC);						// Atribui o valor do convertido do ADC a subrotina
}