; Detector de palíndromos
bloco main 01
    01 a -- A i 10
    01 b -- B i 20
    01 * -- * i rejeite
    10 moveFim 11
    20 moveFim 21

    ; leu a
    11 iniEsq 12
    12 a -- A i 30
    12 b -- * i 70
    12 _ -- * i 60

    ; leu b
    21 iniEsq 22
    22 a -- * i 70
    22 b -- B i 30
    22 _ -- * i 60

    30 moveIni 31
    31 iniDir 32
    32 _ -- * e 60
    32 * -- * i 01

    60 sim *
    70 nao *
fim ; main

; move para último caractere da palavra
bloco moveFim 01
    01 _ -- * e retorne
    01 * -- * d 01
fim ; moveFim

; move para primeiro caractere da palavra
bloco moveIni 01
    01 _ -- * d retorne
    01 * -- * e 01
fim ; moveIni

; recua até caractere minúsculo ou _
bloco iniEsq 01
    01 _ -- * i retorne
    01 a -- * i retorne
    01 b -- * i retorne
    01 * -- * e 01
fim ; iniEsq

; avança até caractere minúsculo ou _
bloco iniDir 01
    01 _ -- * i retorne
    01 a -- * i retorne
    01 b -- * i retorne
    01 * -- * d 01
fim ; iniDir

; palavra é palíndromo
bloco sim 01
    01 moveFim 02
    02 * -- * d 03
    03 * -- _ d 04
    04 * -- S d 05
    05 * -- I d 06
    06 * -- M d aceite
fim ; sim

; palavra não é palíndromopare
bloco nao 01
    01 moveFim 02
    02 * -- * d 03
    03 * -- _ d 04
    04 * -- N d 05
    05 * -- A d 06
    06 * -- O d rejeite
fim ; nao
