/*********************************************************
	Developer: Leon Tran, Mark Luna, Brian Pham
	Date: 05/06/17
	Contact: leontran95@gmail.com, tec9360.therealbws@gmail.com, Brian.qk.pham@gmail.com
	
	Version: 6
	Controls the position of the magnets based off the readings of the readings of the hall
	effect sensors. Utilizes PID controls to maintain a stable postion
	
	Current: PI Control
		-A LUT is used instead of a proportion value to maintain stability
		-Integral is used to fine tune the position of the magnet
	
**********************************************************/


// PIC24EP64GP202 Configuration Bit Settings

// 'C' source line config statements

// FICD
#pragma config ICS = PGD2               // ICD Communication Channel Select bits (Communicate on PGEC1 and PGED1)
#pragma config JTAGEN = OFF             // JTAG Enable bit (JTAG is disabled)

// FPOR
#pragma config ALTI2C1 = OFF            // Alternate I2C1 pins (I2C1 mapped to SDA1/SCL1 pins)
#pragma config ALTI2C2 = OFF            // Alternate I2C2 pins (I2C2 mapped to SDA2/SCL2 pins)
#pragma config WDTWIN = WIN25           // Watchdog Window Select bits (WDT Window is 25% of WDT period)

// FWDT
#pragma config WDTPOST = PS32768        // Watchdog Timer Postscaler bits (1:32,768)
#pragma config WDTPRE = PR128           // Watchdog Timer Prescaler bit (1:128)
#pragma config PLLKEN = ON              // PLL Lock Enable bit (Clock switch to PLL source will wait until the PLL lock signal is valid.)
#pragma config WINDIS = OFF             // Watchdog Timer Window Enable bit (Watchdog Timer in Non-Window mode)
#pragma config FWDTEN = ON              // Watchdog Timer Enable bit (Watchdog timer always enabled)

// FOSC
#pragma config POSCMD = NONE            // Primary Oscillator Mode Select bits (Primary Oscillator disabled)
#pragma config OSCIOFNC = OFF           // OSC2 Pin Function bit (OSC2 is clock output)
#pragma config IOL1WAY = ON             // Peripheral pin select configuration (Allow only one reconfiguration)
#pragma config FCKSM = CSECMD           // Clock Switching Mode bits (Clock switching is enabled,Fail-safe Clock Monitor is disabled)

// FOSCSEL
#pragma config FNOSC = FRC              // Oscillator Source Selection (Internal Fast RC (FRC))
#pragma config IESO = OFF               // Two-speed Oscillator Start-up Enable bit (Start up with user-selected oscillator source)

// FGS
#pragma config GWRP = OFF               // General Segment Write-Protect bit (General Segment may be written)
#pragma config GCP = OFF                // General Segment Code-Protect bit (General Segment Code protect is Disabled)

#define HCurrentYPos _LATA2 
#define HCurrentYNeg _LATB9 
#define HCurrentXNeg _LATA4 
#define HCurrentXPos _LATB15
#define SCALAR_NX_BITS 4
#define SCALAR_NY_BITS 3


// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

#include <xc.h>
#include <p24EP64GP202.h>

void LUTSetup(void);
void initializeADC(void);
void initializeClk(void);
void initializePWMOut(void);
void initializePins(void);


unsigned long count = 0;

int ADCValues[4] = {0, 0, 0, 0}; // Store AD result
int ADR_H1 = 0;
int ADR_H2 = 0;

//Integral Constant
int NX = (1<<SCALAR_NX_BITS);
int NY = (1<<SCALAR_NY_BITS);

int derivativeX = 0;
int derivativeY = 0;
int integralX = 0;
int integralY = 0;

float KpX = 2.4; //2.4
float KpY = 1.43; //1.4
float KdX = 10;
float KdY = 14;
int prev_errorX = 0;
int prev_errorY = 0;

int errorX = 0;
int errorY = 0;

//Hall Effect Readings for different Situations
int stableX = 2; // To be determined
int stableY = 2; // To be determined
int emptyX = 14;
int emptyY = 7;
int emptyCurrentX = 12;
int emptyCurrentY = 4;

int powerX = 0;
int powerY = 0;

int pwmOutX = 0;
int pwmOutY = 0;

int maxPWM = 2700;      //72%
int maxX = 1;
int maxY = 1;

int LUTX[200];
int LUTY[200];

