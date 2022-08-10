# Bitwise operation

Operations performed on individual bits. In Java bitwise operators can be
applied only on integer type i.e. long, int, short, char and byte. There are
following operators-

| Operator | Result                           |
|:---------|:---------------------------------|
| ~        | Bitwise unary NOT                |
| &        | Bitwise AND                      |
| |        | Bitwise OR                       |
| ^        | Bitwise NOT                      |
| >>       | Shift right                      |
| >>>      | Shift right zero fill            |
| <<       | Left shift                       |
| &=       | Bitwise AND assignment           |
| |=       | Bitwise OR assignment            |
| ^=       | Bitwise exclusive OR assignment  |
| >>=      | Shift right assignment           |
| >>>=     | Shift right zero fill assignment |
| <<=      | Shift left assignment            |

## Left Shift

value << num

Shift all the bits in the `value` to the left by `num` times.

`2<<1`

The original bits are `00000010`. Each bit is shifted left once. So, after shift
the value is `00000100`.

In each shift the left most bit gets lost and 0 is inserted to the right. Also
notice that each shift doubles the value. Before shift the value was 2 and after
shift it has become 4. Therefore, many programmers use this as an efficient way
of multiplying by 2.

In Java there are 5 different integer types: byte, char, short, int and long.
Byte and short is type promoted to int when evaluating an expression. Therefore,
     when we left shift on byte and short, the left most bits doesn't get lost.
     Because even though byte has 4 bits, it gets promoted to int whih has 32
     bits. So, left shifting bits in byte doesn't discard the higher order bits.
     To resolve this issue, we need to cast the result to byte after shifting.
     See the following example:

```java
byte num1=64;
byte result;
int intResult;
intResult = num1 << 2;
result = (byte) (num1<<2);
```

The value of the intResult will be 256. This is because the `num1` has been
promoted to in to process the expression. So shifting the bit 1 place left puts
the bit in the 256 value position.

The value of result will be 0. This is because we are casting the int result to
byte.

## Right Shift

Shift all the bits in the `value` to the right by `num` times.

`2>>1`

The original bits are 00000010. After shift it is 00000001.
Right shift divides the number by 2 and discards the remainder.

In case of right shift, the left most bits are filled with previous contents of
left most bits. If the left most bit is 0, the shift fills the left most
positions with 0, if 1, fills with 1.



