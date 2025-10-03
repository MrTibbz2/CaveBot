function roundToDecimal(num, decimalPlaces) {
      const multiplier = Math.pow(10, decimalPlaces);
      return Math.round(num * multiplier) / multiplier;
    }
export function BotSiml() {
    bt = window.bot;
    plt = window.DebugPlotPoint;
    function pltv(sensor, value) {
        // plots a point with variance for a sensor reading, simulating error of real sensor and movement.
        let variance = 1.5; // cm
        let v = (Math.random() * variance * 2) - variance; // random number between -variance and +variance
        plt(sensor, value + roundToDecimal(v, 1))

    }
    function pltside(side, value) { // plots 2 points for a side reading, eg leftfront and leftback at the same time.
        // saves writing time.
        if (side == "front") {
            pltv("frontleft", value);
            pltv("frontright", value);
        } else if (side == "back") {
            pltv("backleft", value);
            pltv("backright", value);
        } else if (side == "left") {
            pltv("leftfront", value);
            pltv("leftback", value);
        } else if (side == "right") {
            pltv("rightfront", value);
            pltv("rightback", value);
        }
    }
    // mov: movement the bot makes
    // hal: a specific stretch of straight hallway in the maze.
    // botrel: bot relative, eg botrel right wall means the wall on the right side of the bot.
    // angle: 0 is north, 90 is east, 180 is south, 270 is west.
    // the bot starts at the beginning of HAL1, facing north, and ends at the end of HAL6 facing north.
    function sim1() {
        // bot angle at 0. north. moving forward through a corridor.
        //HAL1 ENTRY. angle: 0. total movs for this HAL: 5
        pltside("left", 10); // mov1 | hal1
        pltside("right", 10);
        pltside("front", 50);
        pltside("back", 10); // takes initial readings and begins to move.
        
        bt.move(10);
        pltside("left", 10); // mov2 | hal1
        pltside("right", 10); // same walls as move1, different values addjusted for botpos.
        pltside("front", 40);
        pltside("back", 20);
        
        bt.move(10);
        pltside("left", 10); // mov3 | hal1
        pltside("right", 10); 
        pltside("front", 30);
        pltside("back", 30);
        
        bt.move(10);
        pltside("left", 10); // mov4 | hal1
        pltv("rightfront", 90);//frontsensor now sees the opening to HAL2, right wall is now far away.
        pltv("rightback", 10);
        pltside("front", 20);
        pltside("back", 40);
        
        bt.move(10);
        pltside("left", 10); // mov5 | hal1 to hal2
        pltside("right", 90); // entering HAL2, right wall is now far away, the end of HAL2 corridor.
        pltside("front", 10);
        pltside("back", 50);
        
        
        bt.rotate(90); // bot turns right, now facing east.
        
        //HAL2 ENTRY. angle: 90. total movs for this HAL: 8
        bt.move(10);
        pltside("left", 10); // mov1 | hal2
        pltside("right", 50); // right wall is now what was the back wall.
        pltside("front", 80);
        pltside("back", 20);
        
        bt.move(10);
        pltside("left", 10); // mov2 | hal2
        pltv("rightfront", 5); // right wall is now getting closer, as its a wall of HAL2.
        pltv("rightback", 50);
        pltside("front", 70);
        pltside("back", 30);

        bt.move(10); // mov3 | hal2
        pltside("left", 10);
        pltside("right", 5); // both right sensors now see the right wall of HAL2.
        pltside("front", 60);
        pltside("back", 40);
        
        bt.move(10); // mov4 | hal2
        pltside("left", 10);
        pltside("right", 5);
        pltside("front", 50);
        pltside("back", 50);
        
        bt.move(10); // mov5 | hal2
        pltside("left", 10);
        pltside("right", 5);
        pltside("front", 40);
        pltside("back", 60);
        
        bt.move(10);
        pltside("left", 10); // mov6 | hal2
        pltside("right", 5);
        pltside("front", 30);
        pltside("back", 70);
        
        bt.move(10);
        pltside("left", 10); // mov7 | hal2
        pltv("rightfront", 95); // frontright sensor now sees the opening to HAL3, right wall is now far away.
        pltv("rightback", 5);
        pltside("front", 20);
        pltside("back", 80);

        bt.move(10); // mov8 | hal2 to hal3
        pltside("left", 10);
        pltside("right", 95); // entering HAL3, botrel right wall is now far away, the end of HAL3 corridor.
        pltside("front", 10);
        pltside("back", 90);
        
        bt.rotate(90); // bot turns right, now facing south.
        
        //HAL3 ENTRY. angle: 180. total movs for this HAL: 15
        // note: loops back at the end, the bottom wall is a dead end, opening to the right.
        bt.move(10);
        pltside("left", 10); // mov1 | hal3
        pltv("rightfront", 5); // new right wall for HAL3
        pltv("rightback", 90); // right wall is now what was the back wall.
        pltside("front", 85);
        pltside("back", 20);

        bt.move(10);
        pltside("left", 10); // mov2 | hal3
        pltside("right", 5); // both right sensors now see the right wall of HAL3.
        pltside("front", 75);
        pltside("back", 30);

        bt.move(10); // mov3 | hal3
        pltside("left", 10);
        pltside("right", 5);
        pltside("front", 65);
        pltside("back", 40);

        bt.move(10); // mov4 | hal3
        pltv("leftfront", 95); // opening to HAL4 on botrel_left side.
        pltv("leftback", 10);
        pltside("right", 5);
        pltside("front", 55);
        pltside("back", 50);

        bt.move(10); // mov5 | hal3
        pltside("left", 95); // botrel_left wall is now far away, the end of HAL4 corridor.
        pltside("right", 5);
        pltside("front", 45);
        pltside("back", 60);

        bt.move(10); // mov6 | hal3
        pltside("left", 95);
        pltside("right", 5);
        pltside("front", 35);
        pltside("back", 70);
        
        bt.move(10); // mov7 | hal3
        pltv("leftfront", 10); // wall of HAL3 and not opening to HAL4.
        pltv("leftback", 95);
        pltside("right", 5);
        pltside("front", 25);
        pltside("back", 80);
        
        bt.move(10); // mov8 | hal3
        pltside("left", 10);
        pltside("right", 5);
        pltside("front", 15);
        pltside("back", 90);
        
        bt.move(10);
        pltside("left", 10); // mov9 | hal3
        pltside("right", 5);
        pltside("front", 5);
        pltside("back", 100);
        
        bt.move(5);
        pltside("left", 10); // mov10 | hal3
        pltside("right", 5);
        pltside("front", 0);
        pltside("back", 105);

        bt.rotate(-90); 
        // bot turns left, now facing east.
        // at the end of HAL3, facing a dead end wall, opening to HAL4 behind, east.
        
        bt.move(5); // mov11 | hal3
        pltside("left", 105); // botrel left wall is now the previous back wall.
        pltside("right", 0);
        pltside("front", 5);
        pltside("back", 10);

        bt.rotate(-90); // bot facing north, turning around out of the dead end.
        // navigating to HAL4 ENTRY now.

        bt.move(5); // mov12 | hal3
        pltside("front", 100); // back wall of HAL3, now front wall.
        pltside("left", 10);
        pltside("right", 5);
        pltside("back", 5);

        bt.move(10); // mov13 | hal3
        pltside("front", 90);
        pltside("left", 10);
        pltside("right", 5);
        pltside("back", 15);

        bt.move(10); // mov14 | hal3
        pltside("front", 80);
        pltv("rightfront", 90); // opening to HAL4 on botrel_right side.
        pltv("rightback", 5);
        pltside("left", 10);
        pltside("back", 25);

        bt.move(10); // mov15 | hal3 to hal4
        pltside("front", 70);
        pltside("right", 90);
        pltside("left", 10);
        pltside("back", 35);
        
        bt.rotate(90); // bot turns right, now facing east.
        
        //HAL4 ENTRY. angle: 90. total movs for this HAL: N/A
        bt.move(15); // mov1 | hal4
        pltv("leftfront", 10); // new left wall for HAL4
        pltv("leftback", 70); // left wall is now what was the front wall.
        pltv("rightfront", 5); // new right wall for HAL4
        pltv("rightback", 35); // right wall is now what was the back wall.
        pltside("front", 75);
        pltside("back", 30);

        bt.move(20);
        pltside("left", 10); // mov2 | hal4
        pltside("right", 5); // both right sensors now see the right wall of HAL4.
        pltside("front", 55);
        pltside("back", 50);
        
        bt.move(20); // mov3 | hal4
        pltv("leftfront", 40); // sensing the 
        pltv("leftback", 10);
        pltside("right", 5); 
        pltside("front", 35);
        pltside("back", 70);

        bt.move(20)
        pltside("left", 40); // mov4 | hal4
        pltside("right", 5); 
        pltside("front", 15);
        pltside("back", 90);

        // END OF HAL4. 

        // HAL5 ENTRY

        bt.rotate(-90); // facing north now.

        bt.move(10); // mov1 | hal5
        pltside("left", 90);
        pltside("right", 15);
        pltside("front", 30);
        pltside("back", 15);

        bt.move(10); // mov2 | hal5
        pltv("leftfront", 55); // senses opening of HAL6
        pltv("leftback", 90);
        pltside("right", 15);
        pltside("front", 20);
        pltside("back", 25);

        bt.move(15); // mov3 | hal5 to hal6
        pltside("left", 55);
        pltside("right", 15);
        pltside("front", 15);
        pltside("back", 40);



        bt.rotate(-90); // facing west now.
        // HAL6 ENTRY

        bt.move(20); // mov1 | hal6
        pltv("leftfront", 5); // new botrel_left wall for HAL6
        pltv("leftback", 90); // left wall is now what was the back wall.
        pltside("right", 5); // new botrel_right wall for HAL6
        pltside("front", 35);
        pltside("back", 35);

        bt.move(20); // mov2 | hal6
        pltside("left", 5);
        pltside("right", 65); // both right sensors now see back of HAL7.
        pltside("front", 15);
        pltside("back", 55);

        bt.move(5); // mov3 | hal6 to hal7/end
        pltside("left", 5);
        pltside("right", 65);
        pltside("front", 10);
        pltside("back", 60);
        // END OF HAL6
        // HAL7 ENTRY
        bt.rotate(90); // facing north now.

        bt.move(15); // mov1 | hal7/end
        pltside("left", 10);
        pltv("rightfront", 5); // new botrel_right wall for HAL7
        pltv("rightback", 60); // right wall is now what was the back wall.
        pltside("front", 50);
        pltside("back", 20); // old botrel_left wall of HAL6.

        bt.move(20); // mov2 | hal7/end
        pltside("left", 10);
        pltside("right", 5);
        pltside("front", 30);
        pltside("back", 40);

        bt.move(20); // mov3 | hal7/end
        pltside("left", 10);
        pltside("right", 5);
        pltside("front", 10);
        pltside("back", 60);

        // END OF MAZESIM. Bot is at the end of HAL7, facing north.




    }
    sim1();
}