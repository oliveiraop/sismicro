#ifndef INCFILE1_H_
#define INCFILE1_H_

#define USART_RX_BUFFER_SIZE 128     /* 2,4,8,16,32,64,128 or 256 bytes */
#define USART_TX_BUFFER_SIZE 128     /* 2,4,8,16,32,64,128 or 256 bytes */
#define USART_RX_BUFFER_MASK (USART_RX_BUFFER_SIZE - 1)
#define USART_TX_BUFFER_MASK (USART_TX_BUFFER_SIZE - 1)


/* Prototypes */
void USART0_Init(unsigned int ubrr_val);
unsigned char USART0_Receive(void);
void USART0_Transmit(uint16_t data);






#endif /* INCFILE1_H_ */