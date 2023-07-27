import time
from machine import I2C, Pin
from lcd.i2c_lcd import I2CLcd
from timer.death_timer import DeathTimer
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
death_timer = DeathTimer()
devices = i2c.scan()

if devices != []:
    lcd = I2CLcd(i2c, devices[0], 2, 16)   
    death_timer.start()

    death_timer.set_ug_m3(8)
    while True:
        lcd.move_to(0, 0)
        lcd.putstr("{%d}MS" % round(death_timer.get_cumulative_life_lost_ms(), 3))
        
        death_timer.tick()
        time.sleep(1)
        

else:
    print("No address found")