int main(void) {
    LUTSetup();
    
    initializeADC();
    initializeClk();
	initializePins();
    initializePWMOut();

    while (1) {    
        _LATB13 = HCurrentYPos;
        _LATB12 = HCurrentYNeg;     

        _LATB11 = HCurrentXPos;
        _LATB14 = HCurrentXNeg;     
    }

    return 0;
}

void __attribute__((__interrupt__, no_auto_psv)) _T2Interrupt(void) {
    int i;
    AD1CON1bits.SAMP = 1; //start sampling
    for (i = 0; i < 2; i++);     
    AD1CON1bits.SAMP = 0; //stop sampling, start converting
    _T2IF = 0;
}

// ================================================================
// Record values read from Hall sensors and calculate PID values
// ================================================================s

void __attribute__((__interrupt__, no_auto_psv)) _AD1Interrupt(void) 
{    
    // E - W
    // N - S
    ADCValues[0] = ADC1BUF1; // Read the AN0 conversion result for +X
    ADCValues[1] = ADC1BUF2; // Read the AN1 conversion result for +Y
    ADCValues[2] = ADC1BUF3; // Read the AN2 conversion result for -X
    ADCValues[3] = ADC1BUF0; // Read the AN3 conversion result for -Y

    errorX = ADCValues[3] - ADCValues[0]; // Displacement in X direction
    errorY = ADCValues[2] - ADCValues[1]; // Displacement in Y direction

    derivativeX = prev_errorX - errorX;
    derivativeY = prev_errorY - errorY;

    integralX = ((errorX*NX) + integralX*(NX-1)); // 20 ms time (?)
    integralY = ((errorY*NY) + integralY*(NY-1)); // 20 ms time (?)
    
    if(integralX > maxX)
    {
        integralX = maxX;
    }
    else if(integralX < -maxX) 
    {
        integralX = -maxX;
    }
    
    if(integralY > maxY)
    {
        integralY = maxY;
    }
    else if(integralY < -maxY) 
    {
        integralY = -maxY;
    }

    prev_errorX = errorX; // For next time
    prev_errorY = errorY;

    powerX = errorX*KpX;
    powerY = errorY*KpY; 
    
    //powerX = (errorX-stableX)*KpX + (integralX>>SCALAR_N_BITS); //offset x and y
    //powerY = (errorY-stableY)*Kpy + (integralY>>SCALAR_N_BITS); 

    // controls W and E direction 2/9:0/1 E repels - OC1R
    if (powerY > 0) 
	{
        HCurrentYPos = 0;
        HCurrentYNeg = 1;
    } 
	else 
	{
        powerY = -powerY;
        HCurrentYPos = 1;
        HCurrentYNeg = 0;
    }
    if (powerX > 0) 
	{
        HCurrentXPos = 0;
        HCurrentXNeg = 1;
    } 
	else 
	{
        powerX = -powerX;
        HCurrentXPos = 1;
        HCurrentXNeg = 0;
    }
    
    
	//Checks to see if the magnet is on the base
    if(!((powerX >= emptyCurrentX-3 &&  powerX <= emptyCurrentX+3) && (powerY >= emptyCurrentY-3 &&  powerY <= emptyCurrentY+3)) &&
       !((powerX >= emptyX-3 &&  powerX <= emptyX+3) && (powerY >= emptyY-3 &&  powerY <= emptyY+3)))
    {
        pwmOutX = LUTX[powerX] + (integralX>>SCALAR_NX_BITS);
        pwmOutY = LUTY[powerY] + (integralY>>SCALAR_NY_BITS);                      
        
		//PWM that drives the H-Bridges
        OC2R = (pwmOutX > 0 && pwmOutX < maxPWM) ? pwmOutX :
                pwmOutX > maxPWM ? maxPWM :
                -pwmOutX;
        OC1R = (pwmOutY > 0 && pwmOutY < maxPWM) ? pwmOutY :
                pwmOutY > maxPWM ? maxPWM :
                -pwmOutY;
    }
    else            //No Magnet
    {
        OC2R = 0;
        OC1R = 0;
    }
    
    AD1CON1bits.DONE = 0;
    _AD1IF = 0; // Clear conversion done status bit
}

