---
title: CPU architecture: Hardware
tags: minutes,minutes2022
template: minutes
date: 2022-02-03
---

## Introduction

This meeting hopefully answers the question: what _are_ logic gates? _How_ does a logic gate work?

## CMOS

### Here's a NOT gate:

```text
             VDD
             ___
              |
          |+--+
     +---o||
     |    |+--+
     |        |
A ---+        +--- Y
     |        |
     |    |+--+
     +----||
          |+--+
              |
              |
             ---
             VSS
```

* `VDD` is the positive voltage (5V, 3V3, 1V0, etc.).

* `VSS` is the neutral voltage (0V -- it's the ground).

The top transistor is a _PMOS_ transistor (P-type MOSFET). The bottom transistor is an _NMOS_ transistor (N-type MOSFET). When `A` is set to `VSS`, then the PMOS gate is closed (the switch is closed, so power will flow) note the circle means the complement, just like in digital logic. The NMOS gate is opened, so no power will flow through the NMOS gate. Therefore, `Y` is pulled up to `VDD`! The opposite is true for when `A` is set to `VDD`.

Therefore, the logic gate is:

```text
A | Y
-----
0 | 1
1 | 0
```
### NAND Gate

Here's a NAND gate. Let's define the logic gate first and think this through:

```text
A | B || Y
----------
0 | 0 || 1
0 | 1 || 1
1 | 0 || 1
1 | 1 || 0
```

Only when `A = B = 1` will `Y` be pulled to `VSS`. In any other combination, we want `Y = VDD`. Let's think logically. If both `A` and `B` are required, we should chain them together: Y <--> A <--> B <--> VSS, so only when `A` and `B` are _both_ closed will Y connect to VSS. So, the bottom half will be with both NMOS gates will be in series. For `Y = VDD`, we want any combination where A, B, or A+B are enabled. We can create a circuit like this:

```text
                  VDD
                  ___
                   |
          +--------+---------+
          |                  |
      |+--+              |+--+
A ---o||           B ---o||   
      |+--+              |+--+
          |                  |
          +--------+---------+
                   |
                   +---------- Y 
                   | 
               |+--+ 
         A ----||    
               |+--+ 
                   | 
               |+--+ 
         B ----||    
               |+--+ 
                   | 
                   | 
                  ---
                  VSS
```

What if we want an AND gate? Well, you just tack on a NOT gate after the NAND gate. There is no way to create an AND gate in one simple set up.

## Extra CMOS

### Here's a buffer:


```text
             VDD
             ___
              | 
          |+--+ 
     +----||    
     |    |+--+ 
     |        | 
A ---+        +--- Y
     |        | 
     |    |+--+ 
     +---o||    
          |+--+ 
              | 
              | 
             ---
             VSS
```
If `A` = `VSS`, then the PMOS gate is enabled, pulling `Y` to `VSS`. The opposite is true for when `A` = `VDD`. So, the truth table is:

```text
A | Y
-----
0 | 0
1 | 1
```

What's the point of a buffer? Think of them like a repeater in Minecraft. If you're connecting to a massive bus with a lot of gates looking at this bus, you need to have a big gate in order to _pull_ this gate fast enough! Since we're doing the layout of our CPU, we can set the size of this buffer. There is a trade-off, though. With a large buffer, you'll also make the bus really big for _other_ gates trying to write to the bus, so there are strategies on _chaining multiple buffers_ with each buffer having _different_ sizes. Are you interested in this? Look up: logical effort. I recommend following [Berkerley's notes](http://bwrcs.eecs.berkeley.edu/Classes/icdesign/ee141_f05/Lectures/Notes/ComputingLogicalEffort.pdf).



### Tri-state buffer

Tri-state buffers are used to look at a shared bus. With a tri-state buffer, you can _set_ the bus to `VDD` or `VSS`. To _read_ the bus, the tri-state buffer goes... to the tri-state! It's called a `Z` state. Here's a tri-state buffer where `EN` enables the tri-state buffer to write to the output:


```text
                 VDD                  VDD
                 ___                  ___
                  |                    |
                  |                |+--+
              |+--+           +---o||
         +----||              |    |+--+
         |    |+--+           |        |
         |        |           |    |+--+
EN --+---+        +---------------o||   
     |   |        |           |    |+--+
     |   |    |+--+           |        |         
     |   +---o||        +-----+        +--- BUS OUTPUT
     |        |+--+     |     |        |
     |            |     |     |    |+--+
     +------------|----------------|   
                  |     |     |    |+--+
                  |     |     |        |
A ----------------|-----+     |    |+--+
                  |           +----||
                  |                |+--+
                  |                    |
                  |                    |
                 ---                  ---
                 VSS                  VSS
```

What's happening here is the `EN` line is acting like a gate to the buffer. If `EN` is set to `0`, then no matter what `A` is, the output will be disconnected to `VDD` and `VSS`. If `EN` is set to `1`, then the output will be `!A`.

So, the truth table is:

```text
A | EN || Y
-----------
0 |  0 || Z
1 |  0 || Z
0 |  1 || 0
1 |  1 || 1
```

## Layout

It's going to be very, very difficult to draw these in ASCII. I'll try. It's going to be academic layouts only (you don't really see transistors like this in the real world).

Tips, four types of material:

1. Silicon wells. There's n-type and p-type. n- and p- _cannot_ touch each other.

2. Polysilicon (it's actually just glass). When crossing silicon, polysilicon forms a gate. Cross n-well? n-type MOSFET. Cross p-well? p-type MOSFET.

3. Metal. This carries the bulk of voltage. Does not interact with anything except via interconnects.

4. Interconnects. This connects metal to the silicons: metal to polysilicon or metal to silicon.

In ASCII, I define metal with no middle and is wide. I define polysilicon with no middle and narrow. I define silicons with `p` as p-wells and `n` as n-wells. I define interconnections with two `x`'s.

## NOT gate
```text

     +---------------
     |         VDD    ...
     +--+  +---------
        |  |       +-+
        +--+-------| |-------+--+
        |xx|ppppppp| |ppppppp|xx|
        +--+-------| |-------+--+
                   | |       |  |
            +------+ |       |  +---+
            +------+A|       |    Y |
                   | |       |  +---+
                   | |       |  |
        +--+-------| |-------+--+
        |xx|nnnnnnn| |nnnnnnn|xx|
        +--+-------| |-------+--+
        |  |       +-+
     +--+  +---------
     |          VSS    ...
     +---------------
```

Energize A to `VDD`, then the p-type silicon will cease to flow, and the n-type silicon will start to flow. Energize A to `VSS`, then the p-type silicon will start to flow and the n-type silicon will cease to flow.

When IBM says things like "9 nanometer transistors" they mean that the polysilicon is 9 nanometers thin.

## NAND gate
```text

     +----------------------------------------------------
     |
     |         VDD     ...
     |
     +--+  +---------------------------------------+  +---
        |  |       +-+              +-+            |  |
        +--+-------| |-----+--+-----| |------------+--+
        |xx|ppppppp| |ppppp|xx|ppppp| |pppppppppppp|xx|
        +--+-------| |-----+--+-----| |------------+--+
                   | |     |  |     | |
                   | |     |  +-----|-|---------------+
                   | |     |        | |               |
                   | |     +--------|-|------------+  |
                   | |              | |            |  |
            +------+ |              | +----+       |  +---+
            +------+A|              |B+----+       |    Y |
                   | |              | |            |  +---+
                   | |              | |            |  |
        +--+-------| |--------------| |------------+--+
        |xx|nnnnnnn| |nnnnnnnnnnnnnn| |nnnnnnnnnnnn|xx|
        +--+-------| |--------------| |------------+--+
        |  |       +-+              +-+                
     +--+  +---------------------------------------------
     |                 
     |          VSS    ...
     |
     +---------------------------------------------------
```

You should be able to follow what is happening here. Think of each transistor connection like a faucet and p-type goes the wrong way, so if `A = 1`, then the p-type junction is broken/blocked while the n-type junction is open/free flowing. 

Looking at the n-type silicon, you'll need both `A` and `B` to be 1 in order for the connection between `Y` and `VSS` to be made. 

Looking at the p-type silicon, if `A` is 0, then that connection is crossed: `VDD` has a connection to `Y`. If `B` is 0, then that connection is crossed: `VDD` has a connection to `Y`. When both are `0`, then energy flows from both sides, but it really doesn't matter! It's all going to be `VDD`!

## Mux

Let's reduce the mux from [last week's design](meeting03.html) to a CMOS-level design before drawing its layout:

```text
        +-----------------------+
        |                       |
        |                     -----
        |       VDD           -----
        |       ___           |   |
        |        |       A ---+   +---+
        |    |+--+            |   |   |
        +----||               -----   |
        |    |+--+            --o--   |
        |        |              |     |
   C ---+        +--------------+     +--- Y
        |        |              |     |
        |    |+--+            -----   |
        +---o||               -----   |
        |    |+--+            |   |   |
        |        |       B ---+   +---+
        |        |            |   |
        |       ---           -----
        |       VSS           --o--
        |                       |
        +-----------------------+
```

Cool, we'll do it [one piece at a time](https://www.youtube.com/watch?v=uErKI0zWgjg). Let's start with the NOT gate with some extra space:

```text

     +---------------
     |
     |
     |         VDD    ...
     +--+  +---------
        |  |       +-+
        +--+-------| |-------+--+--------------------------
        |xx|ppppppp| |ppppppp|xx|pppppppppppppppppppppppppp ...
        +--+-------| |-------+--+--------------------------
                   | |       |  |
            +------+ |       |  |
            +------+C|       |  |
                   | |       |  |
                   | |       |  |
                   | |       |  +---+
                   | |       |    Y |
                   | |       |  +---+
                   | |       |  |
                   | |       |  |
                   | |       |  |
                   | |       |  |
                   | |       |  |
                   | |       |  |
                   | |       |  |
        +--+-------| |-------+--+
        |xx|nnnnnnn| |nnnnnnn|xx|
        +--+-------| |-------+--+
        |  |       +-+
     +--+  +---------
     |
     |
     |          VSS    ...
     +---------------
```

Easy peasy, let's go on:


```text

+------------+          +----------+              +-------+
|            |          |          |              |       |
|            |          |     B    |              |    A  | 
|      VDD   |          |          |              |       |
|  +---------+          +--+  +----+              +----+  |
|  |       +-+             |  |   +-+            +-+   |  |
+--+-------| |-------+--+  +--+---| |----+--+----| |---+--+
|xx|ppppppp| |ppppppp|xx|  |xx|ppp| |pppp|xx|pppp| |ppp|xx|
+--+-------| |-------+--+  +--+---| |----+--+----| |---+--+
           | |       |  |         | |    |  |    | |  
           | +-------|--|---------+ |    |  |    | |  
           |C+-------|--|---------+C|    |  |    C*|  
           | |       |  |         | |    |  |    | |  
           | |       |  |         | |    |  |    | |  
           | |       |  |        ++-+    |  +----| |-------      
           | |       |C*|        |xx|    |       | |    Y  
           | |       |  |        +--|    |  +----| |-------      
           | |       |  |        |  |    |  |    | |  
           | |       +--+        | C|    |  |    | |  
           | |       |xx+--------|--|----|--|----+ |    
           | |       +--+--------|--|----|--|----+ |  
           | |       |  |        +--+    |  |    | |  
           | |       |  |        |xx|    |  |    | |  
           | |       |  |        ++-+    |  |    | |  
+--+-------| |-------+--+  +--+---| |----+--+----| |---+--+
|xx|nnnnnnn| |nnnnnnn|xx|  |xx|nnn|C|nnnn|xx|nnnn| |nnn|xx|
+--+-------| |-------+--+  +--+---| |----+--+----| |---+--+
|  |       +-+             |  |   +-+            +-+   |  |
|  +---------+          +--+  +----+              +----+  |
|            |          |          |              |       |
|            |          |     A    |              |    B  |
|       VSS  |          |          |              |       |
-------------+          +----------+              +-------+
```

Yeah, it gets complicated fast. And I didn't even connect up both A and B. I have the two isolated. You can extend the silicon line and weave a metal line in between there, but that just gets messy pretty fast and especially in ASCII, it's not going to go anywhere clean. That's where software comes in handy.


You can use [Magic VLSI](http://opencircuitdesign.com/magic/) to draw out the design and then export the design out into SPICE and use LTSPICE to simulate your CPU. It's honestly difficult, but CMOS layout in general is very difficult. Michigan Tech gives [Cadence Virtuoso](https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/layout-design/virtuoso-layout-suite.html) (which is awesome and a beautiful piece of software) but it's about ~$500,000 for a single license. Fuck you. Magic VLSI is free. 

To install: `emerge --ask sci-electronics/magic` or I think `apt install magic` works too. You'll need X running to run this software.

LTspice is a loser and only runs on Windows, but WINE can easily run LTspice. 

Do you really want to learn more? Good. Here's _a lot of material that I've collected over the years._

* [http://users.ece.utexas.edu/~mcdermot/ee460r_fall_2018.htm](http://users.ece.utexas.edu/~mcdermot/ee460r_fall_2018.htm)

* [http://cmosedu.com/jbaker/courses/ee421_ecg621/f18/ee421_ecg621.htm](http://cmosedu.com/jbaker/courses/ee421_ecg621/f18/ee421_ecg621.htm)

* [http://pages.hmc.edu/harris/cmosvlsi/4e/index.html](http://pages.hmc.edu/harris/cmosvlsi/4e/index.html)

* [http://www.righto.com/2015/10/inside-ubiquitous-741-op-amp-circuits.html](http://www.righto.com/2015/10/inside-ubiquitous-741-op-amp-circuits.html)

