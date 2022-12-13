# Tax code calculator

Graphic interface to calculate and show the italian tax code and national card of services (CNS)

## Index

1. [Calculation rules](#calculation-rules)
   - [Surname chars](#surname-chars)
   - [Name chars](#name-chars)
   - [Year code](#year-code)
   - [Month code](#month-code)
   - [Day code](#day-code)
   - [Municipality code](#municipality-code)
   - [CIN code](#cin-code)
   - [Omocoding](#omocoding-issues)
2. [Requirements](#requirements)

## Calculation rules

The italian tax code is a 16-chars long alphanumerical string composed by 3 chars from the surname, 3 chars from the name, the birth date, a code to identify the municipality of birth and a control character (CIN).

### example

Mario Rossi is born in Milan on the 4th of July 1989 so his code would be: `RSSMRA89L04F205S`

|Surname|Name|Year|Month|Day|Municipality|CIN|
|---|---|---|---|---|---|---|
|RSS|MRA|89|L|04|F205|S|

So, how is it done?

### Surname chars

Surname chars are 3 characters taken, giving priority to consonants, from left to right.
If the consonants are not enough (ex. if surname is Pisu), the vowels are taken from left to right.
If, using both vowels and consonants, the limit of 3 chars is not reached `X`s are added to the end of the string.

To calculate surname characters for womens, is used only the maiden name.

### Name chars

Name chars are 3 characters taken, giving priority to consonants, from left to right.
If the consonants are more than 3, in the code are used the first, third and fourth consonants.
Else, if the consonants are less than 3, the vowels are taken from left to right.
If, using both vowels and consonants, the limit of 3 chars is not reached `X`s are added to the end of the string.

### Year code

The year code is composed by the last two digits of the birth year.

### Month code

The month code is calculated by converting the birth month to a single letter.
|Month|Letter|Month|Letter
|---|---|---|---|
JANUARY| A| JULY| L
FEBRUARY| B| AUGUST| M
MARCH| C| SEPTEMBER| P
APRIL| D| OCTOBER| R
MAY| E| NOVEMBER| S
JUNE| H| DECEMBER| T

### Day code

The day code is the day of birth of the person. If the person is a woman, the code is the sum of  the day + 40.

### Municipality code

The municipality code is the code that identifies the place of birth.

### CIN code

The control character is calculated through an algorithm using the first 15 characters partial code.

- Divide characters in even and odd positions
- Convert every character to a value using the tables below
- Sum every value and divide by 26 and get the remainder
- Convert the remainder to a character and add it to the end of the string

#### Even positions

|Character| Value|Character|Value|Character|Value|Character|Value
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|0| 0| 9| 9| I| 8|  R| 17|
|1| 1| A| 0| J| 9|  S| 18|
|2| 2| B| 1| K| 10| T| 19|
|3| 3| C| 2| L| 11| U| 20|
|4| 4| D| 3| M| 12| V| 21|
|5| 5| E| 4| N| 13| W| 22|
|6| 6| F| 5| O| 14| X| 23|
|7| 7| G| 6| P| 15| Y| 24|
|8| 8| H| 7| Q| 16| Z| 25|

#### Odd positions

|Character| Value|Character|Value|Character|Value|Character|Value
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
0| 1|  9| 21| I| 19|R| 8
1| 0|  A| 1|  J| 21|S| 12
2| 5|  B| 0|  K| 2| T| 14
3| 7|  C| 5|  L| 4| U| 16
4| 9|  D| 7|  M| 18|V| 10
5| 13| E| 9|  N| 20|W| 22
6| 15| F| 13| O| 11|X| 25
7| 17| G| 15| P| 3| Y| 24
8| 19| H| 17| Q| 6| Z| 23

#### Remainder conversion

|Character| Value|Character|Value|Character|Value|
|:---:|:---:|:---:|:---:|:---:|:---:|
|0| A| 9| J|  18| S
|1| B| 10| K| 19| T
|2| C| 11| L| 20| U
|3| D| 12| M| 21| V
|4| E| 13| N| 22| W
|5| F| 14| O| 23| X
|6| G| 15| P| 24| Y
|7| H| 16| Q| 25| Z
|8| I| 17| R|

### Omocoding issues

If two or more people are born in the same day in the same place and have the same name, their tax code would be the same. To avoid code duplication, starting from the right every numerical character is converted to a letter using the table. After this conversion a new CIN code is calculated.

|Value | Character|
|:---:|:---:|
|0| L|
|1| M|
|2| N|
|3| P|
|4| Q|
|5| R|
|6| S|
|7| T|
|8| U|
|9| V|

## Requirements

- [Python 3.9.x or newer](https://www.python.org/downloads/)
- pip requirements (`pip install -U -r requirements.txt`)