void LUTSetup(void) {
    int x = 0;
    int y = 0;
    int intervalX = 140;   // 140/3461 = 4%
    int intervalY = 220;   // 220/3461 = 6%
    int stableRangeX = 1;
    int stableRangeY = 1;

    int xCount = 1;
    int yCount = 1;

    int baseX = 2100;        //50% 1900
    int baseY = 1600;        //50%

    maxX = (intervalX * NX > maxPWM) ? maxPWM : intervalX * NX;
    maxY = (intervalY * NY > maxPWM) ? maxPWM : intervalY * NY;
    
	//Constructs a unimodal array based off the stable position
    for(x = stableX; x>=0; x--)
    {
        if (x  != stableX && (x < stableX - stableRangeX || x > stableX + stableRangeX ))                             //Expected PWM Output
        {
            int addX = xCount * intervalX;                 
            LUTX[x] = (baseX + addX < maxPWM) ? baseX + addX : maxPWM;
            xCount++;
        } 
        else                                                     //Stable Position
        {
            LUTX[x] = 0;
        }
    }

    xCount = 1;
    for(x = stableX; x < 200; x++)
    {
        if (x  != stableX  && (x < stableX - stableRangeX || x > stableX + stableRangeX) )                             //Expected PWM Output
        {
            int addX = xCount * intervalX;                 
            LUTX[x] = (baseX + addX < maxPWM) ? baseX + addX : maxPWM;
            xCount++;
        } 
        else                                                     //Stable Position
        {
            LUTX[x] = 0;
        }
    }
    
    for(y = stableY; y>=0; y--)
    {
        if (y  != stableY  && (y < stableY - stableRangeY|| y > stableY +stableRangeY ) )                             //Expected PWM Output
        {
            int addY = yCount * intervalY;                 
            LUTY[y] = (baseY + addY < maxPWM) ? baseY + addY : maxPWM;
            yCount++;
        } 
        else                                                     //Stable Position
        {
            LUTY[y] = 0;
        }
    }

    yCount = 1;
    for(y = stableY; y < 200; y++)
    {
        if (y  != stableY && (y < stableY - stableRangeY || y > stableY + stableRangeY ))                             //Expected PWM Output
        {
            int addY = yCount * intervalY;                 
            LUTY[y] = (baseY + addY < maxPWM) ? baseY + addY : maxPWM;
            yCount++;
        } 
        else                                                     //Stable Position
        {
            LUTY[y] = 0;
        }
    }
    
}

void initializeADC(void)
{
      /* ADC initialization */
    ANSELA = 0x0003; // use only AN0-AN1 as analog
    ANSELB = 0x0003; //use only AN2-AN3 (RB0, RB1) as analog)
    // input pins
    _TRISA0 = 1; // analog input AN0
    _TRISA1 = 1; // analog input AN1
    _TRISB0 = 1; // analog input AN2
    _TRISB1 = 1; // analog input AN3

    /* Initialize and enable ADC module */
    AD1CON1 = 0x0008; // Enable simultaneous sampling and manual sampling
    AD1CON1bits.SSRCG = 0;
    AD1CON1bits.SSRC = 0b000; // manual mode (manually toggle SAMP)
    AD1CON2 = 0x0300; // Sample 4 channels (CH0, CH1, CH2, and CH3)
    AD1CON3bits.ADRC = 0; // using system clock as ADC clock
    //AD1CON3bits.ADCS = 5; //Tad = Tcy * (ADCS + 1) = (1/70 MHz) * 6 = 85.716 ns (11.7 MHz)
    AD1CON3bits.ADCS = 255; //Tad = Tcy * (ADCS + 1) = (1/70 MHz) * 200 = 85.716 ns (11.7 MHz)
    //AD1CON3bits.SAMC = 2; // auto-sample time bits set to 2 Tad (required when SSRCG = 0 and SSRC = 0b111)
    AD1CON3bits.SAMC = 31; // auto-sample time bits set to 31 Tad (required when SSRCG = 0 and SSRC = 0b111)
    AD1CON4 = 0x0000; // Conversion results stored in ADC1BUF0 - ADC1BUFF registers, no DMA, allocate 1 word of buffer to each analog input
    AD1CSSH = 0x0000; // Register is all 0 by default
    AD1CSSL = 0x0000; // Register is all 0 by default
    AD1CHS0bits.CH0SA = 3; // Select AN3 for CH0 +ve input
    AD1CHS0bits.CH0NA = 0; // Select Vref- for CH0 -ve input
    AD1CHS123bits.CH123SA = 0; //Select AN0 for CH1 +ve input
    // Select AN1 for CH2 +ve input
    // Select AN2 for CH3 +ve input
    AD1CHS123bits.CH123NA = 0; // Select Vref- for CH1/CH2/CH3 -ve inputs
    AD1CON1bits.ADON = 1; // Turn on ADC module

    /* Reset AD1 conversion done status bit/interrupt flag */
    IFS0bits.AD1IF = 0;
    /* Enable AD1 interrupt */
    IEC0bits.AD1IE = 1;

    /* Reference clock output to output clock to a pin (testing to see what clock is set) */
    //RPOR2bits.RP38R = 0b110001; // RP38 used as Reference Clock Output
    //REFOCONbits.ROON = 1;
}

void initializeClk(void)
{
    CLKDIVbits.FRCDIV = 0; // FRC divided by 1
    CLKDIVbits.PLLPOST = 0; // output divided by 2 (lowest divisor available here)
    CLKDIVbits.PLLPRE = 0; // input divided by 2 (lowest divisor available here)
    PLLFBDbits.PLLDIV = 73; // PLL multiplier set to 75 (73 + 2)
    OSCTUNbits.TUN = 0; // center frequency tuning of FRC oscillator (nominal, 7.37 MHz)
    // Initiate Clock Switch to FRC oscillator with PLL (NOSC=0b001)
    __builtin_write_OSCCONH(0x01);
    __builtin_write_OSCCONL(OSCCON | 0x01);
    // Wait for Clock switch to occur
    while (OSCCONbits.COSC != 0b001);
    // Wait for PLL to lock
    while (OSCCONbits.LOCK != 1);
    /* By calculation, this setup will result in Fosc = 138.187 MHz or ~70 MHz Fcy / ~70 MIPS / ~14 ns Tcy */

    /* Timer 2 Setup */
    T2CONbits.TCKPS = 2; // 1:64 prescaler on Timer2
    PR2 = 300; // 10 kHz timer/100 microsecond period     1 ms 
    T2CONbits.TON = 1; // Start timer

    /* Reset timer 2 interrupt flag */
    IFS0bits.T2IF = 0;
    /* Enable Timer 2 interrupt */
    IEC0bits.T2IE = 1;

}

void initializePWMOut(void)
{
     /* One PWM output configured here */
    RPOR2bits.RP39R = 16; // RP39 pin tied to Output Compare 1 output
    // Init Output Compare 1
    /* A timer can be used as the source if we need a smaller frequency PWM */
    OC1CON1bits.OCTSEL = 0b111; // Peripheral clock used as clock source
    OC1CON1bits.OCM = 0b110; // Edge-aligned PWM mode
    OC1CON2bits.SYNCSEL = 0b11111; // Trigger/sync source set to OC1RS (max value to compare to)

    /* 2nd PWM output configured here */
    RPOR3bits.RP40R = 17; // RP40 pin tied to Output Compare 2 output
    OC2CON1bits.OCTSEL = 0b111;
    OC2CON1bits.OCM = 0b110;
    OC2CON2bits.SYNCSEL = 0b11111;
    /* RP39 will be set low until OC1TMR counts to OC1R, RP39 will be set high
     afterwards until OC1TMR counts to OC1RS, then repeat */
    OC1RS = 3461; // Will generate 20 kHz PWM signal with peripheral clock as clock source
    OC1R = 0; // The PWM control register
    OC2RS = 3461;
    OC2R = 0;
}

void initializePins(void)
{
	/* H-Bridge 1 */
    _TRISA2 = 0; // output on RA2 (INA)
    _TRISB9 = 0; //output on RB9 (INB)
    HCurrentYPos = 0; // initial output 0
    HCurrentYNeg = 0;

    /* H-Bridge 2 */
    _TRISA4 = 0; // output on RA4 (INA)
    _TRISB15 = 0; // output on RB15 (INB)
    HCurrentXNeg = 0; // initial output 0
    HCurrentXPos = 0;

    // LED
    _TRISB14 = 0; //LED 2/0 X-
    _LATB14 = 1;
    _TRISB13 = 0; //LED 3/1 Y+
    _LATB13 = 1;
    _TRISB12 = 0; //LED 4/2 Y-
    _LATB12 = 1;
    _TRISB11 = 0;
    _LATB11 = 1; //LED 5/3 X+
}